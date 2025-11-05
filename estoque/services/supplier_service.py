from estoque.models import Supplier, Product
from django.utils import timezone

def list_suppliers():
    return Supplier.objects.filter(deletedAt__isnull=True)

def get_supplier_by_id(supplier_id):
    try:
        return Supplier.objects.get(id=supplier_id, deletedAt__isnull=True)
    except Supplier.DoesNotExist:
        return None

def create_supplier(data):
    supplier = Supplier.objects.create(
        name=data.get('name'),
        cnpj=data.get('cnpj'),
        email=data.get('email'),
        phone=data.get('phone'),
        address=data.get('address'),
        zipCode=data.get('zipCode'),
    )
    if product_ids := data.get('products'):
        products = Product.objects.filter(id__in=product_ids)
        supplier.products.set(products)
    return supplier

def update_supplier(supplier_id, data):
    supplier = get_supplier_by_id(supplier_id)
    if not supplier:
        return None

    for key, value in data.items():
        if key != 'products':
            setattr(supplier, key, value)
    
    if product_ids := data.get('products'):
        products = Product.objects.filter(id__in=product_ids)
        supplier.products.set(products)
    
    supplier.save()
    return supplier

def delete_supplier(supplier_id):
    supplier = get_supplier_by_id(supplier_id)
    if not supplier:
        return None
    
    supplier.deletedAt = timezone.now()
    supplier.save()
    return supplier