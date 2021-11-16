from django.shortcuts import render

# Create your views here.
def index(request):
    context = {
        'title':'geekshop',
    }
    return render(request, 'mainapp\index.html', context)

def products(request):
    context = {
        'products' : [
            {
                'name':'Худи черного цвета с монограммами adidas Originals', 'price':'6 090,00 руб.', 'image' : 'vendor/img/products/Adidas-hoodie.png', 'cardtext' : 'Мягкая ткань для свитшотов. Стиль и комфорт – это образ жизни.'
            },
            {
                'name': 'Синяя куртка The North Face', 'price': '23 725,00 руб.', 'image': 'vendor/img/products/Blue-jacket-The-North-Face.png', 'cardtext': 'Гладкая ткань. Водонепроницаемое покрытие. Легкий и теплый пуховый наполнитель.'
            },
            {
                'name': 'Коричневый спортивный oversized-топ ASOS DESIGN', 'price': '3 390,00 руб.', 'image': 'vendor/img/products/Brown-sports-oversized-top-ASOS-DESIGN.png', 'cardtext': 'Материал с плюшевой текстурой. Удобный и мягкий.'
            },
            {
                'name': 'Черный рюкзак Nike Heritage', 'price': '2 340,00 руб.', 'image': 'vendor/img/products/Black-Nike-Heritage-backpack.png', 'cardtext': 'Плотная ткань. Легкий материал.'
            },
            {
                'name': 'Черные туфли на платформе с 3 парами люверсов Dr Martens 1461 Bex', 'price': '13 590,00 руб.', 'image': 'vendor/img/products/Black-Dr-Martens-shoes.png', 'cardtext': 'Гладкий кожаный верх. Натуральный материал.'
            },
            {
                'name': 'Темно-синие широкие строгие брюки ASOS DESIGN', 'price': '2 890,00 руб.', 'image': 'vendor/img/products/Dark-blue-wide-leg-ASOs-DESIGN-trousers.png', 'cardtext': 'Легкая эластичная ткань сирсакер Фактурная ткань.'
            },
        ],
        'title' : 'GeekShop - Каталог',
    }
    return render(request, 'mainapp\products.html', context)
