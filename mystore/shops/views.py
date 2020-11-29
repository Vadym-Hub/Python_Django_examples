from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Product, Category
from cart.forms import CartAddProductForm


class ProductListView(ListView):
    """Список продуктів"""
    model = Product
#   categories = Category.objects.all()
    queryset = Product.objects.filter(available=True)


class ProductDetailView(DetailView):
    """Детальне описання продукту"""
    model = Product
    queryset = Product.objects.filter(available=True)
    slug_field = 'slug'
    cart_product_form = CartAddProductForm()
