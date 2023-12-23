from django import forms
from django.core.exceptions import ValidationError
from .models import Shift, RegisteredShift, Break
from datetime import timedelta

class ShiftForm(forms.ModelForm):

    HOURS = [i for i in range(6, 23)]  # 5 to 22
    MINUTES = [0, 10, 20, 30, 40, 50]

    HOUR_CHOICES = [(f"{hour:02d}", f"{hour:02d}") for hour in HOURS]
    MINUTE_CHOICES = [(f"{minute:02d}", f"{minute:02d}") for minute in MINUTES]

    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        input_formats=['%Y-%m-%d'],
        label="日付"
    )
    start_hour = forms.ChoiceField(choices=HOUR_CHOICES, label='開始時')
    start_minute = forms.ChoiceField(choices=MINUTE_CHOICES, label='開始分')
    end_hour = forms.ChoiceField(choices=HOUR_CHOICES, label='終了時')
    end_minute = forms.ChoiceField(choices=MINUTE_CHOICES, label='終了分')
    
    position = forms.ChoiceField(
        choices=[
            ('kitchen', 'キッチン'),
            ('floor', 'フロア'),
            ('all', 'オール'),
        ],
        widget=forms.Select(attrs={'id': 'category_select'}),
        required=True,
        label="ポジション"
        )
    
    memo = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 5,'placeholder': 'メモを入力...'}),
        )
    
    
    class Meta:
        model = Shift
        fields = ['date', 'start_hour', 'start_minute', 'end_hour', 'end_minute', 'position', 'memo']


    def clean(self):
        
        LOWEST_HOUR = 1
        HIGHEST_HOUR = 9
        
        cleaned_data = super().clean()
        
        start_hour = int(cleaned_data.get("start_hour"))
        start_minute = int(cleaned_data.get("start_minute"))
        end_hour = int(cleaned_data.get("end_hour"))
        end_minute = int(cleaned_data.get("end_minute"))

        # 時間オブジェクトを作成
        start_time = timedelta(hours=start_hour, minutes=start_minute)
        end_time = timedelta(hours=end_hour, minutes=end_minute)

        # 時間差を計算
        time_difference = end_time - start_time
        hours_difference = time_difference.total_seconds() / 3600  # 秒単位での時間差を時間単位に変換

        # 2から8時間の範囲内にあるかどうかをチェック
        if not (LOWEST_HOUR <= hours_difference <= HIGHEST_HOUR):
            raise ValidationError("error")
            

        return cleaned_data
    

class ViewTypeForm(forms.Form):
    view_type = forms.ChoiceField(
        choices=[
            ('mix', 'すべて表示'),
            ('red', '不足のみを表示'),
            ('green', '勤務可能のみを表示'),
            ('grey', '確定済みのみを表示'),
            ('me', '自分のシフトのみを表示'),
        ],
        widget=forms.Select(attrs={'id': 'category_select'}),
        required=True,
        label="表示方法"
        )

class ImageUploadForm(forms.Form):
    image = forms.ImageField()
    
class RegisteredShiftForm(forms.ModelForm):
    HOURS = [i for i in range(6, 23)]  # 5 to 22
    MINUTES = [0, 10, 20, 30, 40, 50]

    HOUR_CHOICES = [(f"{hour:02d}", f"{hour:02d}") for hour in HOURS]
    MINUTE_CHOICES = [(f"{minute:02d}", f"{minute:02d}") for minute in MINUTES]

    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        input_formats=['%Y-%m-%d'],
        label="日付"
    )
    start_hour = forms.ChoiceField(choices=HOUR_CHOICES, label='開始時')
    start_minute = forms.ChoiceField(choices=MINUTE_CHOICES, label='開始分')
    end_hour = forms.ChoiceField(choices=HOUR_CHOICES, label='終了時')
    end_minute = forms.ChoiceField(choices=MINUTE_CHOICES, label='終了分')
    
    break_start_hour = forms.ChoiceField(choices=HOUR_CHOICES, label='開始時')
    break_start_minute = forms.ChoiceField(choices=MINUTE_CHOICES, label='開始分')
    break_end_hour = forms.ChoiceField(choices=HOUR_CHOICES, label='終了時')
    break_end_minute = forms.ChoiceField(choices=MINUTE_CHOICES, label='終了分')
    
    position = forms.ChoiceField(
        choices=[
            ('kitchen', 'キッチン'),
            ('floor', 'フロア'),
            ('all', 'オール'),
        ],
        widget=forms.Select(attrs={'id': 'category_select'}),
        required=True,
        label="ポジション"
        )
    
    class Meta:
        model = RegisteredShift
        fields = ['date', 'username', 'start_hour', 'start_minute', 'end_hour', 'end_minute','break_start_hour', 'break_start_minute', 'break_end_hour', 'break_end_minute', 'position']

    def clean(self):
        
        LOWEST_HOUR = 1
        HIGHEST_HOUR = 9
        
        cleaned_data = super().clean()
        
        start_hour = int(cleaned_data.get("start_hour"))
        start_minute = int(cleaned_data.get("start_minute"))
        end_hour = int(cleaned_data.get("end_hour"))
        end_minute = int(cleaned_data.get("end_minute"))

        # 時間オブジェクトを作成
        start_time = timedelta(hours=start_hour, minutes=start_minute)
        end_time = timedelta(hours=end_hour, minutes=end_minute)

        break_start_hour = int(cleaned_data.get("break_start_hour"))
        break_start_minute = int(cleaned_data.get("break_start_minute"))
        break_end_hour = int(cleaned_data.get("break_end_hour"))
        break_end_minute = int(cleaned_data.get("break_end_minute"))

        # 時間オブジェクトを作成
        break_start_time = timedelta(hours=break_start_hour, minutes=break_start_minute)
        break_end_time = timedelta(hours=break_end_hour, minutes=break_end_minute)
        
        # 時間差を計算
        time_difference = end_time - start_time
        hours_difference = time_difference.total_seconds() / 3600  # 秒単位での時間差を時間単位に変換

        # 2から8時間の範囲内にあるかどうかをチェック
        if not (LOWEST_HOUR <= hours_difference <= HIGHEST_HOUR):
            raise ValidationError("error")
            

        return cleaned_data