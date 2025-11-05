from django.contrib.auth.hashers import make_password, check_password
from estoque.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password

def create_user(name, jobTitle, email, password, role=User.Role.COLLABORATOR):
    if User.objects.filter(email=email).exists():
        raise ValueError("Já existe um usuário com este e-mail.")
    try:
        user = User.objects.create_user(email=email, name=name, password=password, jobTitle=jobTitle, role=role)
        return user
    except Exception:
        hashed = make_password(password)
        user = User.objects.create(
            name=name,
            jobTitle=jobTitle,
            email=email,
            password=hashed,
            role=role
        )
        return user

def get_user_by_id(user_id):
    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        return None

def update_user(user_id, data):
    user = get_user_by_id(user_id)
    if not user:
        return None
    allowed = {'name', 'jobTitle', 'email', 'role', 'password', 'is_active'}
    changed = False
    for key, value in data.items():
        if key not in allowed:
            continue
        if key == 'password':
            user.set_password(value)
            changed = True
        else:
            if key == 'role' and value not in (User.Role.ADMIN, User.Role.COLLABORATOR):
                continue
            setattr(user, key, value)
            changed = True
    if changed:
        user.save()
    return user

def delete_user(user_id):
    user = get_user_by_id(user_id)
    if not user:
        return False
    user.delete()
    return True

def find_all_users():
    return User.objects.all()



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
    
