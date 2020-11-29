from .cart import Cart


def cart(request):
    """Контекст запросу, який видно у віх шаблонах"""
    return {'cart': Cart(request)}
