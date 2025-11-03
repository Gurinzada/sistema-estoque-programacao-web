from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from estoque.services import product_service
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated


@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_products_view(request):
    products = product_service.list_products() 
    products_data = []
    for p in products:
        products_data.append({
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
        })

    return Response(products_data)

@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_categories_view(request):
    categories = product_service.list_categories()
    return Response(categories)

@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_product_view(request):
    product = product_service.create_product(request.data)
    return Response(product)

@csrf_exempt
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_product_view(request, id):
    product = product_service.update_product(id, request.data)
    return Response(product)

@csrf_exempt
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_product_view(request, id):
    message = product_service.delete_product(id)
    return Response(message)

@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def count_products_by_categories_view(request):
    count = product_service.count_products_by_categories()
    return Response(count)


def dashboard_view(request):
    return render(request, 'estoque/dashboard.html')

def products_view(request):
    return render(request, 'estoque/products.html')