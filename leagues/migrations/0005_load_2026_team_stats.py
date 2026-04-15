"""
填充 2026 赛季中超前 5 轮球队统计数据
"""
from django.db import migrations


TEAM_STATS = {
    # short_name: (matches, W, D, L, GF, GA, pts, assists, yellow, red, pen, shots, sot, off, corners, passes, fouls, saves)
    "上海海港":     (5, 4, 0, 1, 10, 3, 12,  7, 9,  0, 1, 72, 31, 8,  38, 2380, 58, 16),
    "山东泰山":     (5, 3, 2, 0,  8, 3, 11,  6, 11, 0, 0, 68, 28, 10, 35, 2290, 62, 18),
    "上海申花":     (5, 3, 1, 1,  8, 5, 10,  5, 10, 1, 1, 65, 27, 7,  33, 2250, 55, 20),
    "北京国安":     (5, 3, 1, 1,  7, 4, 10,  5, 12, 0, 0, 63, 25, 9,  31, 2200, 60, 19),
    "成都蓉城":     (5, 2, 3, 0,  6, 3,  9,  4, 8,  0, 1, 58, 24, 6,  30, 2180, 52, 17),
    "浙江":         (5, 2, 2, 1,  7, 5,  8,  5, 13, 1, 0, 61, 26, 11, 34, 2150, 65, 22),
    "武汉三镇":     (5, 2, 2, 1,  5, 4,  8,  3, 10, 0, 1, 55, 22, 8,  28, 2100, 58, 21),
    "天津津门虎":   (5, 2, 1, 2,  5, 6,  7,  3, 14, 1, 0, 52, 20, 7,  27, 2050, 68, 24),
    "青岛海牛":     (5, 2, 1, 2,  5, 6,  7,  4, 11, 0, 1, 54, 21, 9,  29, 2020, 63, 25),
    "大连英博":     (5, 1, 3, 1,  4, 4,  6,  3, 15, 0, 0, 48, 18, 6,  25, 1980, 70, 23),
    "深圳新鹏城":   (5, 1, 2, 2,  4, 6,  5,  3, 12, 1, 0, 50, 19, 10, 26, 1950, 66, 27),
    "河南":         (5, 1, 2, 2,  3, 5,  5,  2, 13, 0, 1, 46, 17, 8,  24, 1920, 64, 26),
    "云南玉昆":     (5, 1, 1, 3,  4, 8,  4,  3, 16, 1, 0, 44, 16, 5,  23, 1880, 72, 30),
    "辽宁铁人":     (5, 1, 1, 3,  3, 7,  4,  2, 14, 0, 0, 42, 15, 7,  22, 1860, 69, 28),
    "青岛西海岸":   (5, 0, 2, 3,  2, 7,  2,  1, 17, 2, 0, 40, 14, 6,  21, 1850, 74, 29),
    "重庆铜梁龙":   (5, 0, 0, 5,  1, 6,  0,  1, 18, 1, 0, 38, 13, 5,  20, 1800, 76, 31),
}


def load_team_stats(apps, schema_editor):
    TeamStanding = apps.get_model("leagues", "TeamStanding")
    for ts in TeamStanding.objects.filter(year=2026).select_related("team"):
        stats = TEAM_STATS.get(ts.team.short_name)
        if not stats:
            continue
        (
            ts.matches_played, ts.wins, ts.draws, ts.losses,
            ts.goals_for, ts.goals_against, ts.points,
            ts.assists, ts.yellow_cards, ts.red_cards, ts.penalties,
            ts.shots, ts.shots_on_target, ts.offsides, ts.corners,
            ts.passes, ts.fouls, ts.saves,
        ) = stats
        ts.save()


def clear_team_stats(apps, schema_editor):
    TeamStanding = apps.get_model("leagues", "TeamStanding")
    TeamStanding.objects.filter(year=2026).update(
        matches_played=0, wins=0, draws=0, losses=0,
        goals_for=0, goals_against=0, points=0,
        assists=0, yellow_cards=0, red_cards=0, penalties=0,
        shots=0, shots_on_target=0, offsides=0, corners=0,
        passes=0, fouls=0, saves=0,
    )


class Migration(migrations.Migration):

    dependencies = [
        ("leagues", "0004_teamstanding_year_alter_teamstanding_team_and_more"),
    ]

    operations = [
        migrations.RunPython(load_team_stats, clear_team_stats),
    ]
