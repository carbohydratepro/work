from django.db import models

class Shift(models.Model):
    applicant_name = models.CharField(max_length=200, verbose_name="申請者の名前")
    substitute_name = models.CharField(max_length=200, verbose_name="代役の名前", blank=True, null=True)  # 代役がまだ決まっていない場合も考慮
    start_time = models.DateTimeField(verbose_name="開始時間")
    end_time = models.DateTimeField(verbose_name="終了時間")
    is_substitute_found = models.BooleanField(default=False, verbose_name="代役が見つかっている")

    def __str__(self):
        return self.applicant_name
