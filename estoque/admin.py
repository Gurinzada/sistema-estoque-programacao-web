from django.contrib import admin
from .models import User, Category, Product, MovementStock, Supplier

# Register your models here.
admin.site.register(User)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(MovementStock)
admin.site.register(Supplier)

