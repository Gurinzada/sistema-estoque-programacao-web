from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from estoque.services import product_service
from django.views.decorators.csrf import csrf_exempt
import json

def serialize_product(p):
    return {
        'id': p.id,
        'name': p.name,
        'description': p.description,
        'quatityStock': p.quatityStock,
        'costPrice': float(p.costPrice),
        'salePrice': float(p.salePrice),
        'createdAt': p.createdAt.isoformat(),
        'updatedAt': p.updatedAt.isoformat(),
        'deletedAt': p.deletedAt.isoformat() if p.deletedAt else None,
        'categoryId': p.categoryId.id,
        'categoryName': p.categoryId.name
    }

def serialize_category(c):
    return {
        'id': c.id,
        'name': c.name,
        'description': c.description
    }

@csrf_exempt
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def products_view(request):
    if request.method == 'GET':
        products = product_service.list_products()
        products_data = [serialize_product(p) for p in products]
        return Response(products_data)
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            product = product_service.create_product(data)
            return Response(serialize_product(product), status=201)
        except Exception as e:
            return Response({'error': str(e)}, status=400)

@csrf_exempt
@api_view(['GET', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def product_detail_view(request, id):
    if request.method == 'GET':
        product = product_service.get_product_by_id(id)
        if product:
            return Response(serialize_product(product))
        return Response({'error': 'Produto não encontrado'}, status=404)

    if request.method == 'PATCH':
        try:
            data = json.loads(request.body)
            product = product_service.update_product(id, data)
            return Response(serialize_product(product))
        except Exception as e:
            return Response({'error': str(e)}, status=400)

    if request.method == 'DELETE':
        try:
            product_service.delete_product(id)
            return Response(status=204)
        except Exception as e:
            return Response({'error': str(e)}, status=400)

@csrf_exempt
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def categories_view(request):
    if request.method == 'GET':
        categories = product_service.list_categories()
        serialized_categories = [serialize_category(c) for c in categories]
        return Response(serialized_categories)
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            category = product_service.create_category(data)
            return Response(serialize_category(category), status=201)
        except Exception as e:
            return Response({'error': str(e)}, status=400)

@csrf_exempt
@api_view(['GET', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def category_detail_view(request, id):
    if request.method == 'GET':
        category = product_service.get_category_by_id(id)
        if category:
            return Response(serialize_category(category))
        return Response({'error': 'Categoria não encontrada'}, status=404)

    if request.method == 'PATCH':
        try:
            data = json.loads(request.body)
            category = product_service.update_category(id, data)
            return Response(serialize_category(category))
        except Exception as e:
            return Response({'error': str(e)}, status=400)

    if request.method == 'DELETE':
        try:
            product_service.delete_category(id)
            return Response(status=204)
        except Exception as e:
            return Response({'error': str(e)}, status=400)


@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def count_products_by_categories_view(request):
    count = product_service.count_products_by_categories()
    return Response(count)

def dashboard_view(request):
    return render(request, 'estoque/dashboard.html')

def products_templates_view(request):
    return render(request, 'estoque/stock.html')
