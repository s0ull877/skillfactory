import json

from django.test import TestCase

from django.urls import reverse
from django import setup

from .consts import BODY

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'store.settings')
setup()

class SubmitDataTestCase(TestCase):

    def setUp(self):

        self.view_path= reverse('rest_api:submitData')
        self.test_data = BODY

        return super().setUp()

    def test_post_request(self):
        
        body = self.test_data
        response = self.client.post(
            path=self.view_path,
            data=json.dumps(body),
            content_type='application/json'
        )
        self.assertIsNotNone(response.data['id'])

        # делаем невалидный email
        body['user']['email'] = "qwerty@ru"
        response = self.client.post(
            path=self.view_path,
            data=json.dumps(body),
            content_type='application/json'
        )
        self.assertEqual(400, response.status_code)
        self.assertIsNone(response.data['id'])


    def test_get_request(self):
        
        # чекер запроса с пустым query
        response = self.client.get(
            path=self.view_path
        )
        self.assertEqual(400, response.status_code)
        self.assertIsNone(response.data['perevals'])

        # неверный ключ query
        response = self.client.get(
            path=self.view_path,
            query_params={'email': 'qwerty@com.ru'}
        )

        self.assertEqual(400, response.status_code)
        self.assertIsNone(response.data['perevals'])


        # несуществующий email
        response = self.client.get(
            path=self.view_path,
            query_params={'user__email': 'qwerty@.ru'}
        )

        self.assertEqual(404, response.status_code)
        self.assertIsNone(response.data['perevals'])
        

        # создаем модель и чекаем существует ли она
        response = self.client.post(
            path=self.view_path,
            data=json.dumps(self.test_data),
            content_type='application/json'
        )
        self.assertIsNotNone(response.data['id'])

        response = self.client.get(
            path=self.view_path,
            query_params={'user__email': 'qwerty@com.ru'}
        )

        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response.data['perevals'])


class SubmitDataPKTestCase(TestCase):

    def setUp(self):
        self.create_path= reverse('rest_api:submitData')
        self.test_data = BODY


    def test_requests(self):
            
            response = self.client.post(
                path=self.create_path,
                data=json.dumps(self.test_data),
                content_type='application/json'
            )
            self.assertEqual(201, response.status_code)

            path=reverse('rest_api:submitDataPK', kwargs={'pk':response.data['id']})

            # получаем модель которую создали
            response = self.client.get(
                path=path
            )

            self.assertEqual(200, response.status_code)
            self.assertIsNotNone(response.data['pereval'])


            # PATCH
            body=response.data['pereval']
            body['title']='test_title'

            response = self.client.patch(
                path=path,
                data=json.dumps(body,default=str),
                content_type='application/json'
            )

            self.assertEqual(200, response.status_code)
            self.assertEqual(1, response.data['state'])

            # чекаем поменялся ли title
            response = self.client.get(
                path=path
            )

            self.assertEqual(body['title'], response.data['pereval']['title'])

            # пытаемся изменить поля user
            body['user']['fam']='Галиуллин'

            response = self.client.patch(
                path=path,
                data=json.dumps(body,default=str),
                content_type='application/json'
            )

            self.assertEqual(400, response.status_code)
            self.assertEqual(0, response.data['state'])