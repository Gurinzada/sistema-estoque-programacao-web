from django.utils import timezone
from estoque.models import Product, MovementStock, User
from django.db import transaction

def create_movement(type, product_id, quantity, user_id):
    try:
        with transaction.atomic():
            product = Product.objects.get(id=product_id)
            user = User.objects.get(id=user_id)

            if type == 'SAIDA' and product.quatityStock < quantity:
                raise ValueError("Estoque insuficiente")
            
            if type == "ENTRADA":
                product.quatityStock += quantity
            else:
                product.quatityStock -= quantity

            product.save()

            movement = MovementStock.objects.create(
                type=type,
                date=timezone.now(),
                quantity=quantity,
                product=product,
                user=user
            )
            
            return movement
    except (Product.DoesNotExist, User.DoesNotExist, ValueError) as e:
        raise e

def get_all_movements():
    return MovementStock.objects.filter(deletedAt__isnull=True)

def get_movement_by_id(movement_id):
    try:
        return MovementStock.objects.get(id=movement_id, deletedAt__isnull=True)
    except MovementStock.DoesNotExist:
        return None

def update_movement(movement_id, new_type, new_quantity):
    try:
        with transaction.atomic():
            movement = MovementStock.objects.get(id=movement_id, deletedAt__isnull=True)
            product = movement.product

            if movement.type == 'ENTRADA':
                product.quatityStock -= movement.quantity
            else: 
                product.quatityStock += movement.quantity

            if new_type == 'ENTRADA':
                product.quatityStock += new_quantity
            else:
                if product.quatityStock < new_quantity:
                    raise ValueError("Estoque insuficiente para a nova quantidade de saída")
                product.quatityStock -= new_quantity
            
            product.save()

            movement.type = new_type
            movement.quantity = new_quantity
            movement.updatedAt = timezone.now()
            movement.save()

            return movement
    except MovementStock.DoesNotExist:
        raise ValueError("Movimentação não encontrada")
    except ValueError as e:
        raise e


def delete_movement(movement_id):
    try:
        with transaction.atomic():
            movement = MovementStock.objects.get(id=movement_id, deletedAt__isnull=True)
            product = movement.product
            if movement.type == 'ENTRADA':
                if product.quatityStock < movement.quantity:
                    raise ValueError("Estoque insuficiente para reverter a entrada")
                product.quatityStock -= movement.quantity
            else:
                product.quatityStock += movement.quantity
            
            product.save()

            movement.deletedAt = timezone.now()
            movement.save()
    except MovementStock.DoesNotExist:
        raise ValueError("Movimentação não encontrada")
    except ValueError as e:
        raise e

def get_profit_out():
    movements = MovementStock.objects.filter(type="SAIDA", deletedAt__isnull=True)
    total_profit = 0
    for movement in movements:
        total_profit += (movement.product.salePrice - movement.product.costPrice) * movement.quantity
    
    return total_profit

def get_out_and_in():
    movements = MovementStock.objects.filter(deletedAt__isnull=True)
    total_in = movements.filter(type="ENTRADA").count()
    total_out = movements.filter(type="SAIDA").count()
    return total_in, total_out
