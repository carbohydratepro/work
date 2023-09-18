from django.template import loader
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Shift
from .forms import ShiftForm
from django.http import JsonResponse
from datetime import datetime
import json


def display_calendar(request):
    """カレンダーを表示"""
    template = loader.get_template('app/index.html')
    return HttpResponse(template.render())

def get_events(request):
    start_date_str = request.GET.get('start')
    end_date_str = request.GET.get('end')

    # 正しい形式に変換
    start_date_str = start_date_str.replace(" ", "+")
    end_date_str = end_date_str.replace(" ", "+")
    
    # ISO 8601形式の日付文字列（'2023-08-27T00:00:00+09:00'）をdatetimeオブジェクトに変換
    start_date = datetime.fromisoformat(start_date_str)
    end_date = datetime.fromisoformat(end_date_str)

    # datetimeオブジェクトを'YYYY-MM-DD'形式の文字列に変換
    start_date = start_date.strftime('%Y-%m-%d')
    end_date = end_date.strftime('%Y-%m-%d')
    
    # この範囲内のイベントをクエリします。
    events = Shift.objects.filter(date__range=[start_date, end_date])

    # イベントをFullCalendarが受け入れる形式に変換
    data = [{
        'title': '',
        'start': event.date.strftime('%Y-%m-%d'),
        'overlap': False,
        'display': "background",
        'color': 'green' if event.is_substitute_found else 'red'
    } for event in events]


    # 重複するstart日付を特定
    duplicated_starts = set()
    start_counts = {}
    for entry in data:
        start = entry['start']
        start_counts[start] = start_counts.get(start, 0) + 1
        if start_counts[start] > 1:
            duplicated_starts.add(start)

    # 同じstart日付を持ち、'green'と'red'が両方存在する場合、'green'を削除
    filtered_data = []
    for start in duplicated_starts:
        green_exists = any(item for item in data if item['start'] == start and item['color'] == 'green')
        red_exists = any(item for item in data if item['start'] == start and item['color'] == 'red')
        
        if green_exists and red_exists:
            filtered_data.extend([item for item in data if not (item['start'] == start and item['color'] == 'green')])
        else:
            filtered_data.extend([item for item in data if item['start'] == start])
            
    # 重複していないデータを追加
    filtered_data.extend([item for item in data if item['start'] not in duplicated_starts])

    data = filtered_data


    return JsonResponse(data, safe=False)

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
    
    # margin用のフェイクデータ追加
    data.append(
        {"shift": "", "date": date, "Start": "05:00", "Finish": "05:00", "substitute": False, "Resource": "Shift"}
    )
    data.append(
        {"shift": "", "date": date, "Start": "23:00", "Finish": "23:00", "substitute": False, "Resource": "Shift"}
    )
    
    context = {
        'data': json.dumps(data),
        'date': date,
    }
    return render(request, 'app/detail.html', context)

def new(request):
    user = request.user
    if request.method == "POST":
        form = ShiftForm(request.POST)
        if form.is_valid():
            shift = form.save(commit=False)  # データベースにはまだ保存しない
            shift.applicant_name = user.username
            shift.start_time = f"{form.cleaned_data['start_hour']}:{form.cleaned_data['start_minute']}"
            shift.end_time = f"{form.cleaned_data['end_hour']}:{form.cleaned_data['end_minute']}"
            shift.save()
            return redirect('display-calendar')  # 仮にcalendarという名前のURLにリダイレクト
    else:
        form = ShiftForm()

    return render(request, 'app/new.html', {'form': form})


def edit(request, shift_id):
    shift = get_object_or_404(Shift, pk=shift_id)
    if request.method == "POST":
        form = ShiftForm(request.POST, instance=shift)
        if form.is_valid():
            form.save()
            return redirect('display-calendar')  # ここは適切なリダイレクト先に変更してください
    else:
        form = ShiftForm(instance=shift)
    return render(request, 'app/edit.html', {'form': form})


def delete(request, shift_id):
    shift = get_object_or_404(Shift, pk=shift_id)
    if request.method == "POST":
        shift.delete()
        return redirect('display-calendar')  # ここは適切なリダイレクト先に変更してください
    return render(request, 'app/delete.html', {'shift': shift})