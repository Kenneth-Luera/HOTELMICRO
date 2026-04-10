import json
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from .authentication import CustomJWTAuthentication
from .proxy import forward_request


class GatewayView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def dispatch(self, request, service_name, path='', pk=None, *args, **kwargs):
        self.service_name = service_name
        self.forward_path = path
        self.pk = pk
        return super().dispatch(request, *args, **kwargs)

    def _proxy(self, request):
        try:
            response = forward_request(self.service_name, self.forward_path, request, pk=self.pk)
            return HttpResponse(
                content=response.content,
                status=response.status_code,
                content_type=response.headers.get('content-type', 'application/json'),
            )
        except ValueError as e:
            return HttpResponse(
                json.dumps({'error': str(e)}),
                status=404,
                content_type='application/json'
            )
        except Exception as e:
            return HttpResponse(
                json.dumps({'error': 'Gateway error', 'detail': str(e)}),
                status=502,
                content_type='application/json'
            )

    def get(self, request, *args, **kwargs):    return self._proxy(request)
    def post(self, request, *args, **kwargs):   return self._proxy(request)
    def put(self, request, *args, **kwargs):    return self._proxy(request)
    def patch(self, request, *args, **kwargs):  return self._proxy(request)
    def delete(self, request, *args, **kwargs): return self._proxy(request)


class PublicGatewayView(GatewayView):
    authentication_classes = []
    permission_classes = [AllowAny]