from django.urls import path
from .views import ProductCreate, ProductDetail, ProductList

urlpatterns = [
    path("products/", ProductList.as_view()),
    path("products/create/", ProductCreate.as_view()),
    path("products/<int:product_id>/", ProductDetail.as_view()),
]