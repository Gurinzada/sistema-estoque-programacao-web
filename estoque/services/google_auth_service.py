from google.oauth2 import id_token
from google.auth.transport import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

def verify_google_token(token):
    try:
        payload = id_token.verify_oauth2_token(token, requests.Request(), settings.GOOGLE_CLIENT_ID)
        return payload
    except Exception as e:
        print(e)
        return None
    
def authenticate_google_user(token):
    payload = verify_google_token(token)
    if not payload:
        return {'error': 'Token Google inválido'}, 400
    email = payload.get('email')
    if not email:
        return {"error": "No email required"}, 400
    try:
        user = User.objects.get(email=email)
        refresh = RefreshToken.for_user(user)
        return ({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': {
                'id': user.id,
                'name': user.name,
                'jobTitle': user.jobTitle,
                'email': user.email,
                'role': user.role,
                'createdAt': user.createdAt,
                'updatedAt': user.updatedAt,
            }
        }, 200)
    except User.DoesNotExist:
        return ({'error': "Usuário não encontrado"}, 403)