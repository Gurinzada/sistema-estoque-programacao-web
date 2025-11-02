from django.contrib.auth.hashers import make_password, check_password
from estoque.models import User
from rest_framework_simplejwt.tokens import RefreshToken


def create_user(name, jobTitle, email, password, role=User.Role.COLLABORATOR):
    hashed_password = make_password(password)
    user = User.objects.create(
        name=name,
        jobTitle=jobTitle,
        email=email,
        password=hashed_password,
        role=role
    )
    return user

def authenticate_user(email, password):
    try:
        user = User.objects.get(email=email)
        if not check_password(password, user.password):
            return {'error': 'Email ou Senha incorreta'}, 401
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
        return {'error': 'Usuário não encontrado'}, 404
    
