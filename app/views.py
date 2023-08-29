from django.template import loader
from django.http import HttpResponse
from django.shortcuts import render
from .models import Shift
import json


def display_calendar(request):
    """カレンダーを表示"""
    template = loader.get_template('app/index.html')
    return HttpResponse(template.render())

def detail(request, date):
    shifts = Shift.objects.all()
    data = [{
        'shift': shift.name,
        'Start': shift.start_time.strftime('%Y-%m-%d %H:%M'),
        'Finish': shift.end_time.strftime('%Y-%m-%d %H:%M'),
        'Resource': 'Shift'
    } for shift in shifts]
    
    context = {
        'data': json.dumps(data),
        'date': date,
    }
    return render(request, 'app/detail.html', context)

def new(request):
    return render(request, 'app/new.html')

def create(request):
    return render(request, 'app/create.html')