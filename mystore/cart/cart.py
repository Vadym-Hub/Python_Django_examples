from decimal import Decimal
from django.conf import settings
from shops.models import Product


class Cart(object):
    """Кошик"""

    def __init__(self, request):
        """Ініціалізація кошику"""
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # Створення сессії с пустим кошиком
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, update_quantity=False):
        """Добавити продукт в кошик, або оновити його кількість"""
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        """Зберегти корзину в сессії"""
        # Оновлення сессії cart
        self.session[settings.CART_SESSION_ID] = self.cart
        # Відмітити сеанс як "змінений", щоб запевнитись, що його збережено
        self.session.modified = True

    def remove(self, product):
        """Видалення продукту с корзини"""
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """Перебор елементів в кошику та отримання продуктів із бази данних"""
        product_ids = self.cart.keys()
        # Отримання обєктів product та їх додавання в кошик
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """Підрахунок всіх товарів в кошику"""
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """Підрахунок вартості товарів в кошику"""
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        """Очистка сеансу"""
        # Видалення кошику із сессії
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
