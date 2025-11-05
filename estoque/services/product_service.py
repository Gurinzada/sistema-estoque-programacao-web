from estoque.models import Product, Category
from django.db.models import Count

def list_products():
    products = Product.objects.all()
    return products

def list_categories():
    categories = Category.objects.all()
    return categories

def create_category(data):
    return Category.objects.create(
        name=data.get('name'),
        description=data.get('description')
    )

def update_category(id, data):
    category = Category.objects.get(id=id)
    for key, value in data.items():
        setattr(category, key, value)
    category.save()
    return category

def delete_category(id):
    category = Category.objects.get(id=id)
    category.delete()
    return "Categoria deletada com sucesso"

def get_product_by_id(id):
    return Product.objects.get(id=id)

def get_category_by_id(id):
    return Category.objects.get(id=id)


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

def count_products_by_categories():
    categories = (
        Category.objects
        .annotate(total_products=Count('products'))
        .values('name', 'total_products')
    )
    
    return {cat['name']: cat['total_products'] for cat in categories}
