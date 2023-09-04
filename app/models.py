from django.db import models
from django.utils import timezone

class Shift(models.Model):
    applicant_name = models.CharField(max_length=200, verbose_name="申請者の名前")
    substitute_name = models.CharField(max_length=200, verbose_name="代役の名前", blank=True, null=True)
    date = models.DateField(verbose_name="日付", default=timezone.now)
    start_time = models.TimeField(verbose_name="開始時間")
    end_time = models.TimeField(verbose_name="終了時間")
    is_substitute_found = models.BooleanField(default=False, verbose_name="代役が見つかっている")

    def __str__(self):
        return self.applicant_name
