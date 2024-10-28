import re

from django.db import transaction
from django.forms import ValidationError
from django.core.exceptions import BadRequest
from django.core.files.base import ContentFile

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
        fields = ('beauty_title', 'title', 'other_titles', 'connect', 'add_time', 'user', 'coords', 'level', 'images')


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
    def prepare_image(self, image):

        return {
            'title': image['title'],
            'data': ContentFile(image['data'], name='image.jpg')
            }
    
    
    # запарно работать с фото, вынес в отдельную функцию
    def update_images(self, instance: Pereval, images: list):

        # получение текущих фотографий
        self_images = instance.images.all()
        # новые фото
        for image in images:

            # если в data находится url, то проверим, есть ли он в текущих
            match = re.search(r'/media/(perevals_images/image_[^/]+.jpg)',image['data'])
            if match:

                try:
                    perevalimage = self_images.filter(image=match.group(1))
                    perevalimage.update(title=image['title'])
                    # если есть, мы вытаскиваем его из queryset, чтобы не удалять
                    self_images = self_images.exclude(pk=perevalimage.first().id)

                except perevalimage.DoesNotExist:
                    # иначе пишем что он невалидный
                    raise BadRequest("Incorect uri. Images index {}. If u want add new file, send with base64".format(images.index(image)))

            # новые фото мы создаем и присваиваем к instance
            else:
                image = self.prepare_image(image=image)
                PerevalImage.objects.create(
                    to_pereval=instance,
                    title=image['title'],
                    image=image['data']
                )

        # в результате в текущих фотографиях остаются фото
        # который нет validated_data, если их нет в запросе,
        # то нет и на сервере
        # грубо говоря, если у нас на перевале 3 текущих фото,
        # а в запросе пришло 2 фото, то мы удаляем лишнюю
        self_images.delete()


    def create(self, validated_data):

        validated_data['new_images'] = []

        for image in validated_data['images']:
            validated_data['new_images'].append(self.prepare_image(image))

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

            for image in validated_data.pop('new_images'):
                    
                    PerevalImage.objects.create(
                        to_pereval=instance,
                        title=image['title'],
                        image=image['data']
                    )
            
        return instance
    

    def update(self, instance, validated_data):
        
        if instance.status != 'new':
            raise BadRequest("This pereval cant be edited, because status not 'new'.")
        
        user = validated_data.pop('user')
        for attr in user.keys():

            if user[attr] != getattr(instance.user, attr): 
                raise BadRequest(f'You cant edit user data: {attr}')
        

        instance.coords.__class__.objects.filter(pk=instance.coords.id).update(**validated_data.pop('coords'))
        instance.level.__class__.objects.filter(pk=instance.level.id).update(**validated_data.pop('level'))

        self.update_images(instance, validated_data.pop('images'))

        self.Meta.model.objects.filter(pk=instance.id).update(**validated_data)
        
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

            

