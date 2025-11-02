from django.utils import timezone
from estoque.models import Product, MovementStock, User

def register_movement(type, product_id, quantity, user_id):
    product = Product.objects.get(id=product_id)
    user = User.objects.get(id=user_id)

    if type == 'SAIDA' and product.quatityStock < quantity:
        raise ValueError("Estoque insuficiente")
    
    if type == "ENTRADA":
        product.quatityStock +=quantity
    else:
        product.quatityStock -=quantity

    product.save()

    movement = MovementStock.objects.create(
        type=type,
        date=timezone.now(),
        quantity=quantity,
        product=product,
        user=user
    )
    
    return movement