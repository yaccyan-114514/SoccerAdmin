from django.contrib import admin
from .models import News, TicketOrder, Viewer


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ["title", "published_at"]
    list_filter = ["published_at"]
    search_fields = ["title", "summary", "content"]


@admin.register(TicketOrder)
class TicketOrderAdmin(admin.ModelAdmin):
    list_display = ["order_number", "user", "match", "ticket_price", "ticket_count", "total_amount", "status", "created_at"]
    list_filter = ["status", "created_at"]
    search_fields = ["order_number", "user__username", "id_card", "phone"]
    readonly_fields = ["order_number", "created_at", "paid_at"]


@admin.register(Viewer)
class ViewerAdmin(admin.ModelAdmin):
    list_display = ["name", "id_card", "phone", "user", "created_at"]
    list_filter = ["user"]
    search_fields = ["name", "id_card", "phone"]
