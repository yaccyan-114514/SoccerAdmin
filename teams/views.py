from django.shortcuts import render, get_object_or_404
from .models import Team


def team_detail(request, pk):
    """球队详情页"""
    team = get_object_or_404(Team, pk=pk)
    return render(request, "teams/team_detail.html", {"team": team})
