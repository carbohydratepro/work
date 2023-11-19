from django.template import loader
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Shift
from .forms import ShiftForm, ViewTypeForm
from django.http import JsonResponse
from datetime import datetime
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from django.urls import reverse


import json
# import logging

# logger = logging.getLogger(__name__)
# def your_view(request):
#     logger.debug('Debug message')
#     logger.error('Error message')
#     # ...


LOWEST_HOUR = 1
HIGHEST_HOUR = 9


@login_required
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

@login_required
def display_calendar(request):
    try:
        initial_view_type = request.user.view_type
    except AttributeError:
        initial_view_type = "mix"

    form = ViewTypeForm(initial={"view_type": initial_view_type})
    return render(request, 'app/index.html', {'form': form})

@login_required
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
    events = Shift.objects.select_related('user', 'substitute_user').filter(Q(date__range=[start_date, end_date]) & (Q(is_myself=False) | Q(user=request.user)))

    # イベントをFullCalendarが受け入れる形式に変換
    data = [{
        'title': '',
        'user_id': event.user.id,
        'substitute_user_id': event.substitute_user.id if event.substitute_user else None,
        'start': event.date.strftime('%Y-%m-%d'),
        'overlap': False,
        'display': "background",
        'color': 'rgba(128, 128, 128, 0.5)' if event.is_confirmed else ('rgba(255, 0, 0, 0.5)' if event.is_staff else 'rgba(0, 128, 0, 0.5)')
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
        if request.user.view_type == 'me':
            filtered_items = [
                item for item in relevant_items if (item['user_id'] == request.user.id or item['substitute_user_id'] == request.user.id)
                ]
        else:
            color = request.user.view_type
            if color == 'mix':
                # 'mix' の場合は、色の優先順位は 灰色 < 緑色 < 赤色 とする
                color_priority = {'rgba(128, 128, 128, 0.5)': 0, 'rgba(0, 128, 0, 0.5)': 100, 'rgba(255, 0, 0, 0.5)': 200}
                # 最も優先度の高い色を選択する
                max_priority = max(color_priority[item['color']] for item in relevant_items)
                # 最も優先度の高い色のアイテムのみをフィルタリングする
                filtered_items = [item for item in relevant_items if color_priority[item['color']] == max_priority]
                filtered_items = filtered_items[:5]
            else:
                # 'red', 'green', 'grey' のいずれかの場合
                rgba_color_map = {
                    'red': 'rgba(255, 0, 0, 0.5)',
                    'green': 'rgba(0, 128, 0, 0.5)',
                    'grey': 'rgba(128, 128, 128, 0.5)'
                }
                selected_rgba_color = rgba_color_map[color]
                filtered_items = [item for item in relevant_items if item['color'] == selected_rgba_color]
                filtered_items = filtered_items[:5]  # 最大3つのアイテムを選択


        filtered_data.extend(filtered_items)

    # 重複していないデータを追加
    filtered_data.extend([item for item in data if item['start'] not in duplicated_starts])

    data = filtered_data

    return JsonResponse(data, safe=False)

@login_required
def check_shift_exists(request, date):
    exists = Shift.objects.filter(Q(date=date) & (Q(is_myself=False) | Q(user=request.user))).exists()
    print(exists)
    return JsonResponse({'exists': exists})

@login_required
def detail(request, date):
    user = request.user
    # 指定された日付のシフトのみをフィルタリング
    shifts = Shift.objects.select_related('user').filter(Q(date=date) & (Q(is_myself=False) | Q(user=request.user)))
    all_shifts = Shift.objects.select_related('user').filter(Q(date=date) & (Q(is_myself=False) | Q(user=request.user)) & Q(position="all"))
    kitchen_shifts = Shift.objects.select_related('user').filter(Q(date=date) & (Q(is_myself=False) | Q(user=request.user)) & Q(position="kitchen"))
    floor_shifts = Shift.objects.select_related('user').filter(Q(date=date) & (Q(is_myself=False) | Q(user=request.user)) & Q(position="floor"))

    data = [{
        'id':shift.id,
        'user_id': shift.user.id,
        'shift': shift.substitute_name if shift.substitute_name else shift.applicant_name,
        'date':shift.date.strftime('%Y-%m-%d'),
        'Start': shift.start_time.strftime('%H:%M'),
        'Finish': shift.end_time.strftime('%H:%M'),
        'substitute_name':shift.substitute_name,
        'is_staff': shift.is_staff,
        'is_confirmed':shift.is_confirmed,
        'position':shift.position,
        'Resource': 'Shift'
    } for shift in shifts]
    
    # margin用のフェイクデータ追加
    if any(shift['position'] == "floor" for shift in data):
        data.append(
            {"shift": "", "date": date, "Start": "05:00", "Finish": "05:00", "substitute_name": "", "is_staff": True, "is_confirmed": True, "position":"floor", "Resource": "Shift"}
        )
    if any(shift['position'] == "kitchen" for shift in data):
        data.append(
            {"shift": "", "date": date, "Start": "05:00", "Finish": "05:00", "substitute": "", "is_staff": True, "is_confirmed": True, "position":"kitchen", "Resource": "Shift"}
        )
    
    if any(shift['position'] == "all" for shift in data):
        data.append(
            {"shift": "", "date": date, "Start": "05:00", "Finish": "05:00", "substitute": "", "is_staff": True, "is_confirmed": True, "position":"all", "Resource": "Shift"}
        )
    
    data.append(
        {"shift": "", "date": date, "Start": "23:00", "Finish": "23:00", "substitute": "", "is_staff": True, "is_confirmed": True, "position":"all", "Resource": "Shift"}
    )
    
    
    context = {
        'all_shifts': all_shifts,
        'kitchen_shifts': kitchen_shifts,
        'floor_shifts': floor_shifts,
        'data': json.dumps(data),
        'date': date,
        'is_staff': user.is_staff,
    }
    return render(request, 'app/detail.html', context)

@login_required
def new(request):
    user = request.user
    user_position = "all" if user.position == "chick" else user.position
    form_error = None
    if request.method == "POST":
        form = ShiftForm(request.POST or None, initial={'position': user_position})
        if form.is_valid():
            shift = form.save(commit=False)  # データベースにはまだ保存しない
            shift.user = user
            shift.applicant_name = user.username
            shift.start_time = f"{form.cleaned_data['start_hour']}:{form.cleaned_data['start_minute']}"
            shift.end_time = f"{form.cleaned_data['end_hour']}:{form.cleaned_data['end_minute']}"
            if user.is_staff:
                shift.is_staff = True
            else:
                shift.is_staff = False
                
            if 'action' in request.POST:
                if request.POST['action'] == 'register_availability':
                    shift.is_myself = False
                elif request.POST['action'] == 'register_attendance':
                    shift.is_myself = True
                    shift.is_confirmed = True
            shift.save()
            return redirect('display-calendar')  # 仮にcalendarという名前のURLにリダイレクト
        else:
            form_error = form.errors.as_text()  # エラーをテキストとして取得
            form_error = f"勤務時間が{LOWEST_HOUR}時間以上{HIGHEST_HOUR}時間以内になるように調整してください"
    else:
        form = ShiftForm(initial={'position': "all"})

    return render(request, 'app/new.html', {'form': form, 'form_error': form_error})

@login_required
def edit(request, shift_id):
    user = request.user
    
    shift = get_object_or_404(Shift, pk=shift_id)
    if shift.user.id != user.id:
        # 元のURLをリファラヘッダから取得
        referer_url = request.META.get('HTTP_REFERER')
        # リファラが取得できない場合は別のデフォルトURLにリダイレクト
        if not referer_url:
            referer_url = reverse('display-calendar')
        return redirect(referer_url)
    
    form_error = None
    initial = {
        "date": shift.date,
        "start_hour": shift.start_time.hour,
        "start_minute": shift.start_time.minute,
        "end_hour": shift.end_time.hour,
        "end_minute": shift.end_time.minute,
        "position":shift.position,
        "memo": shift.memo,
    }

    if request.method == "POST":
        if shift.is_confirmed and shift.is_myself == False:
            form_error = "確定済みのシフトは変更できません"
            form = ShiftForm(instance=shift, initial=initial)
        else:
            form = ShiftForm(request.POST or None, instance=shift, initial=initial)
            if form.is_valid():
                shift = form.save(commit=False)  # データベースにはまだ保存しない
                shift.applicant_name = user.username
                shift.start_time = f"{form.cleaned_data['start_hour']}:{form.cleaned_data['start_minute']}"
                shift.end_time = f"{form.cleaned_data['end_hour']}:{form.cleaned_data['end_minute']}"
                shift.save()
                messages.success(request, "シフトの編集が完了しました")
                # print(connection.queries) # データベースの状態確認用
                return redirect('list')
            else:
                form_error = form.errors.as_text()  # エラーをテキストとして取得
                form_error = f"勤務時間が{LOWEST_HOUR}時間以上{HIGHEST_HOUR}時間以内になるように調整してください"
    else:
        form = ShiftForm(instance=shift, initial=initial)
    
    return render(request, 'app/edit.html', {'form': form, 'form_error': form_error, 'shift': shift})


@login_required
def delete(request, shift_id):
    shift = get_object_or_404(Shift, pk=shift_id)
    if request.method == "POST":
        if shift.is_confirmed and shift.is_myself == False:
            messages.error(request, "確定済みのシフトは削除できません")
        else:
            shift.delete()
            messages.success(request, "シフトを削除しました")
        return redirect('list')
    return redirect('list')


@login_required
def confirm(request, shift_id):
    user = request.user
    shift = get_object_or_404(Shift, pk=shift_id)
    
    # 元のURLをリファラヘッダから取得
    referer_url = request.META.get('HTTP_REFERER')
    # リファラが取得できない場合は別のデフォルトURLにリダイレクト
    if not referer_url:
        referer_url = reverse('display-calendar')
        
    # 現在の日時を取得
    now = timezone.localtime(timezone.now())
    print(now)

    # shift.date と shift.start_time を組み合わせた日時オブジェクトを作成
    shift_datetime = timezone.make_aware(datetime.combine(shift.date, shift.start_time))

    # shift.date と shift.start_time が現在時刻より前かどうかを確認
    if shift_datetime < now:
        messages.error(request, '過去のシフトは確定できません。')
        return redirect(referer_url)

    if user.is_staff:
        shift.is_confirmed = True
        shift.substitute_user = shift.user
        shift.substitute_name = shift.user.username
        shift.confirmed_user = request.user
        shift.save()
        messages.success(request, 'シフトは正常に確定されました！')
    else:
        shift.is_confirmed = True
        shift.substitute_user = user
        shift.substitute_name = user.username
        shift.confirmed_user = request.user
        shift.save()
        messages.success(request, 'シフトは正常に確定されました！')
    
    
    return redirect(referer_url)


@login_required
def list(request):
    # ログイン中のユーザーのシフトを日付の新しい順に取得
    shifts = Shift.objects.filter(Q(user=request.user) | Q(substitute_user=request.user) | Q(confirmed_user=request.user)).order_by('-date')

    paginator = Paginator(shifts, 10)  # 10件ずつ表示するページネーター

    page = request.GET.get('page')  # 現在のページ番号を取得
    shifts = paginator.get_page(page)  # ページに対応するシフトを取得
    context = {
        'shifts': shifts,
        'today': timezone.now().date()  # 今日の日付をcontextに追加
    }
    return render(request, 'app/list.html', context)

