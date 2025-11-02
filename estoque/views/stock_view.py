from rest_framework.decorators import api_view
from rest_framework.response import Response
from estoque.services.stock_service import register_movement
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@api_view(['POST'])
def register_movement_view(request):
    try:
        movement = register_movement(
            type=request.data.get('type'),
            product_id=request.data.get('product_id'),
            quantity=request.data.get('quantity'),
            user_id=request.data.get('user_id'),
        )
        return Response({'message': 'Movimentação registrada', 'id': movement.id})
    except Exception as e:
        return Response({'error': str(e)}, status=400)
