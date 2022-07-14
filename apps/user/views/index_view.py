from chartjs.views import JSONView
from chartjs.views.columns import BaseColumnsHighChartsView
from chartjs.views.lines import BaseLineChartView, BaseLineOptionsChartView, HighchartPlotLineChartView
from django.db.models import Sum, F
from django.http import JsonResponse

from apps.order.models import SalesOrderLine


class LineChartMixin(BaseLineChartView):
    qs = None

    def get_labels(self):
        return [q['name'] for q in self.qs]

    def get_providers(self):
        return [q['total'] for q in self.qs]

    def get_data(self):
        return [[{"x": q['name'], "y": q['total']} for q in self.qs]]

    def get_options(self):
        return {"responsive": False}


class BaseColumnsChartMixin(BaseColumnsHighChartsView):
    qs = None

    def get_labels(self):
        return [q['name'] for q in self.qs]

    def get_providers(self):
        return [q['total'] for q in self.qs]

    def get_data(self):
        return [[{"x": q['name'], "y": q['total']} for q in self.qs]]

    def get_options(self):
        return {"responsive": False}


class MostPurchasedProductsChartJSONView(LineChartMixin):
    title = "Most Purchased Products"
    y_axis_title = "Most Purchased Products"
    subtitle = "In terms of Volume of sales"
    qs = SalesOrderLine.objects.all().annotate(name=F('product__name')).values('name').annotate(total=Sum('quantity')).order_by('-total')[:10]


class MostPurchasedProductsChartJSONView2(BaseColumnsChartMixin):
    title = "Most Purchased Products"
    y_axis_title = "Most Purchased Products"
    subtitle = "In terms of Volume of sales"
    qs = SalesOrderLine.objects.all().annotate(name=F('product__name')).values('name').annotate(total=Sum('quantity')).order_by('-total')[:10]
    yUnit = "Most Purchased Products"


# ======================================================================================================================================


class BaseBarChart(JSONView):
    qs = None
    label = None

    def get(self, request, *args, **kwargs):
        return JsonResponse({
            "type": 'bar',
            "data": self.get_data(),
            "options": {
                "indexAxis": 'y',
            }
        })

    def get_data(self):
        count = self.qs.count()
        return {
            "labels": {
                "count": count
            },
            "datasets": [{
                "axis": 'y',
                "label": self.label,
                "data": [q['total'] for q in self.qs],
                "fill": True,
                "backgroundColor": [
                                       'rgba(255, 205, 86, 0.2)',
                                       'rgba(255, 99, 132, 0.2)',
                                       'rgba(153, 102, 255, 0.2)',
                                       'rgba(255, 159, 64, 0.2)',
                                       'rgba(255, 205, 86, 0.2)',
                                       'rgba(75, 192, 192, 0.2)',
                                       'rgba(54, 162, 235, 0.2)',
                                       'rgba(255, 205, 86, 0.2)',
                                       'rgba(153, 102, 255, 0.2)',
                                       'rgba(201, 203, 207, 0.2)'
                                       'rgba(255, 205, 86, 0.2)',
                                   ][:count],
                "borderColor": [
                                   'rgb(255, 99, 132)',
                                   'rgb(153, 102, 255)',
                                   'rgb(255, 159, 64)',
                                   'rgb(255, 205, 86)',
                                   'rgb(75, 192, 192)',
                                   'rgb(255, 99, 132)',
                                   'rgb(54, 162, 235)',
                                   'rgb(153, 102, 255)',
                                   'rgb(201, 203, 207)'
                                   'rgb(255, 159, 64)',
                                   'rgb(75, 192, 192)',
                               ][:count],
                "borderWidth": 1
            }]
        }


class ProductPurchasedProductBarChart(BaseBarChart):
    label = "Most Purchased Products"
    # y_axis_title = "Most Purchased Products"
    # subtitle = "In terms of Volume of sales"
