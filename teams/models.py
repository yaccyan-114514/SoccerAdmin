from django.db import models


class Team(models.Model):
    """球队模型"""

    name = models.CharField("球队全称", max_length=100)
    short_name = models.CharField("简称", max_length=50)
    city = models.CharField("所在城市", max_length=50)
    stadium = models.CharField("主场", max_length=100, blank=True)
    founded_year = models.PositiveIntegerField("成立年份", null=True, blank=True)
    created_at = models.DateTimeField("创建时间", auto_now_add=True)
    updated_at = models.DateTimeField("更新时间", auto_now=True)

    class Meta:
        verbose_name = "球队"
        verbose_name_plural = "球队"
        ordering = ["name"]

    def __str__(self):
        return self.short_name

    def get_logo_filename(self):
        """获取队徽文件名"""
        logo_map = {
            "北京国安": "beijing-guoan-v2022.png",
            "成都蓉城": "chengdu-rongcheng-v2021.png",
            "河南": "henan-fc-v2023.png",
            "青岛海牛": "qingdao-hainiu-v2022.png",
            "青岛西海岸": "qingdao-west-coast-v2023.png",
            "山东泰山": "shandong-taishan-v2022.png",
            "上海海港": "shanghai-port-v2021.png",
            "上海申花": "shanghai-shenhua-v2022.png",
            "深圳新鹏城": "shenzhen-peng-city-v2024.png",
            "天津津门虎": "tianjin-jinmen-tiger-v2021.png",
            "武汉三镇": "wuhan-three-towns-v2019.png",
            "浙江": "zhejiang-professional-v2022.png",
            "辽宁铁人": "liaoning-tieren-v2024.png",
            "重庆铜梁龙": "chongqing-tonglianglong-v2023.png",
            "大连英博": "Dalian-Yingbo-v2025.png",
            "云南玉昆": "YunNan-YuKun-v2025.png",
        }
        return logo_map.get(self.short_name, None)


class Player(models.Model):
    """球员模型"""

    name = models.CharField("姓名", max_length=50)
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name="players",
        verbose_name="球队",
    )
    position = models.CharField("位置", max_length=20, blank=True)
    number = models.PositiveIntegerField("球衣号码", null=True, blank=True)
    year = models.PositiveIntegerField("年份", default=2026)
    # 统计数据
    goals = models.PositiveIntegerField("进球", default=0)
    assists = models.PositiveIntegerField("助攻", default=0)
    yellow_cards = models.PositiveIntegerField("黄牌", default=0)
    red_cards = models.PositiveIntegerField("红牌", default=0)
    penalties = models.PositiveIntegerField("点球", default=0)
    shots = models.PositiveIntegerField("射门", default=0)
    shots_on_target = models.PositiveIntegerField("射正", default=0)
    dribbles = models.PositiveIntegerField("过人", default=0)
    fouls = models.PositiveIntegerField("犯规", default=0)
    fouls_suffered = models.PositiveIntegerField("被犯规", default=0)
    passes = models.PositiveIntegerField("传球", default=0)
    crosses = models.PositiveIntegerField("传中", default=0)
    tackles = models.PositiveIntegerField("抢断", default=0)
    clearances = models.PositiveIntegerField("解围", default=0)
    saves = models.PositiveIntegerField("扑救", default=0)
    market_value = models.DecimalField("身价（万元）", max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField("创建时间", auto_now_add=True)
    updated_at = models.DateTimeField("更新时间", auto_now=True)

    class Meta:
        verbose_name = "球员"
        verbose_name_plural = "球员"
        ordering = ["team", "number"]

    def __str__(self):
        return f"{self.name} - {self.team.short_name}"
