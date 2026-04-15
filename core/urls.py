from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    path("tickets/", views.tickets, name="tickets"),
    path("tickets/login/", views.tickets_login, name="tickets_login"),
    path("tickets/logout/", views.tickets_logout, name="tickets_logout"),
    path("tickets/team/<int:team_id>/", views.team_tickets, name="team_tickets"),
    path("tickets/viewers/add/", views.add_viewer, name="add_viewer"),
    path("tickets/viewers/<int:viewer_id>/edit/", views.edit_viewer, name="edit_viewer"),
    path("tickets/viewers/<int:viewer_id>/delete/", views.delete_viewer, name="delete_viewer"),
    path("tickets/order/create/", views.create_order, name="create_order"),
    path("tickets/pay/<str:order_number>/", views.payment_qr, name="payment_qr"),
    path("tickets/pay/<str:order_number>/confirm/", views.confirm_payment, name="confirm_payment"),
    path("tickets/success/<str:order_number>/", views.payment_success, name="payment_success"),
    path("schedule/", views.schedule, name="schedule"),
    path("standings/", views.team_standings, name="team_standings"),
    path("players/", views.player_rankings, name="player_rankings"),
]
