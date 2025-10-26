from django.contrib import admin
from .models import User, Category, Product, MovementStock, Supplier

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'jobTitle',
        'role',
        'email',
        'createdAt',
        'updatedAt',
        'deletedAt',
    )
    list_display_links = ('id', 'name')
    search_fields = ('name', 'email', 'jobTitle')
    list_filter = ('role',)
    ordering = ('id',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'description',
    )
    list_display_links = ('id', 'name')
    search_fields = ('name', 'description')
    ordering = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'description',
        'quatityStock',   
        'costPrice',
        'salePrice',
        'categoryId',
        'createdAt',
        'updatedAt',
        'deletedAt',
    )
    list_display_links = ('id', 'name')
    list_editable = ('salePrice', 'quatityStock')
    search_fields = ('name', 'description')
    list_filter = ('categoryId',)
    ordering = ('id',)

@admin.register(MovementStock)
class MovementStockAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'type',
        'date',
        'quantity',
        'produto_resumido',
        'usuario_resumido',
        'createdAt',
        'updatedAt',
        'deletedAt',
    )
    list_display_links = ('id', 'type')
    list_filter = ('type', 'user', 'product')
    search_fields = ('product__name', 'user__name')
    ordering = ('-date',)

    def produto_resumido(self, obj):
        return f"ID: {obj.product.id} - {obj.product.name}"
    produto_resumido.short_description = 'Product'

    def usuario_resumido(self, obj):
        return f"ID: {obj.user.id} - {obj.user.name}"
    usuario_resumido.short_description = 'User'



@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'cnpj',
        'email',
        'phone',
        'address',
        'zipCode',
        'createdAt',
        'updatedAt',
        'deletedAt',
    )
    list_display_links = ('id', 'name')
    search_fields = ('name', 'cnpj', 'email')
    list_filter = ('products',)
    ordering = ('name',)
