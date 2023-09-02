from django.template import loader
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Shift
from .forms import ShiftForm
import json


def display_calendar(request):
    """カレンダーを表示"""
    template = loader.get_template('app/index.html')
    return HttpResponse(template.render())

def detail(request, date):
    # 指定された日付のシフトのみをフィルタリング
    shifts = Shift.objects.filter(date=date)

    data = [{
        'shift': shift.applicant_name,
        'date':shift.date.strftime('%Y-%m-%d'),
        'Start': shift.start_time.strftime('%H:%M'),
        'Finish': shift.end_time.strftime('%H:%M'),
        'substitute':shift.is_substitute_found,
        'Resource': 'Shift'
    } for shift in shifts]
    
    context = {
        'data': json.dumps(data),
        'date': date,
    }
    return render(request, 'app/detail.html', context)

def new(request):
    if request.method == "POST":
        form = ShiftForm(request.POST)
        if form.is_valid():
            shift = form.save(commit=False)  # データベースにはまだ保存しない
            shift.start_time = f"{form.cleaned_data['start_hour']}:{form.cleaned_data['start_minute']}"
            shift.end_time = f"{form.cleaned_data['end_hour']}:{form.cleaned_data['end_minute']}"
            shift.save()
            return redirect('display-calendar')  # 仮にcalendarという名前のURLにリダイレクト
    else:
        form = ShiftForm()

    return render(request, 'app/new.html', {'form': form})