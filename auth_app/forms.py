from django import forms
from django.contrib.auth import get_user_model # ユーザーモデルを取得するため
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm




'''ログイン用フォーム'''
class LoginForm(AuthenticationForm):
    employee_id_number = forms.CharField(label="社員コード")

    # bootstrap4対応
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['employee_id_number'].label = "社員コード"
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label  # placeholderにフィールドのラベルを入れる



'''サインアップ用フォーム'''
class SignupForm(UserCreationForm):
    username = forms.CharField(label="ユーザー名")
    email = forms.EmailField(label="メールアドレス")
    store_code = forms.CharField(label="店舗コード")
    employee_id_number = forms.CharField(label="社員コード")

    class Meta:
        model = get_user_model()
        fields = ('username', 'employee_id_number', 'store_code', 'email')

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['required'] = '' # 全フィールドを入力必須

            # オートフォーカスとプレースホルダーの設定
            print(field.label)
            # if field.label == '姓':
            #     field.widget.attrs['autofocus'] = '' # 入力可能状態にする
            #     field.widget.attrs['placeholder'] = '田中'
            # elif field.label == '名':
            #     field.widget.attrs['placeholder'] = '一郎'
            # elif field.label == 'メールアドレス':
            #     field.widget.attrs['placeholder'] = '***@gmail.com'
            

'''ユーザー情報更新用フォーム'''
class UserUpdateForm(forms.ModelForm):
    position = forms.ChoiceField(
        choices=[
            ('chick', 'ひよっこ'),
            ('kitchen', 'キッチン'),
            ('floor', 'フロア'),
            ('all', 'オール'),
        ],
        widget=forms.Select(attrs={'id': 'category_select'}),
        required=True,
        label="ポジション",
        )

    username = forms.CharField(label="ユーザー名")
    email = forms.EmailField(label="メールアドレス")
    store_code = forms.CharField(label="店舗コード")
    employee_id_number = forms.CharField(label="社員コード")
    
    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'store_code', 'employee_id_number', 'position')

    # bootstrap4対応
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['required'] = '' # 全フィールドを入力必須
            

'''パスワード変更フォーム'''
class MyPasswordChangeForm(PasswordChangeForm):

    # bootstrap4対応で、classを指定
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'