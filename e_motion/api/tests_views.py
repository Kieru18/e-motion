"""
Unit tests for the views in the 'api' application.

This module contains tests for the views defined in the 'api' application's views.py file.
Test cases cover the handling of HTTP requests, responses, and the overall behavior of the views.
"""

from django.test import TestCase
from rest_framework.test import APITestCase

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from api.models import Project, LearningModel
from api.views import ProjectCreateView
from django.contrib.auth.models import User
import json


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


class ProjectCreateViewTests(APITestCase):
    def setUp(self):
        self.test_user = User.objects.create_user(username='test', password='test')
        self.client.force_authenticate(user=self.test_user)
        self.url = "/api/create_project"

    def test_create_project_valid(self):
        data = {
            'title': 'title',
            'description': 'description',
            'dataset_url': 'dataset_url',
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


class ProjectDeleteViewTests(APITestCase):
    def setUp(self):
        self.test_user = User.objects.create_user(username='test', password='test')
        self.client.force_authenticate(user=self.test_user)
        Project.objects.create(title='title1', description='desc1', dataset_url='url1', user=self.test_user)
        Project.objects.create(title='title2', description='desc2', dataset_url='url2', user=self.test_user)
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
        Project.objects.create(title='title1', description='desc1', dataset_url='url1', user=self.test_user)
        Project.objects.create(title='title2', description='desc2', dataset_url='url2', user=self.test_user)
        self.url = "/api/edit_project"

    def test_valid_edit_request(self):
        data = {"id": 1, "title": "new", "description": "desc1", "dataset_url": "url1", "user": 1}
        expected = "new"

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(Project.objects.get(id=1).title, expected)

    def test_invalid_request_no_id(self):
        data = {"title": "new", "description": "desc1", "dataset_url": "url1", "user": 1}

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_request_incorrect_field(self):
        data = {"id": 1, "pods": "new", "description": "desc1", "dataset_url": "url1", "user": 1}

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ListProjectsViewTests(APITestCase):
    def setUp(self):
        self.test_user = User.objects.create_user(username='test', password='test')
        self.client.force_authenticate(user=self.test_user)
        Project.objects.create(title='title1', description='desc1', dataset_url='url1', user=self.test_user)
        Project.objects.create(title='title2', description='desc2', dataset_url='url2', user=self.test_user)
        self.url = "/api/list_projects"

    def test_valid_request(self):
        data = [
            {"id": 1, "title": "title1", "description": "desc1", "dataset_url": "url1", "user": 1},
            {"id": 2, "title": "title2", "description": "desc2", "dataset_url": "url2", "user": 1},
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
        self.project = Project.objects.create(title='title1', description='desc1', dataset_url='url1', user=self.test_user)
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


class ListScoresViewTest(APITestCase):
    def setUp(self):
        self.test_user = User.objects.create_user(username='test', password='test')
        self.client.force_authenticate(user=self.test_user)
        self.project = Project.objects.create(title='title1', description='desc1', dataset_url='url1', user=self.test_user)
        self.model = LearningModel.objects.create(name="model1", architecture="Faster RCNN", miou_score=0.0, top1_score=0.6, top5_score=0.7, project=self.project)
        self.url = f"/api/get_scores/{self.model.id}/"

    def test_valid_request(self):
        result = {'miou_score': 0.0, 'top1_score': 0.6, 'top5_score': 0.7}

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), result)

    def test_no_models_bad_request(self):
        for record in LearningModel.objects.filter(project=self.project):
            record.delete()

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(json.loads(response.content), {'detail': 'Not found.'})


class MakePredictionsViewTest(APITestCase):
    def setUp(self):
        self.test_user = User.objects.create_user(username='test', password='test')
        self.client.force_authenticate(user=self.test_user)
        self.project = Project.objects.create(title='title1', description='desc1', dataset_url='url1', user=self.test_user)
        self.model = LearningModel.objects.create(id=1, name="model1", architecture="Faster RCNN", miou_score=0.0, top1_score=0.6, top5_score=0.7, project=self.project)
        self.url = "/api/make_predictions/1/1/"

    def test_get_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_no_model_in_db(self):
        invalid_model_id_url = f'/api/make_predictions/{self.project.id}/2/'
        response = self.client.get(invalid_model_id_url)
        self.assertEqual(response.status_code, 404)
