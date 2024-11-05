import json
from rest_framework import response, status
from rest_framework.decorators import api_view

from perevals.serializers import PerevalSerializer, UserProfile
from django.core.exceptions import BadRequest

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi



@swagger_auto_schema(method='patch', 
                     operation_description='Частичноое изменение модели Pereval. state=1, если изменение успешно', 
                     request_body=PerevalSerializer,
                     responses={
                        200: json.dumps({'state': 1, 'message': None}),
                        400: json.dumps({'state': 0, 'message': 'Some request body errors'}),
                        404: json.dumps({'state': 1, 'message': 'Object with this id Does not exist'}),
                        500: json.dumps({'state': 0, 'message': 'Some server errors'}),
                         
                     })
@swagger_auto_schema(method='get',
                     operation_description='Получение обьекта pereval по его id, включая его статус модерации и id', 
                     responses={
                        200: PerevalSerializer,
                        404: json.dumps({'pereval':None, 'message':'Object with this id Does not exist'})
                     })
@api_view(['PATCH', 'GET'])
def getedit_pereval(request, pk):

    try:
        pereval = PerevalSerializer.Meta.model.objects.select_related('user','coords','level').get(pk=pk)
    except PerevalSerializer.Meta.model.DoesNotExist:
        return  response.Response(data={'pereval': None, 'message': f'Object with id {pk}. Does not exist'}, status=status.HTTP_404_NOT_FOUND)


    if request.method == 'GET':

        serializer = PerevalSerializer(pereval)
        return  response.Response(data={'pereval': serializer.data}, status=status.HTTP_200_OK)

    # PATCH
    else:

        try:

            serializer = PerevalSerializer(instance=pereval, data=request.data)
        
            if serializer.is_valid():

                serializer.save()
                return response.Response(data={'state': 1, 'message': None}, status=status.HTTP_200_OK)
            
            else:
                return response.Response(data={'state': 0, 'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        except BadRequest as ex:
            return response.Response(data={'state': 0, 'message': str(ex)}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as ex:
            return response.Response(data={'state': 0, 'message': str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



test_param = openapi.Parameter('user__email', openapi.IN_QUERY, description="user email param", type=openapi.TYPE_STRING)
user_response = openapi.Response('response description', PerevalSerializer) 

@swagger_auto_schema(method='get', manual_parameters=[test_param],
                     operation_description='Получение всех обьектов pereval созданных пользователем указанным в user__email', 
                     responses={
                        200: PerevalSerializer(many=True),
                        400: json.dumps({'pereval': None, 'message': 'Invalid query params, expected `user__email`'}),
                        404: json.dumps({'pereval': None, 'message': 'User with this email not found.'}),
                        500: json.dumps({'pereval': None, 'message': 'Some server error'}),
                     })
@swagger_auto_schema(method='post', request_body=PerevalSerializer,
                     operation_description='Создание обьекта pereval', 
                     responses={
                        201: json.dumps({'status': 200, 'message': None, 'id': 'id of created object here'}),
                        400: json.dumps({'status': 400, 'message': 'some serializers errors here', 'id': None}),
                        500: json.dumps({'status': 500, 'message': 'Some server error', 'id': None}),
                     })
@api_view(['POST', 'GET'])
def submitData(request):

    if request.method == 'POST':    
        try:

            serializer = PerevalSerializer(data=request.data) 

            if serializer.is_valid():

                pereval = serializer.save(**request.data)
                return response.Response(data={'status': 200, 'message': None, 'id': pereval.id}, status=status.HTTP_201_CREATED)
            
            else:

                return response.Response(data={'status': 400, 'message': serializer.errors, 'id': None}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as ex:

            return response.Response(data={'status': 500, 'message': str(ex), 'id': None}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    else:

        try:
            # perevals = PerevalSerializer.objects.filter(**request.query_params)
            perevals = PerevalSerializer.Meta.model.objects.filter(user__email=request.query_params['user__email'])

            if not perevals.exists():
                return response.Response(data={'perevals': None, 'message': 'User with email {} not found.'.format(request.query_params['user__email'])}, status=status.HTTP_404_NOT_FOUND)
            
            else:
                serializer = PerevalSerializer(perevals, many=True)
                return response.Response(data={'perevals': serializer.data, 'message': None}, status=status.HTTP_200_OK)


        except KeyError:
            return response.Response(data={'perevals': None, 'message': 'Invalid query params, expected `user__email`'}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as ex:

            return response.Response(data={'perevals': None, 'message': str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        