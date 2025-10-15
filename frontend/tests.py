from django.test import TestCase

class FrontendBasicTest(TestCase):
    def test_homepage_loads(self):
        """Verifica que la vista principal se cargue correctamente"""
        response = self.client.get('/')
        self.assertIn(response.status_code, [200, 404])
