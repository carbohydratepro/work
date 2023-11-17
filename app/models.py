from django.db import models
from django.utils import timezone

class Shift(models.Model):
    user = models.ForeignKey("auth_app.CustomUser", on_delete=models.CASCADE, null=True)
    applicant_name = models.CharField(max_length=200, verbose_name="申請者の名前")
    substitute_user = models.ForeignKey("auth_app.CustomUser", on_delete=models.SET_NULL, blank=True, null=True, related_name="代役ユーザー")
    substitute_name = models.CharField(max_length=200, verbose_name="代役の名前", blank=True, null=True)
    date = models.DateField(verbose_name="日付", default=timezone.now)
    start_time = models.TimeField(verbose_name="開始時間")
    end_time = models.TimeField(verbose_name="終了時間")
    is_substitute_found = models.BooleanField(default=False, verbose_name="代役が見つかっている")
    is_confirmed = models.BooleanField(default=False, verbose_name="確定済み")
    is_staff = models.BooleanField(default=False, verbose_name="スタッフアカウント")
    is_myself = models.BooleanField(default=False)
    position = models.CharField(max_length=10, default="all") # chick kitchen floor all
    memo = models.TextField(null=True, default=None, blank=True)

    def __str__(self):
        return self.applicant_name or "未指定"