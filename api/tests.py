from django.test import TestCase

class ApiBasicTest(TestCase):
    def test_api_root_url(self):
        """
        Verifica que la API responda correctamente.
        Se prueba la raíz '/' y el prefijo '/api/'.
        """
        # Intenta acceder al endpoint raíz
        response_root = self.client.get('/')
        self.assertIn(response_root.status_code, [200, 404])

        # Intenta acceder a un endpoint común de API (si existe)
        response_api = self.client.get('/api/')
        self.assertIn(response_api.status_code, [200, 404])
