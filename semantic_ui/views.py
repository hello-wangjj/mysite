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
    return render(request, 'data.html', item_info)


# 获取不同地区的发帖量前三名
def top_x(date1, date2, area, limit):
    pipeline = [
        {'$match': {'$and': [{'pub_date': {'$gt': date1, '$lt': date2}}, {'area': {'$all': area}}]}},
        {'$group': {'_id': {'$slice': ['$cates', 2, 1]}, 'counts': {'$sum': 1}}},
        {'$sort': {'counts': -1}},
        {'$limit': limit}
    ]
    for i in ItemInfo._get_collection().aggregate(pipeline):
        data = {
            'name': i['_id'][0],
            'data': [i['counts']],
            # 'type': 'column'
        }
        yield data

series_CY = [i for i in top_x('2015.12.25', '2016.01.10', ['朝阳'], 3)]
series_TZ = [i for i in top_x('2015.12.25', '2016.01.10', ['通州'], 3)]
series_HD = [i for i in top_x('2015.12.25', '2016.01.10', ['海淀'], 3)]


# 各类目的发帖量对比
def top_cates():
    pipeline = [
        {'$group': {'_id': {'$slice': ['$cates', 2, 1]}, 'counts': {'$sum': 1}}}
    ]
    for i in ItemInfo._get_collection().aggregate(pipeline):
        data = {
            'name': i['_id'][0],
            'y': i['counts'],
        }
        yield data

series_ALL = [i for i in top_cates()]

# 给地区的发帖量
def top_area():
    pipeline = [
        {'$group': {'_id': {'$slice': ['$area', 1]}, 'counts':{'$sum': 1}}},
        {'$sort': {'counts': -1}}
    ]
    for i in ItemInfo._get_collection().aggregate(pipeline):
        data = {
            'name': i['_id'][0],
            'y': i['counts']
        }
        yield data
xAxis_all = [i['name'] for i in top_area()]
data_all = [i['y'] for i in top_area()]

#分布
def cate_distributed():
    pipeline = [
        {'$group': {'_id': {'$slice': ['$cates', 2, 1]}, 'counts': {'$sum': 1}}},
        {'$sort': {'counts': -1}}
    ]
    for i in ItemInfo._get_collection().aggregate(pipeline):
        yield [i['_id'][0], i['counts']]

cate_distributed = [i for i in cate_distributed()]


def sale_one_day():
    pipeline = [
        {'$match': {'time': 1}},
        {'$group': {'_id': {'$slice': ['$area', 1]}, 'counts': {'$sum': 1}}},
        {'$sort': {'counts': -1}}
    ]
    for i in ItemInfo._get_collection().aggregate(pipeline):
        yield [i['_id'][0], i['counts']]

sale_distributed = [i for i in sale_one_day()]


def chart(request):
    context = {
        'chart_CY': series_CY,
        'chart_TZ': series_TZ,
        'chart_HD': series_HD,
        'chart_ALL': series_ALL,
        'xAxis_All': xAxis_all,
        'data_all': data_all,
        'cate_distributed': cate_distributed,
        'sale_distributed': sale_distributed
    }
    return render(request, 'charts.html', context)
