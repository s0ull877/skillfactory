from rest_framework import response, status
from rest_framework.decorators import api_view

from perevals.serializers import PerevalSerializer, UserProfile
from django.core.exceptions import BadRequest



@api_view(['PATCH', 'GET'])
def getedit_pereval(request, pk):

    if request.method == 'GET':

        try:
            pereval = PerevalSerializer.Meta.model.objects.get(pk=pk)
        except PerevalSerializer.Meta.model.DoesNotExist:
            return  response.Response(data={'pereval': None, 'message': f'Object with id {pk}. Does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = PerevalSerializer(pereval)
        return  response.Response(data={'pereval': serializer.data}, status=status.HTTP_200_OK)

    else:

        try:

            try:
            
                pereval = PerevalSerializer.Meta.model.objects.select_related('user','coords','level').get(pk=pk)
                serializer = PerevalSerializer(instance=pereval, data=request.data)
            
            except PerevalSerializer.Meta.model.DoesNotExist:
                return  response.Response(data={'state': 0, 'message': f'Object with id {pk}. Does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
            if serializer.is_valid():

                serializer.save()
                return response.Response(data={'state': 1, 'message': None}, status=status.HTTP_200_OK)
            
            else:
                return response.Response(data={'state': 1, 'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


        except BadRequest as ex:
            return response.Response(data={'state': 0, 'message': str(ex)}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as ex:
            return response.Response(data={'state': 0, 'message': str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        

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
                return response.Response(data={'perevals': None, 'message': 'User with this email not found'}, status=status.HTTP_404_NOT_FOUND)
            
            else:
                serializer = PerevalSerializer(perevals, many=True)
                return response.Response(data={'perevals': serializer.data, 'message': None}, status=status.HTTP_201_CREATED)


        except KeyError:
            return response.Response(data={'perevals': None, 'message': 'Invalid query params, expected `user__email`'}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as ex:

            return response.Response(data={'perevals': None, 'message': str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        