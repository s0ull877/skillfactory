from django.forms import ValidationError
from rest_framework import response, status
from rest_framework.decorators import api_view

from perevals.serializers import PerevalSerializer
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
        
        

@api_view(['POST'])
def submitData(request):
        
    try:

        serializer = PerevalSerializer(data=request.data) 

        if serializer.is_valid():

            pereval = serializer.save(**request.data)
            return response.Response(data={'status': 200, 'message': None, 'id': pereval.id}, status=status.HTTP_201_CREATED)
        
        else:

            return response.Response(data={'status': 400, 'message': serializer.errors, 'id': None}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as ex:

        return response.Response(data={'status': 500, 'message': str(ex), 'id': None}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
        
        