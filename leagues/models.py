from django.db import models
from teams.models import Team


class TeamStanding(models.Model):
    """积分榜"""

    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name="standings",
        verbose_name="球队",
    )
    year = models.PositiveIntegerField("年份", default=2026)
    points = models.PositiveIntegerField("胜点", default=0)
    matches_played = models.PositiveIntegerField("场次", default=0)
    wins = models.PositiveIntegerField("胜", default=0)
    draws = models.PositiveIntegerField("平", default=0)
    losses = models.PositiveIntegerField("负", default=0)
    goals_for = models.PositiveIntegerField("进球", default=0)
    goals_against = models.PositiveIntegerField("失球", default=0)
    assists = models.PositiveIntegerField("助攻", default=0)
    yellow_cards = models.PositiveIntegerField("黄牌", default=0)
    red_cards = models.PositiveIntegerField("红牌", default=0)
    penalties = models.PositiveIntegerField("点球", default=0)
    shots = models.PositiveIntegerField("射门", default=0)
    shots_on_target = models.PositiveIntegerField("射正", default=0)
    offsides = models.PositiveIntegerField("越位", default=0)
    corners = models.PositiveIntegerField("角球", default=0)
    passes = models.PositiveIntegerField("传球", default=0)
    fouls = models.PositiveIntegerField("犯规", default=0)
    saves = models.PositiveIntegerField("扑救", default=0)

    class Meta:
        verbose_name = "积分"
        verbose_name_plural = "积分榜"
        ordering = ["-points", "-goals_for", "goals_against"]
        unique_together = [["team", "year"]]

    def __str__(self):
        return f"{self.team.short_name} - {self.points}分"

    @property
    def goal_difference(self):
        """净胜球"""
        return self.goals_for - self.goals_against
