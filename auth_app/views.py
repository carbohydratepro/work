from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView
from django.shortcuts import render, redirect, resolve_url
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import UserPassesTestMixin
from .forms import LoginForm, SignupForm, UserUpdateForm, MyPasswordChangeForm
from django.urls import reverse_lazy



class TopView(generic.TemplateView):
    template_name = 'registration/top.html'
    
class Login(LoginView):
    form_class = LoginForm
    template_name = 'registration/login.html'
    
'''自分しかアクセスできないようにするMixin(My Pageのため)'''
class OnlyYouMixin(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        # 今ログインしてるユーザーのpkと、そのマイページのpkが同じなら許可
        user = self.request.user
        return user.pk == self.kwargs['pk']


'''マイページ'''
class MyPage(OnlyYouMixin, generic.DetailView):
    # ユーザーモデル取得
    User = get_user_model()
    model = User
    template_name = 'registration/my_page.html'
    # モデル名小文字(user)でモデルインスタンスがテンプレートファイルに渡される
    
'''サインアップ'''
class Signup(generic.CreateView):
    template_name = 'registration/user_form.html'
    form_class = SignupForm

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_staff = False
        user.is_superuser = False
        user.save()
        return redirect('signup_done')

    # データ送信
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["process_name"] = "サインアップ"
        context["button_text"] = "サインアップ"
        return context


'''サインアップ完了'''
class SignupDone(generic.TemplateView):
    template_name = 'registration/signup_done.html'
    
    
'''ユーザー登録情報の更新'''
class Edit(OnlyYouMixin, generic.UpdateView):
    model = get_user_model()
    form_class = UserUpdateForm
    template_name = 'registration/user_form.html'

    def get_success_url(self):
        return resolve_url('my_page', pk=self.kwargs['pk'])

    # contextデータ作成
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["process_name"] = "名前変更フォーム"
        context["button_text"] = "変更"
        return context

'''パスワード変更'''
class PasswordChange(PasswordChangeView):
    form_class = MyPasswordChangeForm
    success_url = reverse_lazy('password_change_done')
    template_name = 'registration/user_form.html'
    
    # contextデータ作成
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["process_name"] = "パスワード変更フォーム"
        context["button_text"] = "変更"
        return context


'''パスワード変更完了'''
class PasswordChangeDone(PasswordChangeDoneView):
    template_name = 'registration/passwordchange_done.html'