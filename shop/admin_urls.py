from django.urls import path
from . import admin_views
from . import views


urlpatterns = [
    path('login/', admin_views.admin_login, name='admin_login'),
    path('', admin_views.admin_dashboard, name='admin_dashboard'),

    path('add-product/', admin_views.add_product, name='add_product'),
    path('delete-product/<int:product_id>/', admin_views.delete_product, name='delete_product'),
    path('update-product/<int:product_id>/', admin_views.update_product, name='update_product'),

    path('view-product/', admin_views.view_products, name='view_products'),



]
