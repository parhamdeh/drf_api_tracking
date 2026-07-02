import ast

from rest_framework.test import APITestCase, APIRequestFactory

from django.contrib.auth.models import User
from django.test import override_settings

from traking.base_mixins import BaseLoggingMixin
from traking.models import APIRquestLog
from .views import MockWithMixinAPIView

@override_settings(ROOT_URLCONF='traking.tests.urls')
class TestLoggingMixin(APITestCase):
    def test_nologgin_no_log_created(self):
        self.client.get('/no-logging/')
        self.assertEqual(APIRquestLog.objects.all().count(), 0)

    def test_logging_creates_log(self):
        self.client.get('/logging/')
        self.assertEqual(APIRquestLog.objects.all().count(), 1)
    
    def test_log_path(self):
        self.client.get('/logging/')
        log = APIRquestLog.objects.first()
        self.assertEqual(log.path, '/logging/')

    def test_log_ip_remote(self):
        request = APIRequestFactory().get('/logging/')
        request.META['REMOTE_ADDR'] = '127.0.0.9'
        MockWithMixinAPIView.as_view()(request).render()
        log = APIRquestLog.objects.first()
        self.assertEqual(log.remote_address, '127.0.0.9')

    def test_log_ip_remote_list(self):
        request = APIRequestFactory().get('/logging/')
        request.META['REMOTE_ADDR'] = '127.0.0.9, 128.1.1.9'
        MockWithMixinAPIView.as_view()(request).render()
        log = APIRquestLog.objects.first()
        self.assertEqual(log.remote_address, '127.0.0.9')
    
    def test_log_ip_remote_v4_with_port(self):
        request = APIRequestFactory().get('/logging/')
        request.META['REMOTE_ADDR'] = '127.0.0.9:1234'
        MockWithMixinAPIView.as_view()(request).render()
        log = APIRquestLog.objects.first()
        self.assertEqual(log.remote_address, '127.0.0.9')

    def test_log_ip_remote_v6(self):
        request = APIRequestFactory().get('/logging/')
        request.META['REMOTE_ADDR'] = '2001:0db8:85a3:0000:0000:8a2e:0370:7334'
        MockWithMixinAPIView.as_view()(request).render()
        log = APIRquestLog.objects.first()
        self.assertEqual(log.remote_address, '2001:db8:85a3::8a2e:370:7334')
    
    def test_log_ip_remote_v6_loopback(self):
        request = APIRequestFactory().get('/logging/')
        request.META['REMOTE_ADDR'] = '::1'
        MockWithMixinAPIView.as_view()(request).render()
        log = APIRquestLog.objects.first()
        self.assertEqual(log.remote_address, '::1')
    
    def test_log_ip_remote_v6_with_port(self):
        request = APIRequestFactory().get('/logging/')
        request.META['REMOTE_ADDR'] = '[::1]:1234'
        MockWithMixinAPIView.as_view()(request).render()
        log = APIRquestLog.objects.first()
        self.assertEqual(log.remote_address, '::1')

    def test_log_host(self):
        self.client.get('/logging/')
        log = APIRquestLog.objects.first()
        self.assertEqual(log.host, 'testserver')
    
    def test_log_method(self):
        self.client.get('/logging/')
        log = APIRquestLog.objects.first()
        self.assertEqual(log.method, 'GET')
    
    def test_log_status(self):
        self.client.get('/logging/')
        log = APIRquestLog.objects.first()
        self.assertEqual(log.status_code, 200)

    def test_logging_explicit(self):
        self.client.get('/explicit-logging/')
        self.client.post('/explicit-logging/')
        self.assertEqual(APIRquestLog.objects.all().count(), 1)

    def test_custom_check_logging(self):
        self.client.get('/custom-check-logging/')
        self.client.post('/custom-check-logging/')
        self.assertEqual(APIRquestLog.objects.all().count(), 1)

    def test_log_anon_user(self):
        self.client.get('/logging/')
        log = APIRquestLog.objects.first()
        self.assertEqual(log.user, None)

    def test_log_auth_user(self):
        User.objects.create_user(username='myname', password='secret')
        user = User.objects.get(username="myname")

        self.client.login(username='myname', password='secret')
        self.client.get('/session-auth-logging/')

        log = APIRquestLog.objects.first()
        self.assertEqual(log.user, user)

    def test_log_params(self):
        self.client.get('/logging/', {'p1':'a', "another":"2"})
        log = APIRquestLog.objects.first()
        self.assertEqual(ast.literal_eval(log.query_params), {'p1':'a', "another":"2"})
    
    def test_log_params_cleaned_from_personal_list(self):
        self.client.get('/sensitive-fields-logging/', {'api':'1234', "capitalized":"12345", 'my_field':123456})
        log = APIRquestLog.objects.first()
        self.assertEqual(ast.literal_eval(log.query_params), {'api':BaseLoggingMixin.CLEANED_SUBSTITUTE, "capitalized":"12345", 'my_field':BaseLoggingMixin.CLEANED_SUBSTITUTE})
    
    def test_invalid_cleaned_substitute_fields(self):
        with self.assertRaises(AssertionError):
            self.client.get('/invalid-cleaned-subsstitute-logging/')
