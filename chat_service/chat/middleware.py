from urllib.parse import parse_qs
from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from django.conf import settings
import jwt

class JWTAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        query_string = scope.get("query_string", b"").decode()
        params = parse_qs(query_string)
        token_list = params.get("token", [])

        print("🔍 query_string:", query_string)
        print("🔍 token_list:", token_list)

        if token_list:
            token = token_list[0]
            user_data = await self.get_user_from_token(token)
            print("✅ user_data:", user_data)
            scope["user"] = user_data
        else:
            scope["user"] = None
            print("❌ No token encontrado")

        return await super().__call__(scope, receive, send)

    @database_sync_to_async
    def get_user_from_token(self, token):
        try:
            # ✅ Valida con SimpleJWT
            UntypedToken(token)

            # ✅ Decodifica sin verificar de nuevo (ya validado arriba)
            decoded = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=["HS256"]
            )

            print("🧩 decoded payload:", decoded)

            return {
                "user_id": decoded.get("user_id"),
                "role": decoded.get("role"),
                "is_authenticated": True
            }
        except (InvalidToken, TokenError) as e:
            print("❌ Token inválido:", e)
            return {"is_authenticated": False, "error": str(e)}