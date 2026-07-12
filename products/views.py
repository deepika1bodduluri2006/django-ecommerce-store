from django.shortcuts import render, get_object_or_404
from .models import Product


def product_list(request):

    products = Product.objects.all()

    query = request.GET.get('q')

    category = request.GET.get('category')

    if query:
        products = products.filter(name__icontains=query)

    if category:
        products = products.filter(category=category)

    context = {
        'products': products,
        'query': query,
        'selected_category': category,
    }

    return render(request, 'products/product_list.html', context)


def product_detail(request, pk):

    product = get_object_or_404(Product, pk=pk)

    return render(
        request,
        'products/product_detail.html',
        {'product': product}
    )