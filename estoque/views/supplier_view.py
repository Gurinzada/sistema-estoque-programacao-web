from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from estoque.services import supplier_service
from django.views.decorators.csrf import csrf_exempt
import json
from django.shortcuts import render

def serialize_supplier(supplier):
    return {
        'id': supplier.id,
        'name': supplier.name,
        'cnpj': supplier.cnpj,
        'email': supplier.email,
        'phone': supplier.phone,
        'address': supplier.address,
        'zipCode': supplier.zipCode,
        'products': [p.id for p in supplier.products.all()]
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

@csrf_exempt
@api_view(['GET', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def supplier_detail_view(request, id):
    supplier = supplier_service.get_supplier_by_id(id)
    if not supplier:
        return Response({'error': 'Fornecedor não encontrado'}, status=404)

    if request.method == 'GET':
        return Response(serialize_supplier(supplier))

    if request.method == 'PATCH':
        try:
            data = json.loads(request.body)
            updated_supplier = supplier_service.update_supplier(id, data)
            return Response(serialize_supplier(updated_supplier))
        except Exception as e:
            return Response({'error': str(e)}, status=400)

    if request.method == 'DELETE':
        try:
            supplier_service.delete_supplier(id)
            return Response(status=204)
        except Exception as e:
            return Response({'error': str(e)}, status=400)
        
def supplier_template_view(request):
    return render(request, 'estoque/suppliers.html')