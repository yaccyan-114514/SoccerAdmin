from django.contrib import admin
from .models import TeamStanding


@admin.register(TeamStanding)
class TeamStandingAdmin(admin.ModelAdmin):
    list_display = [
        "team",
        "year",
        "points",
        "matches_played",
        "wins",
        "draws",
        "losses",
        "goals_for",
        "goals_against",
        "goal_difference_display",
        "assists",
        "yellow_cards",
        "red_cards",
        "penalties",
        "shots",
        "shots_on_target",
        "offsides",
        "corners",
        "passes",
        "fouls",
        "saves",
    ]
    list_editable = [
        "points",
        "matches_played",
        "wins",
        "draws",
        "losses",
        "goals_for",
        "goals_against",
        "assists",
        "yellow_cards",
        "red_cards",
        "penalties",
        "shots",
        "shots_on_target",
        "offsides",
        "corners",
        "passes",
        "fouls",
        "saves",
    ]
    list_filter = ["year", "team"]
    search_fields = ["team__name", "team__short_name"]
    ordering = ["year", "-points", "-goals_for", "goals_against"]

    def goal_difference_display(self, obj):
        return obj.goal_difference

    goal_difference_display.short_description = "净胜球"
