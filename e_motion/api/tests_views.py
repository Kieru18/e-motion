from django.test import TestCase, Client
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from api.models import Project, LearningModel
from api.views import ProjectCreateView
from django.contrib.auth.models import User
import json
import unittest
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from PIL import Image
import numpy as np
from io import BytesIO
import os



class BasicTest(TestCase):
    def test_hello_world(self):
        """Basic test description"""
        x = 1
        self.assertEqual(x, 1)

    def test_not_equal(self):
        """Basic test description"""
        x = 1
        self.assertNotEqual(x, 0)


# WZOREK
# ==========================================
class YourTestClass(TestCase):
    def setUp(self):
        # Setup run before every test method.
        pass

    def tearDown(self):
        # Clean up run after every test method.
        pass

    def test_something_that_will_pass(self):
        self.assertFalse(False)
# ==========================================

class SignUpViewTests(APITestCase):
    def setUp(self):
        self.url = "/api/signup"
        self.existing_user = User.objects.create_user(username='Naruto', 
                                                      password='123', 
                                                      email='konoha@gmail.com')

    def test_signup_valid(self):
        data = {
            'username': 'Sasuke',
            'password': 'ilovenaruto',
            'email': 'sussygussy@gmail.com'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.count(), 2)

    def test_signup_invalid_existing_username(self):
        data = {
            'username': 'Naruto',
            'password': 'ilovesasuke',
            'email': 'bombastick@gmail.com'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)

    def test_signup_invalid_existing_email(self):
        data = {
            'username': 'Itachi',
            'password': 'akatsuki',
            'email': 'konoha@gmail.com'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)

    def test_signup_invalid_no_email(self):
        data = {
            'username': 'Gojo',
            'password': 'nahidwin',
            'email': ''
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
    
    def test_signup_invalid_bad_email(self):
        data = {
            'username': 'Yuji',
            'password': 'lobotomykaisen',
            'email': 'fireinthehole'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)

    def test_signup_invalid_no_username(self):
        data = {
            'username': '',
            'password': 'ilovenaruto',
            'email': 'fortnite@gmail.com'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)

    def test_signup_invalid_no_password(self):
        data = {
            'username': 'Sasuke',
            'password': '',
            'email': 'theguyfromfortnite@gmail.com'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)

    def test_signup_invalid_no_username_and_password(self):
        data = {
            'username': '',
            'password': '',
            'email': 'bombocla@gmail.com'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)


class LoginViewTests(APITestCase):
    def setUp(self):
        self.url = "/api/login"
        self.existing_user = User.objects.create_user(username='Naruto', 
                                                      password='123', 
                                                      email='konoha@gmail.com')
        
    def test_login_valid(self):
        data = {
            'username': 'Naruto',
            'password': '123'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

    def test_login_invalid_wrong_password(self):
        data = {
            'username': 'Naruto',
            'password': '~123'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_invalid_non_existant_username(self):
        data = {
            'username': 'Peter Griffin',
            'password': 'i hate . . .'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_invalid_no_username(self):
        data = {
            'username': '',
            'password': '123'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_login_invalid_no_password(self):
        data = {
            'username': 'Naruto',
            'password': ''
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_login_invalid_no_username_and_password(self):
        data = {
            'username': '',
            'password': ''
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
class LogoutViewTests(APITestCase):
    def setUp(self):
        self.url = "/api/logout"
        self.user = User.objects.create_user(username='Naruto', 
                                                      password='123', 
                                                      email='konoha@gmail.com')
        self.client = APIClient()
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

    def test_logout_authenticated_user(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Token.objects.filter(user=self.user).count(), 0)

    def test_logout_unauthenticated_user(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Token.objects.filter(user=self.user).count(), 1)

    def test_logout_without_token(self):
        client_without_token = APIClient()
        response = client_without_token.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_logout_invalid_token(self):
        invalid_token = 'invalid_token'
        client_with_invalid_token = APIClient()
        client_with_invalid_token.credentials(HTTP_AUTHORIZATION=f'Token {invalid_token}')
        response = client_with_invalid_token.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class TestTokenViewTests(APITestCase):
    def setUp(self):
        self.url = "/api/test_token"
        self.user = User.objects.create_user(username='Naruto',
                                             password='123',
                                             email='konoha@gmail.com')
        self.client.force_authenticate(user=self.user)
    
    def test_test_token(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class ListProjectsViewTests(APITestCase):
    def setUp(self):
        self.test_user = User.objects.create_user(username='test', password='test')
        self.client.force_authenticate(user=self.test_user)
        Project.objects.create(title='title1', description='desc1', label_studio_project='1', user=self.test_user)
        Project.objects.create(title='title2', description='desc2', label_studio_project='2', user=self.test_user)
        self.url = "/api/list_projects"

    def test_valid_request(self):
        data = [
            {"id": 1, "title": "title1", "description": "desc1", "label_studio_project": "1", "user": 1},
            {"id": 2, "title": "title2", "description": "desc2", "label_studio_project": "2", "user": 1},
        ]
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), data)

    def test_no_projects(self):
        for record in Project.objects.filter(user=self.test_user):
            record.delete()

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), [])

class ListModelsViewTest(APITestCase):
    def setUp(self):
        self.test_user = User.objects.create_user(username='test', password='test')
        self.client.force_authenticate(user=self.test_user)
        self.project = Project.objects.create(title='title1', description='desc1', label_studio_project='1', user=self.test_user)
        LearningModel.objects.create(name="model1", architecture="Faster RCNN", project=self.project)
        LearningModel.objects.create(name="model2", architecture="Faster RCNN", project=self.project)
        self.url = f"/api/list_models/{self.project.id}/"

    def test_valid_request(self):
        data = [
            {"id": 1, "name": "model1", "architecture": "Faster RCNN", 'miou_score': None, 'top1_score': None, 'top5_score': None},
            {"id": 2, "name": "model2", "architecture": "Faster RCNN", 'miou_score': None, 'top1_score': None, 'top5_score': None},
        ]
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), data)

    def test_no_models(self):
        for record in LearningModel.objects.filter(project=self.project):
            record.delete()

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), [])



class ProjectCreateViewTests(APITestCase):
    def setUp(self):
        self.test_user = User.objects.create_user(username='test', password='test')
        self.client.force_authenticate(user=self.test_user)
        self.url = "/api/create_project"

    def test_create_project_valid(self):
        data = {
            'title': 'title',
            'description': 'description',
            'label_studio_project': 'label_studio_project',
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Project.objects.count(), 1)
        self.assertEqual(Project.objects.get().title, 'title')

    def test_create_project_invalid(self):
        data = {
            'description': 'description',
            'dataset': '',
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(Project.objects.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_project_unauthorized(self):
        self.client.force_authenticate(user=None)
        data = {
            'description': 'description',
            'dataset': '',
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_project_no_data(self):
        response = self.client.post(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class ModelCreateViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='test')
        self.token = Token.objects.create(user=self.user)
        self.project = Project.objects.create(title='title1', description='desc1', label_studio_project='1', user=self.user)
        self.url = "/api/create_model"

    def test_create_model_valid(self):
        data = {
            'name': 'model1',
            'architecture': 'Faster RCNN',
            'learning_rate': 0.0001,
            'weight_decay': 0.0001,
            'epochs': 100,
            'validation_set_size': 10,
            'miou_score': '',
            'top1_score': '',
            'top5_score': '',
            'checkpoint': '',
            'project': self.project.id
        }
        response = self.client.post(
            self.url,
            data,
            HTTP_AUTHORIZATION=f'Token {self.token.key}'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(LearningModel.objects.count(), 1)
        self.assertEqual(LearningModel.objects.get().name, 'model1')

    def test_create_model_invalid_empty_project(self):
        data = {
            'name': 'model1',
            'architecture': 'Faster RCNN',
            'learning_rate': 0.0001,
            'weight_decay': 0.0001,
            'epochs': 100,
            'validation_set_size': 10,
            'miou_score': '',
            'top1_score': '',
            'top5_score': '',
            'checkpoint': '',
            'project': ''
        }
        response = self.client.post(
            self.url,
            data,
            HTTP_AUTHORIZATION=f'Token {self.token.key}'
        )
        self.assertEqual(LearningModel.objects.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_model_invalid_bad_architecture(self):
        data = {
            'name': 'model1',
            'architecture': '片思いサンバ', # obviously not a valid architecture
            'learning_rate': 0.0001,
            'weight_decay': 0.0001,
            'epochs': 100,
            'validation_set_size': 10,
            'miou_score': '',
            'top1_score': '',
            'top5_score': '',
            'checkpoint': '',
            'project': self.project.id
        }
        response = self.client.post(
            self.url,
            data,
            HTTP_AUTHORIZATION=f'Token {self.token.key}'
        )
        self.assertEqual(LearningModel.objects.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_model_invalid_no_data(self):
        response = self.client.post(
            self.url,
            HTTP_AUTHORIZATION=f'Token {self.token.key}'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_model_invalid_unauthorized(self):
        data = {
            'name': 'model1',
            'architecture': 'Faster RCNN',
            'learning_rate': 0.0001,
            'weight_decay': 0.0001,
            'epochs': 100,
            'validation_set_size': 10,
            'miou_score': '',
            'top1_score': '',
            'top5_score': '',
            'checkpoint': '',
            'project': self.project.id
        }
        response = self.client.post(
            self.url,
            data
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        
        file_path = "/path/to/file.json"        


class UploadAnnotationViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.model_id = 1
        self.url = f'/api/upload_annotation/{self.model_id}/'

    def test_upload_annotation_authenticated(self):
        self.client.login(username='testuser', password='testpassword')

        json_file = SimpleUploadedFile('file.json', b'{"key": "value"}', 
                                       content_type='application/json')
        data = {
            'file': json_file,
            'name': 'modellussy',
            'architecture': 'Faster RCNN',
            'learning_rate': 0.0001,
            'weight_decay': 0.0001,
            'epochs': 100,
            'validation_set_size': 10,
            'miou_score': '',
            'top1_score': '',
            'top5_score': '',
            'checkpoint': '',
            'project': 1
        }
        response = self.client.post(
            self.url,
            data,
            HTTP_AUTHORIZATION=f'Token {self.token.key}'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['success'])

    def test_upload_annotation_unauthenticated(self):
        json_file = SimpleUploadedFile('file.json', b'{"key": "value"}', 
                                       content_type='application/json')
        data = {
            'file': json_file,
            'name': 'modellussy',
            'architecture': 'Faster RCNN',
            'learning_rate': 0.0001,
            'weight_decay': 0.0001,
            'epochs': 100,
            'validation_set_size': 10,
            'miou_score': '',
            'top1_score': '',
            'top5_score': '',
            'checkpoint': '',
            'project': 1
        }
        response = self.client.post(
            self.url,
            data
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_upload_annotation_invalid_file(self):
        self.client.login(username='testuser', password='testpassword')

        json_file = SimpleUploadedFile('skibidi.txt', b'ogladacie moze skibidi toilet?', 
                                       content_type='text/plain')
        data = {
            'file': json_file,
            'name': 'modellussy',
            'architecture': 'Faster RCNN',
            'learning_rate': 0.0001,
            'weight_decay': 0.0001,
            'epochs': 100,
            'validation_set_size': 10,
            'miou_score': '',
            'top1_score': '',
            'top5_score': '',
            'checkpoint': '',
            'project': 1
        }
        response = self.client.post(
            self.url,
            data,
            HTTP_AUTHORIZATION=f'Token {self.token.key}'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_upload_annotation_no_file(self):
        self.client.login(username='testuser', password='testpassword')

        data = {
            'name': 'modellussy',
            'architecture': 'Faster RCNN',
            'learning_rate': 0.0001,
            'weight_decay': 0.0001,
            'epochs': 100,
            'validation_set_size': 10,
            'miou_score': '',
            'top1_score': '',
            'top5_score': '',
            'checkpoint': '',
            'project': 1
        }
        response = self.client.post(
            self.url,
            data,
            HTTP_AUTHORIZATION=f'Token {self.token.key}'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ProjectDeleteViewTests(APITestCase):
    def setUp(self):
        self.test_user = User.objects.create_user(username='test', password='test')
        self.client.force_authenticate(user=self.test_user)
        Project.objects.create(title='title1', description='desc1', label_studio_project='1', user=self.test_user)
        Project.objects.create(title='title2', description='desc2', label_studio_project='2', user=self.test_user)
        self.url = "/api/delete_project"

    def test_valid_request(self):
        data = {'id': 1}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(Project.objects.count(), 1)
        self.assertEqual(Project.objects.get().title, 'title2')

    def test_no_projects(self):
        for record in Project.objects.filter(user=self.test_user):
            record.delete()
        data = {'id': 1}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(Project.objects.count(), 0)


class ProjectEditViewTests(APITestCase):
    def setUp(self):
        self.test_user = User.objects.create_user(username='test', password='test')
        self.client.force_authenticate(user=self.test_user)
        Project.objects.create(title='title1', description='desc1', label_studio_project='1', user=self.test_user)
        Project.objects.create(title='title2', description='desc2', label_studio_project='2', user=self.test_user)
        self.url = "/api/edit_project"

    def test_valid_edit_request(self):
        data = {"id": 1, "title": "new", "description": "desc1", "label_studio_project": "1", "user": 1}
        expected = "new"

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(Project.objects.get(id=1).title, expected)

    def test_invalid_request_no_id(self):
        data = {"title": "new", "description": "desc1", "label_studio_project": "1", "user": 1}

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_request_incorrect_field(self):
        data = {"id": 1, "pods": "new", "description": "desc1", "label_studio_project": "1", "user": 1}

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_request_no_data(self):
        response = self.client.post(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ListScoresViewTests(APITestCase):
    def setUp(self):
        self.test_user = User.objects.create_user(username='test', password='test')
        self.client.force_authenticate(user=self.test_user)
        self.project = Project.objects.create(title='title1', description='desc1', label_studio_project='1', user=self.test_user)
        self.model = LearningModel.objects.create(name="model1", architecture="Faster RCNN", project=self.project,
                                                  miou_score=0.2, top1_score=0.1, top5_score=0.3)
        self.url = f"/api/get_scores/{self.model.id}/"

    def test_valid_request(self):
        data = {"miou_score": 0.2, "top1_score": 0.1, "top5_score": 0.3}

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), data)

class MakePredictionsViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.project = Project.objects.create(title='title1', description='desc1', label_studio_project='1', user=self.user)
        self.model = LearningModel.objects.create(name="model1", architecture="Faster RCNN", project=self.project)
        
        self.url = f'/api/make_predictions/{self.project.id}/{self.model.id}/'

    def test_make_predictions_unauthenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
 
class TrainViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.model_id = 1
        self.url = f'/api/train/{self.model_id}/'

    def test_train_unauthenticated(self):
 
        response = self.client.post(
            self.url,
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)



# class UploadFilesViewTests(APITestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(username='testuser', password='testpassword')
#         self.token = Token.objects.create(user=self.user)
#         self.project_id = 1
#         self.url = f'/api/upload/{self.project_id}/'
        
#         gradient = np.arange(0, 255, 25).reshape((1, -1)).astype(np.uint8)
#         pixel_data = np.tile(gradient, (10, 1))

#         image = Image.fromarray(pixel_data, mode='L')
#         image_io = BytesIO()
#         image.save(image_io, format='JPEG')

#         self.valid_image_file = SimpleUploadedFile('image1.jpeg', image_io.getvalue(), 
#                                                     content_type='image/jpeg')


#     def test_upload_files_authenticated(self):
#         self.client.login(username='testuser', password='testpassword')

#         data = {
#             'file': self.valid_image_file,
#         }
#         response = self.client.post(
#             self.url,
#             data,
#             HTTP_AUTHORIZATION=f'Token {self.token.key}'
#         )

#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertTrue(response.data['success'])
# always returns 400
        
