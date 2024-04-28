from django.urls import path

from product.api import views


urlpatterns = [
    # Get API's
    path("list-filter", views.ProductFilterAPIView.as_view(), name="product_list"),
    path("get-categories", views.CategoryListView.as_view(), name="category_list"),
    path("product/<int:id>", views.ProductRetrieveView.as_view(), name="get_product"),
    path("category/<int:id>", views.CategoryRetrieveView.as_view(), name="get_category"),


    # Post API's
    path("create-category", views.CategoryCreateView.as_view(), name="category_create"),
    path("create-product", views.ProductCreateView.as_view(), name="product_create"),

    # Delete API's
    path("remove-product/<int:id>", views.ProductDeleteView.as_view(), name="delete_product"),
    path("remove-category/<int:id>", views.CategoryDeleteView.as_view(), name="delete_category"),
]
