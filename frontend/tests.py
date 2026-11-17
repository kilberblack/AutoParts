from django.test import TestCase


class PaginaInicioTest(TestCase):
    def test_pagina_inicio_responde(self):
        respuesta = self.client.get("/")
        self.assertEqual(respuesta.status_code, 200)