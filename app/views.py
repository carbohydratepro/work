from django.template import loader
from django.http import HttpResponse
from django.shortcuts import render


def display_calendar(request):
    """カレンダーを表示"""
    template = loader.get_template('app/index.html')
    return HttpResponse(template.render())

def detail(request, date):
    return render(request, 'app/detail.html', {'date': date})

def new(request):
    return render(request, 'app/new.html')

def create(request):
    return render(request, 'app/create.html')