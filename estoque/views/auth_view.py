from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from estoque.services.user_service import authenticate_user
from estoque.services.google_auth_service import authenticate_google_user
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def login_email_view(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response({'error': 'Email and Password are required'}, status=400)
    
    result, status = authenticate_user(email=email, password=password)
    return Response(result, status=status)

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def login_google_view(request):
    token = request.data.get('credential')
    if not token:
        return Response({'error': "Token not provided"}, status=400)
    result, status = authenticate_google_user(token=token)
    return Response(result, status=status)

@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user_view(request):
    user = request.user
    print(user)
    return Response({
        'id': user.id,
        'name': user.name,
        'jobTitle': user.jobTitle,
        'email': user.email,
        'role': user.role,
        'createdAt': user.createdAt,
        'updatedAt': user.updatedAt,
    })


def login_page_view(request):
    return render(request, 'estoque/login.html')