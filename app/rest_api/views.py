from rest_framework import response, status
from rest_framework.decorators import api_view

import base64

from perevals.serializers import PerevalSerializer, PerevalImage

from django.core.files.base import ContentFile


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