from django.contrib import admin
from .models import Team, Player


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ["short_name", "name", "city", "stadium", "founded_year"]
    list_filter = ["city"]
    search_fields = ["name", "short_name", "city"]
    ordering = ["short_name"]


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "team",
        "year",
        "position",
        "number",
        "goals",
        "assists",
        "yellow_cards",
        "red_cards",
        "penalties",
        "shots",
        "shots_on_target",
        "dribbles",
        "fouls",
        "fouls_suffered",
        "passes",
        "crosses",
        "tackles",
        "clearances",
        "saves",
        "market_value",
    ]
    list_editable = [
        "goals",
        "assists",
        "yellow_cards",
        "red_cards",
        "penalties",
        "shots",
        "shots_on_target",
        "dribbles",
        "fouls",
        "fouls_suffered",
        "passes",
        "crosses",
        "tackles",
        "clearances",
        "saves",
        "market_value",
    ]
    list_filter = ["team", "year", "position"]
    search_fields = ["name", "team__name", "team__short_name"]
    ordering = ["team", "number"]
