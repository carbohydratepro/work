from django.template import loader
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Shift
from .forms import ShiftForm, ViewTypeForm, TestForm
from django.http import JsonResponse
from datetime import datetime
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

import json
# import logging

# logger = logging.getLogger(__name__)
# def your_view(request):
#     logger.debug('Debug message')
#     logger.error('Error message')
#     # ...


@csrf_exempt
def update_user_view_type(request):
    if request.method == 'POST':
        form = ViewTypeForm(request.POST)
        if form.is_valid():
            view_type = form.cleaned_data['view_type']
            request.user.view_type = view_type
            request.user.save()
            return JsonResponse({'status': 'ok'})
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors})
    return JsonResponse({'status': 'invalid_method'})

def display_calendar(request):
    try:
        initial_view_type = request.user.view_type
    except AttributeError:
        initial_view_type = "red"

    form = ViewTypeForm(initial={"view_type": initial_view_type})
    return render(request, 'app/index.html', {'form': form})

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
        'color': 'grey' if event.is_confirmed else ('red' if event.is_staff else 'green')
    } for event in events]

    # 重複するstart日付を特定
    duplicated_starts = set()
    start_counts = {}
    for entry in data:
        start = entry['start']
        start_counts[start] = start_counts.get(start, 0) + 1
        if start_counts[start] > 0:
            duplicated_starts.add(start)

    # 各日付に対して必要な色を決定する
    filtered_data = []
    for start in duplicated_starts:
        relevant_items = [item for item in data if item['start'] == start]
        color = request.user.view_type
        if color == 'mix':
            # 'mix' の場合は、色の優先順位は 灰色 < 緑色 < 赤色 とする
            color_priority = {'grey': 0, 'green': 100, 'red': 200}
            # 最も優先度の高い色を選択する
            max_priority = max(color_priority[item['color']] for item in relevant_items)
            # 最も優先度の高い色のアイテムのみをフィルタリングする
            filtered_items = [item for item in relevant_items if color_priority[item['color']] == max_priority]
        else:
            # 'red', 'green', 'grey' のいずれかの場合は、指定された色のアイテムのみをフィルタリングする
            filtered_items = [item for item in relevant_items if item['color'] == color]

        filtered_data.extend(filtered_items)

    # 重複していないデータを追加
    filtered_data.extend([item for item in data if item['start'] not in duplicated_starts])

    data = filtered_data

    return JsonResponse(data, safe=False)

def check_shift_exists(request, date):
    exists = Shift.objects.filter(date=date).exists()
    print(exists)
    return JsonResponse({'exists': exists})


def detail(request, date):
    # 指定された日付のシフトのみをフィルタリング
    shifts = Shift.objects.filter(date=date)

    data = [{
        'id':shift.id,
        'shift': shift.applicant_name,
        'date':shift.date.strftime('%Y-%m-%d'),
        'Start': shift.start_time.strftime('%H:%M'),
        'Finish': shift.end_time.strftime('%H:%M'),
        'substitute':shift.is_substitute_found,
        'is_staff': shift.is_staff,
        'is_confirmed':shift.is_confirmed,
        'Resource': 'Shift'
    } for shift in shifts]
    
    # margin用のフェイクデータ追加
    data.append(
        {"shift": "", "date": date, "Start": "05:00", "Finish": "05:00", "substitute": False, "is_staff": False, "is_confirmed": False, "Resource": "Shift"}
    )
    data.append(
        {"shift": "", "date": date, "Start": "23:00", "Finish": "23:00", "substitute": False, "is_staff": False, "is_confirmed": False, "Resource": "Shift"}
    )
    
    context = {
        'data': json.dumps(data),
        'date': date,
    }
    return render(request, 'app/detail.html', context)

def new(request):
    user = request.user
    form_error = None
    if request.method == "POST":
        form = ShiftForm(request.POST or None)
        if form.is_valid():
            shift = form.save(commit=False)  # データベースにはまだ保存しない
            shift.applicant_name = user.username
            shift.start_time = f"{form.cleaned_data['start_hour']}:{form.cleaned_data['start_minute']}"
            shift.end_time = f"{form.cleaned_data['end_hour']}:{form.cleaned_data['end_minute']}"
            if user.is_staff:
                shift.is_staff = True
            shift.save()
            return redirect('display-calendar')  # 仮にcalendarという名前のURLにリダイレクト
        else:
            form_error = form.errors.as_text()  # エラーをテキストとして取得
    else:
        form = ShiftForm()

    return render(request, 'app/new.html', {'form': form, 'form_error': form_error})


def edit(request, shift_id):
    user = request.user
    shift = get_object_or_404(Shift, pk=shift_id)
    form_error = None
    if request.method == "POST":
        form = ShiftForm(request.POST or None, instance=shift)
        if form.is_valid():
            shift = form.save(commit=False)  # データベースにはまだ保存しない
            shift.applicant_name = user.username
            shift.start_time = f"{form.cleaned_data['start_hour']}:{form.cleaned_data['start_minute']}"
            shift.end_time = f"{form.cleaned_data['end_hour']}:{form.cleaned_data['end_minute']}"
            shift.save()
            # print(connection.queries) # データベースの状態確認用
            return redirect('display-calendar')  # 仮にcalendarという名前のURLにリダイレクト
        else:
            LOWEST_HOUR = 2
            HIGHEST_HOUR = 8
            form_error = form.errors.as_text()  # エラーをテキストとして取得
            form_error = f"勤務時間が{LOWEST_HOUR}時間以上{HIGHEST_HOUR}時間以内になるように調整してください"
            
    else:
        form = ShiftForm(instance=shift)
    
    return render(request, 'app/edit.html', {'form': form, 'form_error': form_error})


def delete(request, shift_id):
    shift = get_object_or_404(Shift, pk=shift_id)
    if request.method == "POST":
        shift.delete()
        return redirect('display-calendar')
    return render(request, 'app/delete.html', {'shift': shift})

def test(request):
    import torch
    from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
    from torch.optim import AdamW
    
    sentence=[
        'アメリカには自由の女神がある。',
        'アフリカの草原にはゾウがいる。',
        '早起きして一日を有意義に過ごす。',
        'パソコンが壊れたので買い替える。',
        'リサイクルショップで中古の自転車を買う。',
        '自由の女神がある国はアメリカである。',
        '新品の電動自転車を購入する。'
    ]
    
    model_name = "cl-tohoku/bert-large-japanese"
    unmasker = pipeline('fill-mask', model=model_name)
    results = None
    
    sentence_index = request.GET.get(key="sentence", default=0)
    word_selected = request.GET.get(key="word", default="")
    
    form = TestForm()
    if request.method == "POST":
        if form.is_valid():
        # 内容を取得する
            sentence_index = int(form.cleaned_data.get("sentence"))
            word_selected = form.cleaned_data.get("word")
            

    sentence_selected = sentence[int(sentence_index)]
    form.fields['sentence'].initial = [sentence_selected]
    
    # 選択フォームの選択を取得した値で固定する
    print(sentence_selected)
    print(word_selected)

    
    if (sentence_selected is not None and 
        word_selected is not None and
        word_selected in sentence_selected):
        
        text = sentence_selected.replace(word_selected, "[MASK]")
        results = unmasker(text)

        for result in results:
            if isinstance(result, dict) and "token_str" in result:
                token_str = result["token_str"]
                score = result["score"]
                print(f"{token_str}:{score:.5f}")
                
    context = {
        "form": form,
        "sentence_selected": sentence_selected,
        "word_selected": word_selected,
        "results": results,
    }

    return render(request, 'app/test.html', context)