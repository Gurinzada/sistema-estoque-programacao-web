from django.urls import path
from estoque.views import auth_view, product_view, supplier_view, stock_view, user_view

urlpatterns = [
    path('login-page', auth_view.login_page_view, name='login_page'),
    path('login', auth_view.login_email_view),
    path('login/google', auth_view.google_login_start_view, name='google_login_start'),
    path('login/google/callback', auth_view.google_login_callback_view, name='google_login_callback'),
    path('me',  auth_view.current_user_view),

    path('users', user_view.users_view),
    path('users/<int:id>', user_view.user_detail_view),

    path('products', product_view.products_view),
    path('products/<int:id>', product_view.product_detail_view),
    path('products/count', product_view.count_products_by_categories_view),

    path('category', product_view.categories_view),
    path('category/<int:id>', product_view.category_detail_view),

    path('suppliers', supplier_view.suppliers_view),

    path('stock/movements', stock_view.movement_list_create_view),
    path('stock/movements/<int:movement_id>', stock_view.movement_detail_view),
    path('stock/profit', stock_view.get_profit_out_view),
    path('stock/out-and-in', stock_view.get_out_and_in_view),
]
