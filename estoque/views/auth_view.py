from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from estoque.services import user_service, google_auth_service

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def login_email_view(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response({'error': 'Email and Password are required'}, status=400)
    
    result, status = user_service.authenticate_user(email=email, password=password)
    return Response(result, status=status)

@csrf_exempt
@api_view(['GET'])
@permission_classes([AllowAny])
def google_login_start_view(request):
    flow = google_auth_service.get_google_flow()
    authorization_url, state = flow.authorization_url()
    request.session['oauth_state'] = state
    return HttpResponseRedirect(authorization_url)

from django.contrib.auth import get_user_model

User = get_user_model()

@csrf_exempt
@api_view(['GET'])
@permission_classes([AllowAny])
def google_login_callback_view(request):
    """
    Handles the callback from Google after user authentication.
    """
    state = request.GET.get('state')
    if state != request.session.get('oauth_state'):
        return Response({'error': 'Invalid state parameter'}, status=400)

    code = request.GET.get('code')
    try:
        tokens = google_auth_service.handle_google_redirect_login(code)
        if tokens:
            # Redirect to the frontend login page with the token in the URL fragment
            access_token = tokens['access_token']
            login_url = reverse('login_page')
            return redirect(f'{login_url}#token={access_token}')
        else:
            return redirect(f"{reverse('login_page')}?error=auth_failed")
    except User.DoesNotExist:
        return redirect(f"{reverse('login_page')}?error=user_not_found")
    except Exception as e:
        return redirect(f"{reverse('login_page')}?error=generic_error")

@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user_view(request):
    user = request.user
    return Response({
        'id': user.id,
        'name': user.name,
        'jobTitle': user.jobTitle,
        'email': user.email,
        'role': user.role,
        'createdAt': user.createdAt.isoformat(),
        'updatedAt': user.updatedAt.isoformat(),
    })

def login_page_view(request):
    return render(request, 'estoque/login.html')
