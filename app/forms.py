from django import forms
from django.core.exceptions import ValidationError
from .models import Shift
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

    class Meta:
        model = Shift
        fields = ['date', 'start_hour', 'start_minute', 'end_hour', 'end_minute']


    def clean(self):
        
        LOWEST_HOUR = 2
        HIGHEST_HOUR = 8
        
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
            ('red', '不足のみを表示'),
            ('green', '勤務可能のみを表示'),
            ('grey', '確定済みのみを表示'),
            ('mix', 'すべて表示')
        ],
        widget=forms.Select(attrs={'id': 'category_select'}),
        required=True
        )

class TestForm(forms.Form):
    sentence = forms.ChoiceField(
        choices=[
            (0, 'アメリカには自由の女神がある。'),
            (1, 'アフリカの草原にはゾウがいる。'),
            (2, '早起きして一日を有意義に過ごす。'),
            (3, 'パソコンが壊れたので買い替える。'),
            (4, 'リサイクルショップで中古の自転車を買う。'),
            (5, '自由の女神がある国はアメリカである。'),
            (6, '新品の電動自転車を購入する。')
        ],
        widget=forms.Select(attrs={'id': 'category_select'}),
        required=False
        )
    
    word = forms.CharField()
    
    