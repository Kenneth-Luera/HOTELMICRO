import requests
from django.http import JsonResponse
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny


def merge_schemas(schemas: list[dict]) -> dict:
    """Combina múltiples schemas OpenAPI en uno solo."""
    base = {
        "openapi": "3.0.3",
        "info": {
            "title": "Hotel Platform API",
            "version": "1.0.0",
            "description": "Documentación unificada de todos los microservicios",
        },
        "paths": {},
        "components": {
            "schemas": {},
            "securitySchemes": {
                "BearerAuth": {
                    "type": "http",
                    "scheme": "bearer",
                    "bearerFormat": "JWT",
                }
            },
        },
        "security": [{"BearerAuth": []}],
    }

    for schema in schemas:
        for path, value in schema.get("paths", {}).items():
            base["paths"][path] = value

        components = schema.get("components", {})
        for name, value in components.get("schemas", {}).items():
            base["components"]["schemas"][name] = value

    return base


class UnifiedSchemaView(APIView):
    permission_classes = [AllowAny]

    SERVICES = [
        {
            "name": "auth",
            "schema_url": f"{settings.MICROSERVICES['auth']}/api/schema/?format=json",
            "prefix": "/api/auth",
            "strip": "/api",
        },
        {
            "name": "hotels",
            "schema_url": f"{settings.MICROSERVICES['hotels']}/api/schema/?format=json",
            "prefix": "/api",
            "strip": "/api",
        },
        {
            "name": "booking",
            "schema_url": f"{settings.MICROSERVICES['booking']}/schema/?format=json",
            "prefix": "/api",
            "strip": "",
        },
    ]

    def get(self, request):
        schemas = []

        for service in self.SERVICES:
            try:
                response = requests.get(
                    service["schema_url"],
                    timeout=5,
                    headers={"Host": "localhost"},  # ← evita DisallowedHost
                )
                schema = response.json()

                remapped = {}
                for path, value in schema.get("paths", {}).items():
                    new_path = service["prefix"] + path.replace(service["strip"], "", 1)
                    remapped[new_path] = value

                schema["paths"] = remapped
                schemas.append(schema)

            except Exception as e:
                print(f"Error fetching schema from {service['name']}: {e}")

        merged = merge_schemas(schemas)
        return JsonResponse(merged)