from google.oauth2 import id_token, credentials
from google.auth.transport import requests as google_requests
from google_auth_oauthlib.flow import Flow
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
import os

User = get_user_model()

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

def get_google_flow():
    return Flow.from_client_secrets_file(
        settings.GOOGLE_CLIENT_SECRETS_FILE,
        scopes=[
            'https://www.googleapis.com/auth/userinfo.email',
            'https://www.googleapis.com/auth/userinfo.profile',
            'openid'
        ],
        redirect_uri=settings.GOOGLE_REDIRECT_URI
    )

def get_google_tokens_and_user_info(code):
    flow = get_google_flow()
    flow.fetch_token(code=code)
    
    creds = flow.credentials
    
    request = google_requests.Request()
    id_info = id_token.verify_oauth2_token(
        id_token=creds.id_token, request=request, audience=settings.GOOGLE_CLIENT_ID
    )
    
    return id_info

def handle_google_redirect_login(code):
    try:
        user_info = get_google_tokens_and_user_info(code)
        email = user_info.get('email')
        if not email:
            raise ValueError("Email não retornado pelo Google.")

        user = User.objects.get(email=email)
        refresh = RefreshToken.for_user(user)
        return {
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh)
        }

    except Exception as e:
        print(f"Erro durante a autenticação Google: {e}")
        return None
