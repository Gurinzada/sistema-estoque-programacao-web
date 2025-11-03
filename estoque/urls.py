from django.urls import path
from estoque.views import auth_view, product_view, supplier_view, stock_view

urlpatterns = [
    path('login', auth_view.login_email_view),
    path('login/google', auth_view.login_google_view),
    path('me',  auth_view.current_user_view),

    path('products', product_view.list_products_view),
    path('products', product_view.create_product_view),
    path('products/<int:id>', product_view.update_product_view),
    path('products/<int:id>', product_view.delete_product_view),
    path('products/count', product_view.count_products_by_categories_view),
    

    path('suppliers', supplier_view.list_suppliers_view),
    path('suppliers', supplier_view.create_supplier_view),

    path('category', product_view.list_categories_view),

    path('stock', stock_view.register_movement_view),
    path('stock/profit', stock_view.get_profit_out_view),
    path('stock/out-and-in', stock_view.get_out_and_in_view),
]
