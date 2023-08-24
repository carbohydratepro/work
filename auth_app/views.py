from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def protected_view(request):
    # ここにビューのロジックを記述します。
    return render(request, 'login.html')
