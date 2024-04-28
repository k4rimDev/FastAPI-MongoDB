from django.urls import path

from product.api import views


urlpatterns = [
    path("", views, name="product_list")
]
