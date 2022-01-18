import os

from django.conf import settings
from django.core.cache import cache
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from django.views.decorators.cache import never_cache
from django.views.generic import DetailView

from mainapp.models import Products, ProductCategory

# Create your views here.

MODULE_DIR = os.path.dirname(__file__)
def get_link_category():
    if settings.LOW_CACHE:
        key = 'link_category'
        link_category = cache.get(key)
        if link_category is None:
            link_category = ProductCategory.objects.all()
            cache.set(key,link_category)
        return link_category
    else:
        return ProductCategory.objects.all()

def get_link_product():
    if settings.LOW_CACHE:
        key = 'link_product'
        link_product = cache.get(key)
        if link_product is None:
            link_product = Products.objects.all().select_related('category')
            cache.set(key,link_product)
        return link_product
    else:
        return Products.objects.all().select_related('category')


def get_product(pk):
    if settings.LOW_CACHE:
        key = f'product{pk}'
        product = cache.get(key)
        if product is None:
            product = Products.objects.get(id=pk)
            cache.set(key,product)
        return product
    else:
        return Products.objects.get(id=pk)


def index(request):
    context = {
        'title': 'geekshop',
    }
    return render(request, 'mainapp/index.html', context)

@never_cache
def products(request, id_category=None, page=1):
    # context = {
    #     'products' : [
    #         {
    #             'name':'Худи черного цвета с монограммами adidas Originals', 'price':'6 090,00 руб.', 'image' : 'vendor/img/products/Adidas-hoodie.png', 'cardtext' : 'Мягкая ткань для свитшотов. Стиль и комфорт – это образ жизни.'
    #         },
    #         {
    #             'name': 'Синяя куртка The North Face', 'price': '23 725,00 руб.', 'image': 'vendor/img/products/Blue-jacket-The-North-Face.png', 'cardtext': 'Гладкая ткань. Водонепроницаемое покрытие. Легкий и теплый пуховый наполнитель.'
    #         },
    #         {
    #             'name': 'Коричневый спортивный oversized-топ ASOS DESIGN', 'price': '3 390,00 руб.', 'image': 'vendor/img/products/Brown-sports-oversized-top-ASOS-DESIGN.png', 'cardtext': 'Материал с плюшевой текстурой. Удобный и мягкий.'
    #         },
    #         {
    #             'name': 'Черный рюкзак Nike Heritage', 'price': '2 340,00 руб.', 'image': 'vendor/img/products/Black-Nike-Heritage-backpack.png', 'cardtext': 'Плотная ткань. Легкий материал.'
    #         },
    #         {
    #             'name': 'Черные туфли на платформе с 3 парами люверсов Dr Martens 1461 Bex', 'price': '13 590,00 руб.', 'image': 'vendor/img/products/Black-Dr-Martens-shoes.png', 'cardtext': 'Гладкий кожаный верх. Натуральный материал.'
    #         },
    #         {
    #             'name': 'Темно-синие широкие строгие брюки ASOS DESIGN', 'price': '2 890,00 руб.', 'image': 'vendor/img/products/Dark-blue-wide-leg-ASOs-DESIGN-trousers.png', 'cardtext': 'Легкая эластичная ткань сирсакер Фактурная ткань.'
    #         },
    #     ],
    #     'title' : 'GeekShop - Каталог',
    # }
    context = {'title': 'Geekshop | Каталог'}
    if id_category and id_category != 9:
        products = Products.objects.filter(category_id=id_category).select_related('category')
    elif id_category == 9:
        products = Products.objects.all().select_related('category')
    else:
        products = Products.objects.all().select_related('category')
    paginator = Paginator(products, per_page=3)

    try:
        products_paginator = paginator.page(page)
    except PageNotAnInteger:
        products_paginator = paginator.page(1)
    except EmptyPage:
        products_paginator = paginator.page(paginator.num_pages)

    context['products'] = products_paginator
    context['categories'] = ProductCategory.objects.all()
    return render(request, 'mainapp/products.html', context)


class ProductDetail(DetailView):
    model = Products
    template_name = 'mainapp/detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super(ProductDetail, self).get_context_data(**kwargs)
        product = self.get_object()
        context['product'] = product
        return context
