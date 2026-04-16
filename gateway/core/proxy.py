import httpx
import logging
from urllib.parse import urlparse
from django.conf import settings

logger = logging.getLogger(__name__)

_client = httpx.Client(timeout=10.0)


def get_service_url(service_name: str) -> str | None:
    return settings.MICROSERVICES.get(service_name)


def forward_request(service_name: str, path: str, request, pk=None) -> httpx.Response:
    base_url = get_service_url(service_name)
    if not base_url:
        raise ValueError(f"Servicio '{service_name}' no registrado.")

    if pk:
        url = f"{base_url}/{path}{pk}/"
    else:
        url = f"{base_url}/{path}"

    logger.info(f"[GATEWAY] {request.method} {service_name} → {url}")

    headers = {
        key: value for key, value in request.headers.items()
        if key.lower() not in ('host', 'content-length')
    }
    headers['Host'] = urlparse(base_url).hostname

    if request.user and request.user.is_authenticated:
        headers['X-User-Id']    = str(request.user.id)
        headers['X-User-Email'] = getattr(request.user, 'email', '')
        headers['X-User-Role']  = getattr(request.user, 'role', 'guest')

    try:
        response = _client.request(
            method=request.method,
            url=url,
            headers=headers,
            content=request.body,
            params=request.GET,
        )
        logger.info(f"[GATEWAY] Respuesta {service_name}: {response.status_code}")
        return response

    except httpx.ConnectError as e:
        logger.error(f"[GATEWAY] Sin conexión a '{service_name}': {e}")
        raise ConnectionError(f"No se pudo conectar al servicio '{service_name}'")

    except httpx.TimeoutException as e:
        logger.error(f"[GATEWAY] Timeout en '{service_name}': {e}")
        raise TimeoutError(f"Timeout al conectar con '{service_name}'")

    except httpx.RequestError as e:
        logger.error(f"[GATEWAY] Error inesperado en '{service_name}': {e}")
        raise