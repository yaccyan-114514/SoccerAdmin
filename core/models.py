from django.db import models
from django.contrib.auth.models import User
from matches.models import Match


class News(models.Model):
    """比赛新闻"""

    title = models.CharField("标题", max_length=200)
    summary = models.CharField("摘要", max_length=300, blank=True)
    content = models.TextField("内容", blank=True)
    published_at = models.DateTimeField("发布时间", auto_now_add=True)
    created_at = models.DateTimeField("创建时间", auto_now_add=True)

    class Meta:
        verbose_name = "新闻"
        verbose_name_plural = "新闻"
        ordering = ["-published_at"]

    def __str__(self):
        return self.title


class TicketOrder(models.Model):
    """购票订单"""

    STATUS_CHOICES = [
        ("pending", "待支付"),
        ("paid", "已支付"),
        ("cancelled", "已取消"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")
    match = models.ForeignKey(Match, on_delete=models.CASCADE, verbose_name="比赛")
    ticket_price = models.PositiveIntegerField("票档价格")
    ticket_count = models.PositiveIntegerField("购票张数", default=1)
    id_card = models.CharField("身份证号", max_length=18)
    phone = models.CharField("手机号", max_length=11)
    total_amount = models.DecimalField("总金额", max_digits=10, decimal_places=2)
    order_number = models.CharField("订单号", max_length=32, unique=True)
    status = models.CharField("订单状态", max_length=20, choices=STATUS_CHOICES, default="pending")
    payment_qr_code = models.TextField("支付二维码数据", blank=True)
    created_at = models.DateTimeField("创建时间", auto_now_add=True)
    paid_at = models.DateTimeField("支付时间", null=True, blank=True)

    class Meta:
        verbose_name = "购票订单"
        verbose_name_plural = "购票订单"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.order_number} - {self.user.username}"


class Viewer(models.Model):
    """观影人"""

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")
    name = models.CharField("姓名", max_length=50)
    id_card = models.CharField("身份证号", max_length=18)
    phone = models.CharField("手机号", max_length=11)
    created_at = models.DateTimeField("创建时间", auto_now_add=True)

    class Meta:
        verbose_name = "观影人"
        verbose_name_plural = "观影人"
        ordering = ["-created_at"]
        unique_together = [["user", "id_card"]]

    def __str__(self):
        return f"{self.name} - {self.phone}"
