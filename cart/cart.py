from decimal import Decimal
from django.conf import settings

from catalog.models import Products, Services


class Cart(object):
    def __init__(self, request):
        """Инициализация объекта корзины."""
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # Сохраняем в сессии пустую корзину.
            cart = self.session[settings.CART_SESSION_ID] = {
                'product': {},
                'service': {}
            }
        self.cart = cart

    def __iter__(self):
        """Проходим по товарам корзины и получаем соответствующие объекты Product."""
        product_ids = self.cart['product'].keys()
        services_ids = self.cart['service'].keys()
        # получение объектов products, services и добавление их в корзину
        products = Products.objects.filter(id__in=product_ids)
        services = Services.objects.filter(id__in=services_ids)

        cart = self.cart.copy()

        for product in products:
            cart['product'][str(product.id)]['product'] = product
        for service in services:
            cart['service'][str(service.id)]['service'] = service

        for type_tov in ['product', 'service']:
            for item in cart[type_tov].values():
                if type_tov == 'product':
                    item['type_tov'] = 1
                else:
                    item['type_tov'] = 2
                item['price'] = Decimal(item['price'])
                item['total_price'] = item['price'] * item['quantity']
                yield item




    def product_add(self, product, quantity=1, update_quantity=False):
        """Добавление товара в корзину или обновление его количества."""
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart['product'][product_id] = {'quantity': 0, 'price': str(product.price)}
        if update_quantity:
            self.cart['product'][product_id]['quantity'] = quantity
        else:
            self.cart['product'][product_id]['quantity'] += quantity
        self.save()

    def service_add(self, service, quantity=1, update_quantity=False):
        """Добавление услуги в корзину или обновление его количества."""
        service_id = str(service.id)
        if service_id not in self.cart:
            self.cart['service'][service_id] = {'quantity': 0, 'price': str(service.price)}
        if update_quantity:
            self.cart['service'][service_id]['quantity'] = quantity
        else:
            self.cart['service'][service_id]['quantity'] += quantity
        self.save()

    def product_remove(self, product):
        """Удаление товара из корзины."""
        product_id = str(product.id)
        if product_id in self.cart['product']:
            del self.cart['product'][product_id]
        self.save()

    def service_remove(self, product):
        """Удаление товара из корзины."""
        product_id = str(product.id)
        if product_id in self.cart['service']:
            del self.cart['service'][product_id]
        self.save()

    def save(self):
        # Помечаем сессию как измененную
        self.session.modified = True

    def clear(self):
        # Очистка корзины.
        del self.session[settings.CART_SESSION_ID]
        self.save()