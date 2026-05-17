import firebase_admin
from firebase_admin import auth, credentials
from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from apps.users.models import User


if not firebase_admin._apps:
    cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS_PATH)
    firebase_admin.initialize_app(cred)


class FirebaseAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            return None

        token = auth_header.split("Bearer ")[1]

        try:
            decoded_token = auth.verify_id_token(token)
        except auth.ExpiredIdTokenError:
            raise AuthenticationFailed("Firebase token has expired")
        except auth.InvalidIdTokenError:
            raise AuthenticationFailed("Firebase token is invalid")
        except Exception:
            raise AuthenticationFailed("Firebase token could not be verified")

        firebase_uid = decoded_token["uid"]
        email = decoded_token.get("email", "")
        display_name = decoded_token.get("name", "")
        photo_url = decoded_token.get("picture", "")

        user, _ = User.objects.get_or_create(
            firebase_uid=firebase_uid,
            defaults={
                "email": email,
                "display_name": display_name,
                "photo_url": photo_url,
            },
        )

        return (user, None)
