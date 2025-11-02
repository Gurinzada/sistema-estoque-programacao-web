from estoque.models import Supplier, Product

def list_suppliers():
    return Supplier.objects.all()

def create_supplier(data):
    supplier = Supplier.objects.create(
        name=data.get('name'),
        cnpj=data.get('cnpj'),
        email=data.get('email'),
        phone=data.get('phone'),
        address=data.get('address'),
        zipCode=data.get('zipCode'),
    )
    if products := data.get('products'):
        supplier.products.set(Product.objects.filter(id__in=products))
    return supplier
