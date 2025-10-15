#!/usr/bin/env bash
set -e

echo "==> Limpiando reportes previos..."
rm -rf htmlcov coverage.xml .coverage 2>/dev/null || true

echo "==> Ejecutando pruebas unitarias con coverage..."
coverage run manage.py test || true  # continúa aunque fallen tests para reportar

echo "==> Resumen de cobertura (con líneas no cubiertas):"
coverage report -m || true

echo "==> Generando coverage.xml y reporte HTML..."
coverage xml -o coverage.xml || true
coverage html || true

echo "==> Tests fallidos (si los hubo) ya quedaron mostrados arriba por Django."
echo "==> Revisa también htmlcov/index.html para un reporte navegable."
