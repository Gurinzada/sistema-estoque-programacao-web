from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from estoque.services import supplier_service
from django.views.decorators.csrf import csrf_exempt
import json

def serialize_supplier(s):
    return {
        'id': s.id,
        'name': s.name,
        'cnpj': s.cnpj,
        'email': s.email,
        'phone': s.phone
    }

@csrf_exempt
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def suppliers_view(request):
    if request.method == 'GET':
        suppliers = supplier_service.list_suppliers()
        data = [serialize_supplier(s) for s in suppliers]
        return Response(data)
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            supplier = supplier_service.create_supplier(data)
            return Response(serialize_supplier(supplier), status=201)
        except Exception as e:
            return Response({'error': str(e)}, status=400)
