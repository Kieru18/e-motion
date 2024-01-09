from django.test import TestCase
from django.urls import resolve
from api.views import SignUpView, LoginView, LogoutView, ListProjectsView, \
                   ListModelsView, ProjectCreateView, ProjectDeleteView, ProjectEditView, \
                   MakePredictionsView, UploadFilesView, UploadAnnotationView


class UrlsTest(TestCase):
    def test_signup_url(self):
        path = "/api/signup"
        resolver = resolve(path)
        self.assertEqual(resolver.func.view_class, SignUpView)

    def test_login_url(self):
        path = "/api/login"
        resolver = resolve(path)
        self.assertEqual(resolver.func.view_class, LoginView)

    def test_logout_url(self):
        path = "/api/logout"
        resolver = resolve(path)
        self.assertEqual(resolver.func.view_class, LogoutView)

    def test_list_projects_url(self):
        path = "/api/list_projects"
        resolver = resolve(path)
        self.assertEqual(resolver.func.view_class, ListProjectsView)

    def test_list_models_url(self):
        path = "/api/list_models/1/"
        resolver = resolve(path)
        self.assertEqual(resolver.func.view_class, ListModelsView)

    def test_create_project_url(self):
        path = "/api/create_project"
        resolver = resolve(path)
        self.assertEqual(resolver.func.view_class, ProjectCreateView)

    def test_delete_project_url(self):
        path = "/api/delete_project"
        resolver = resolve(path)
        self.assertEqual(resolver.func.view_class, ProjectDeleteView)

    def test_edit_project_url(self):
        path = "/api/edit_project"
        resolver = resolve(path)
        self.assertEqual(resolver.func.view_class, ProjectEditView)

    def test_upload_annotation_url(self):
        path = "/api/upload_annotation"
        resolver = resolve(path)
        self.assertEqual(resolver.func.view_class, UploadAnnotationView)

    def test_make_predictions_url(self):
        path = "/api/make_predictions/1/1/"
        resolver = resolve(path)
        self.assertEqual(resolver.func.view_class, MakePredictionsView)

    def test_upload_files_url(self):
        path = "/api/upload/1/"
        resolver = resolve(path)
        self.assertEqual(resolver.func.view_class, UploadFilesView)
