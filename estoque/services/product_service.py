from estoque.models import Product, Category

def list_products():
    products = Product.objects.all()
    return products

def list_categories():
    categories = Category.objects.all()
    return categories

def create_product(data):
    catgory = Category.objects.get(id=data['categoryId'])
    return Product.objects.create(
        name=data.get('name'),
        description=data.get('description'),
        quatityStock=data.get('quatityStock'),
        costPrice=data.get('costPrice'),
        salePrice=data.get('salePrice'),
        categoryId=catgory
    )

def update_product(id, data):
    product = Product.objects.get(id=id)
    for key, value in data.items():
        setattr(product, key, value)
    product.save()
    return product

def delete_product(id):
    product = Product.objects.get(id=id)
    product.delete()
    return "Produto deletado com sucesso"