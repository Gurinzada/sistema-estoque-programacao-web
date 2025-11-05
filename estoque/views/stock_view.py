from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from estoque.services import stock_service
from django.views.decorators.csrf import csrf_exempt
import json

def serialize_movement(movement):
    return {
        "id": movement.id,
        "type": movement.type,
        "date": movement.date,
        "quantity": movement.quantity,
        "product": {
            "id": movement.product.id,
            "name": movement.product.name
        },
        "user": {
            "id": movement.user.id,
            "name": movement.user.name
        }
    }

@csrf_exempt
@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated])
def movement_list_create_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            movement = stock_service.create_movement(
                type=data.get('type'),
                product_id=data.get('product_id'),
                quantity=data.get('quantity'),
                user_id=request.user.id 
            )
            return Response(serialize_movement(movement), status=201)
        except Exception as e:
            return Response({'error': str(e)}, status=400)
    
    if request.method == 'GET':
        movements = stock_service.get_all_movements()
        serialized_movements = [serialize_movement(m) for m in movements]
        return Response(serialized_movements)

@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def movement_detail_view(request, movement_id):
    if request.method == 'GET':
        movement = stock_service.get_movement_by_id(movement_id)
        if movement:
            return Response(serialize_movement(movement))
        return Response({'error': 'Movimentação não encontrada'}, status=404)

    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            movement = stock_service.update_movement(
                movement_id=movement_id,
                new_type=data.get('type'),
                new_quantity=data.get('quantity')
            )
            return Response(serialize_movement(movement))
        except ValueError as e:
            return Response({'error': str(e)}, status=400)
        except Exception as e:
            return Response({'error': 'Erro ao atualizar movimentação'}, status=500)

    if request.method == 'DELETE':
        try:
            stock_service.delete_movement(movement_id)
            return Response(status=204)
        except ValueError as e:
            return Response({'error': str(e)}, status=400)
        except Exception as e:
            return Response({'error': 'Erro ao deletar movimentação'}, status=500)


@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_profit_out_view(request):
    profit = stock_service.get_profit_out()
    return Response({'profit': profit})

@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_out_and_in_view(request):
    total_in, total_out = stock_service.get_out_and_in()
    return Response({'total_in': total_in, 'total_out': total_out})