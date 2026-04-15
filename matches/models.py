from datetime import timedelta

from django.db import models
from django.utils import timezone
from teams.models import Team


class Match(models.Model):
    """比赛"""

    home_team = models.ForeignKey(
        Team, on_delete=models.CASCADE, related_name="home_matches", verbose_name="主队"
    )
    away_team = models.ForeignKey(
        Team, on_delete=models.CASCADE, related_name="away_matches", verbose_name="客队"
    )
    match_time = models.DateTimeField("比赛时间")
    round_number = models.PositiveIntegerField("轮次")
    stadium = models.CharField("场地", max_length=100, blank=True)
    tickets_open = models.BooleanField("已开票", default=False)
    created_at = models.DateTimeField("创建时间", auto_now_add=True)

    @property
    def is_tickets_open(self):
        """比赛前 7 天自动开票"""
        now = timezone.now()
        return now >= self.match_time - timedelta(days=7) and now < self.match_time

    class Meta:
        verbose_name = "比赛"
        verbose_name_plural = "比赛"
        ordering = ["match_time"]

    def __str__(self):
        return f"{self.home_team.short_name} vs {self.away_team.short_name}"
