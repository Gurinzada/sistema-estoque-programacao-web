from rest_framework.decorators import api_view
from rest_framework.response import Response
from estoque.services import supplier_service
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated


@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_suppliers_view(request):
    suppliers = supplier_service.list_suppliers()
    data = [{
        'id': s.id,
        'name': s.name,
        'cnpj': s.cnpj,
        'email': s.email,
        'phone': s.phone
    } for s in suppliers]
    return Response(data)

@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_supplier_view(request):
    supplier = supplier_service.create_supplier(request.data)
    return Response({'message': 'Fornecedor criado', 'id': supplier.id})
