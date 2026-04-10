import httpx
from django.conf import settings


def get_service_url(service_name: str) -> str | None:
    return settings.MICROSERVICES.get(service_name)


def forward_request(service_name: str, path: str, request, pk=None) -> httpx.Response:
    base_url = get_service_url(service_name)
    if not base_url:
        raise ValueError(f"Servicio '{service_name}' no registrado.")

    # Si viene un pk lo agregamos al path
    if pk:
        url = f"{base_url}/{path}{pk}/"
    else:
        url = f"{base_url}/{path}"

    headers = {
        key: value for key, value in request.headers.items()
        if key.lower() not in ('host', 'content-length')
    }
    headers['Host'] = 'localhost'

    if request.user and request.user.is_authenticated:
        headers['X-User-Id']    = str(request.user.id)
        headers['X-User-Email'] = getattr(request.user, 'email', '')
        headers['X-User-Role']  = getattr(request.user, 'role', 'guest')

    with httpx.Client(timeout=10.0) as client:
        response = client.request(
            method=request.method,
            url=url,
            headers=headers,
            content=request.body,
            params=request.GET,
        )

    return response