from django.db import transaction
from django.core.files.base import ContentFile
from django.forms import ValidationError

from rest_framework import serializers

from .models import Pereval,PerevalImage,PerevalLevel,Coordinates

from users.serializers import UserProfileSerializer, UserProfile


class CoordinatesSerializer(serializers.ModelSerializer):

    class Meta:
        
        model = Coordinates
        fields = ('latitude', 'longitude', 'height',)


class PerevalLevelSerializer(serializers.ModelSerializer):

    class Meta:
        
        model = PerevalLevel
        fields = ('winter', 'summer', 'autumn', 'spring')
        

class PerevalSerializer(serializers.ModelSerializer):

    user = UserProfileSerializer()
    coords = CoordinatesSerializer()
    level = PerevalLevelSerializer()
    images = serializers.ListField()

    class Meta:
        
        model = Pereval
        fields = ('beauty_title', 'title', 'connect', 'add_time', 'user', 'coords', 'level', 'images')


    # проверка ключей, для последующей подготовки, 
    # можно было бы сделать через dict.keys(), но уже оставил так
    def validate_images(self, images):
        for image in images:
            try:
                image['data']
                image['title']
            except KeyError as ex:
                raise ValidationError(f'Field {ex.args[0]} in images element is required!')

        return images

    # делаю из кодированных байтов ContentFile, для дальнейшей обработки ImageField
    def prepare_images(self, images):
        for i in range(0, len(images)):
            images[i]['data'] = ContentFile(images[i]['data'], name='image.jpg')

        return images


    def create(self, validated_data):

        validated_data['images'] = self.prepare_images(validated_data['images'])

        # атомарная транзакция, ибо если будет какой-то косяк, 
        # то смысла в предшевствующих запросах больше нет
        with transaction.atomic():
            user = UserProfile.objects.get_or_create(**validated_data.pop('user'))[0]
            coords = Coordinates.objects.create(**validated_data.pop('coords'))
            level = PerevalLevel.objects.create(**validated_data.pop('level'))
            instance = Pereval.objects.create(
                beauty_title=validated_data.pop('beauty_title'),
                title=validated_data.pop('title'),
                other_titles=validated_data.pop('other_titles'),
                connect=validated_data.pop('connect'),
                add_time=validated_data.pop('add_time'),
                user=user,
                coords=coords,
                level=level
            )

            for image in validated_data.pop('images'):
                    
                    PerevalImage.objects.create(
                        to_pereval=instance,
                        title=image['title'],
                        image=image['data']
                    )
            
        return instance
    

    
    def to_representation(self, instance):

        data = {}

        # берем все поля, включая status из модели перевал
        fields = instance._meta.get_fields()
        for field in fields:
                
            # так как images явно не указана в модели Pereval, 
            # попытка взять название приводит к AttributeError
            try:

                # _id оканчивается у oneToOne и foreign связей
                if field.attname.endswith('_id'):
                    field_name = field.attname.replace('_id', '') #меняем название с field_id на field
                    # берем класс сериализатора из self.fields.fields и получаем данные
                    data[field_name] = self.fields.fields[field_name].to_representation(instance=getattr(instance, field_name))
                
                else:
                    
                    data[field.attname] = getattr(instance, field.attname)

            # ловим поле images
            except AttributeError:
                
                images = []
                
                # достаем все обьекты и апендим в список
                for image in instance.images.all():
                    images.append({
                        'title': image.title,
                        'data': image.image.url
                    })
        
        # добавляем в конце, так красивее
        data['images'] = images
        
        return data

            

