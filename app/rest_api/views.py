from rest_framework import response, status
from rest_framework.decorators import api_view

from perevals.serializers import PerevalSerializer



@api_view(['PATCH', 'GET'])
def getedit_pereval(request, pk):

    if request.method == 'GET':

        try:
            pereval = PerevalSerializer.Meta.model.objects.prefetch_related('images').select_related('coords', 'level', 'user').get(pk=pk)
        except PerevalSerializer.Meta.model.DoesNotExist:
            return  response.Response(data={'pereval': None}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = PerevalSerializer(pereval)
        return  response.Response(data={'pereval': serializer.data}, status=status.HTTP_200_OK)
        ...


@api_view(['POST'])
def submitData(request):
        
    try:

        serializer = PerevalSerializer(data=request.data) 

        if serializer.is_valid():

            pereval = serializer.save(**request.data)
            resp = response.Response(data={'status': 200, 'message': None, 'id': pereval.id}, status=status.HTTP_201_CREATED)

        
        else:

            resp = response.Response(data={'status': 400, 'message': serializer.errors, 'id': None}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as ex:

        resp = response.Response(data={'status': 500, 'message': str(ex), 'id': None}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    finally:

        return  resp
        
        