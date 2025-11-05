from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from estoque.services import user_service

def serialize_user(user):
    return {
        "id": user.id,
        "name": user.name,
        "jobTitle": getattr(user, "jobTitle", None),
        "email": user.email,
        "role": user.role,
        "is_active": user.is_active,
        "createdAt": user.createdAt.isoformat() if getattr(user, "createdAt", None) else None,
        "updatedAt": user.updatedAt.isoformat() if getattr(user, "updatedAt", None) else None,
    }

@csrf_exempt
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def users_view(request):
    current_user = request.user
    if request.method == 'GET':
        if current_user.role != 'ADMIN':
            return Response({'error': 'Apenas administradores podem listar usuários.'}, status=status.HTTP_403_FORBIDDEN)
        users = user_service.find_all_users()
        serialized = [serialize_user(u) for u in users]
        return Response(serialized, status=status.HTTP_200_OK)
    if request.method == 'POST':
        if current_user.role != 'ADMIN':
            return Response({'error': 'Apenas administradores podem criar usuários.'}, status=status.HTTP_403_FORBIDDEN)
        data = request.data or {}
        required = ['name', 'email', 'password']
        if not all(k in data and data.get(k) for k in required):
            return Response({'error': 'Campos obrigatórios ausentes: name, email, password'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = user_service.create_user(
                name=data.get('name'),
                jobTitle=data.get('jobTitle'),
                email=data.get('email'),
                password=data.get('password'),
                role=data.get('role', 'COLLABORATOR')
            )
            return Response(serialize_user(user), status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['GET', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def user_detail_view(request, id):
    try:
        user_id = int(id)
    except (TypeError, ValueError):
        return Response({'error': 'ID inválido'}, status=status.HTTP_400_BAD_REQUEST)
    target_user = user_service.get_user_by_id(user_id)
    if not target_user:
        return Response({'error': 'Usuário não encontrado'}, status=status.HTTP_404_NOT_FOUND)
    current_user = request.user
    is_admin = current_user.role == 'ADMIN'
    is_owner = current_user.id == target_user.id
    if request.method == 'GET':
        if not (is_admin or is_owner):
            return Response({'error': 'Você não tem permissão para acessar este recurso.'}, status=status.HTTP_403_FORBIDDEN)
        return Response(serialize_user(target_user), status=status.HTTP_200_OK)
    if request.method == 'PATCH':
        if not is_admin:
            return Response({'error': 'Apenas administradores podem editar usuários.'}, status=status.HTTP_403_FORBIDDEN)
        data = request.data or {}
        if 'id' in data:
            data.pop('id', None)
        role = data.get('role')
        if role and role not in ['ADMIN', 'COLLABORATOR']:
            return Response({'error': 'role inválido'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            updated = user_service.update_user(user_id, data)
            if not updated:
                return Response({'error': 'Falha ao atualizar usuário.'}, status=status.HTTP_400_BAD_REQUEST)
            return Response(serialize_user(updated), status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'DELETE':
        if not is_admin:
            return Response({'error': 'Apenas administradores podem excluir usuários.'}, status=status.HTTP_403_FORBIDDEN)
        if is_owner:
            return Response({'error': 'Você não pode excluir sua própria conta.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            deleted = user_service.delete_user(user_id)
            if not deleted:
                return Response({'error': 'Falha ao excluir usuário.'}, status=status.HTTP_400_BAD_REQUEST)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

def user_template_view(request):
    return render(request, 'estoque/users.html')
