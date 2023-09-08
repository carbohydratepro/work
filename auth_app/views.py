from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views import generic

@login_required
def protected_view(request):
    # ここにビューのロジックを記述します。
    return render(request, 'registaration/login.html')

class TopView(generic.TemplateView):
    template_name = 'registration/top.html'