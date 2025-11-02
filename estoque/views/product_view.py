from rest_framework.decorators import api_view
from rest_framework.response import Response
from estoque.services import product_service
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
@api_view(['GET'])
def list_products_view(request):
    products = product_service.list_products()
    return Response(products)

@csrf_exempt
@api_view(['GET'])
def list_categories_view(request):
    categories = product_service.list_categories()
    return Response(categories)

@csrf_exempt
@api_view(['POST'])
def create_product_view(request):
    product = product_service.create_product(request.data)
    return Response(product)

@csrf_exempt
@api_view(['PATCH'])
def update_product_view(request, id):
    product = product_service.update_product(id, request.data)
    return Response(product)

@csrf_exempt
@api_view(['DELETE'])
def delete_product_view(request, id):
    message = product_service.delete_product(id)
    return Response(message)