from django.shortcuts import render
from semantic_ui.models import ItemInfo, last_pub_date
from django.core.paginator import Paginator
# Create your views here.


def base(request):
    return render(request, 'base.html')


def data(request):
    limit = 10
    item_info = ItemInfo.objects
    paginator = Paginator(item_info, limit)
    page = request.GET.get('page', 1)
    loaded = paginator.page(page)
    item_info = {
        'loaded': loaded,
        'counts': item_info.count(),
        'last_date': last_pub_date[0]

    }
    print(item_info)
    return render(request, 'data.html', item_info)


def chart(request):
    return render(request, 'charts.html')
