from rest_framework.decorators import api_view
from rest_framework.response import Response
from estoque.services.stock_service import register_movement, get_profit_out, get_out_and_in
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
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

@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_profit_out_view(request):
    profit = get_profit_out()
    return Response({'profit': profit})

@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_out_and_in_view(request):
    total_in, total_out = get_out_and_in()
    return Response({'total_in': total_in, 'total_out': total_out})