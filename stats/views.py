from django.shortcuts import get_object_or_404, render, redirect
from .models import Statistic
from faker import Faker
from django.http import JsonResponse
from django.db.models import Sum
# Create your views here.

fake = Faker()


def main(request):
    qs = Statistic.objects.all()
    if request.method == 'POST':
        new_stat = request.POST.get('new-statitocs')
        obj, created = Statistic.objects.get_or_create(new=new_stat)
        return redirect("stats:dashboard", slug=obj.slug, created=created)

    return render(request, 'stats/main.html', {'qs': qs})


def dashboard(request, slug):
    fake = Faker()
    obj = get_object_or_404(Statistic, slug=slug)

    return render(request, 'stats/dashboard.html', {
        'name': obj.name,
        'slug': obj.slug,
        'data': obj.data,
        'request': request.user.username
        if request.user.username else fake.name()
    })


def chart_data(request, slug):
    obj = get_object_or_404(Statistic, slug=slug)

    qs = obj.data().values('owner').annotate(value_sum=Sum('value'))

    chart_data = [x["value_sum"] for x in qs]
    chart_labels = [x["owner"] for x in qs]

    return JsonResponse({
        "chartData": chart_data,
        "chartLabels": chart_labels,
    })
