from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import User, Category, Product, MovementStock, Supplier

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'jobTitle', 'role', 'createdAt')
    list_filter = ('role', 'createdAt')
    search_fields = ('email', 'name', 'jobTitle')
    ordering = ('-createdAt',)
    readonly_fields = ('createdAt', 'updatedAt')
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Informações Pessoais', {'fields': ('name', 'jobTitle', 'role')}),
        ('Datas Importantes', {'fields': ('createdAt', 'updatedAt', 'deletedAt')}),
    )
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        return form

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'product_count', 'description')
    list_filter = ('name', 'description')
    search_fields = ('name', 'description')
    
    def product_count(self, obj):
        return obj.products.count()
    product_count.short_description = 'Nº de Produtos'

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'stock_status', 'cost_price', 'sale_price', 'profit_margin', 'createdAt')
    list_filter = ('categoryId', 'createdAt')
    search_fields = ('name', 'description', 'categoryId__name')
    readonly_fields = ('createdAt', 'updatedAt', 'profit_margin')
    
    def category(self, obj):
        return obj.categoryId.name
    category.short_description = 'Categoria'
    
    def cost_price(self, obj):
        return f"R$ {obj.costPrice}"
    cost_price.short_description = 'Custo'
    
    def sale_price(self, obj):
        return f"R$ {obj.salePrice}"
    sale_price.short_description = 'Venda'
    
    def stock_status(self, obj):
        if obj.quatityStock <= 0:
            color = 'red'
            status = 'ESGOTADO'
        elif obj.quatityStock < 10:
            color = 'orange'
            status = f'BAIXO ({obj.quatityStock})'
        else:
            color = 'green'
            status = f'OK ({obj.quatityStock})'
        return format_html('<span style="color: {}; font-weight: bold;">{}</span>', color, status)
    stock_status.short_description = 'Estoque'
    
    def profit_margin(self, obj):
        if obj.costPrice > 0 and obj.salePrice > 0:
            margin = ((obj.salePrice - obj.costPrice) / obj.costPrice) * 100
            color = 'green' if margin > 0 else 'red'
            return format_html('<span style="color: {};">{}%</span>', color, f"{margin:.1f}")
        return "0%"
    profit_margin.short_description = 'Margem'

    fieldsets = (
        ('Informações Básicas', {
            'fields': ('name', 'description', 'categoryId')
        }),
        ('Estoque e Preços', {
            'fields': ('quatityStock', 'costPrice', 'salePrice', 'profit_margin')
        }),
        ('Metadados', {
            'fields': ('createdAt', 'updatedAt', 'deletedAt'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'cnpj', 'contact_email', 'phone', 'product_count', 'createdAt')
    list_filter = ('createdAt',)
    search_fields = ('name', 'cnpj', 'email', 'phone')
    readonly_fields = ('createdAt', 'updatedAt')
    filter_horizontal = ('products',)
    
    def contact_email(self, obj):
        return obj.email
    contact_email.short_description = 'Email'
    
    def product_count(self, obj):
        return obj.products.count()
    product_count.short_description = 'Nº Produtos'

    fieldsets = (
        ('Informações do Fornecedor', {
            'fields': ('name', 'cnpj', 'email', 'phone', 'address', 'zipCode')
        }),
        ('Produtos Fornecidos', {
            'fields': ('products',)
        }),
        ('Metadados', {
            'fields': ('createdAt', 'updatedAt', 'deletedAt'),
            'classes': ('collapse',)
        }),
    )

@admin.register(MovementStock)
class MovementStockAdmin(admin.ModelAdmin):
    list_display = ('product', 'movement_type_colored', 'quantity', 'user', 'movement_date', 'createdAt')
    list_filter = ('type', 'createdAt', 'user')
    search_fields = ('product__name', 'user__name')
    readonly_fields = ('createdAt', 'updatedAt')
    date_hierarchy = 'date'
    
    def movement_type_colored(self, obj):
        color = 'green' if obj.type == 'ENTRADA' else 'red'
        icon = '⬆️' if obj.type == 'ENTRADA' else '⬇️'
        return format_html(
            '<span style="color: {}; font-weight: bold;">{} {}</span>', 
            color, icon, obj.get_type_display()
        )
    movement_type_colored.short_description = 'Tipo'
    
    def movement_date(self, obj):
        return obj.date.strftime('%d/%m/%Y %H:%M')
    movement_date.short_description = 'Data Mov.'
    
    def created_at(self, obj):
        return obj.createdAt.strftime('%d/%m/%Y %H:%M')
    created_at.short_description = 'Criado em'

    fieldsets = (
        ('Movimentação', {
            'fields': ('product', 'type', 'quantity', 'date', 'user')
        }),
        ('Metadados', {
            'fields': ('createdAt', 'updatedAt', 'deletedAt'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('product', 'user')
    
    def get_changeform_initial_data(self, request):
        initial = super().get_changeform_initial_data(request)
        initial['user'] = request.user
        return initial

def update_product_stock(modeladmin, request, queryset):
    for product in queryset:
        product.quatityStock += 10
        product.save()
    modeladmin.message_user(request, f"Estoque de {queryset.count()} produtos atualizado com +10 unidades.")
update_product_stock.short_description = "Adicionar 10 unidades ao estoque"

def reset_product_stock(modeladmin, request, queryset):
    for product in queryset:
        product.quatityStock = 0
        product.save()
    modeladmin.message_user(request, f"Estoque de {queryset.count()} produtos zerado.")
reset_product_stock.short_description = "Zerar estoque dos produtos"

ProductAdmin.actions = [update_product_stock, reset_product_stock]