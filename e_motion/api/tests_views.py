from django.test import TestCase
from rest_framework.test import APITestCase

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from api.models import Project, LearningModel
from api.views import ProjectCreateView
from django.contrib.auth.models import User


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
