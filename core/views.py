from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import uuid
import json
import time
from decimal import Decimal
from teams.models import Team, Player
from matches.models import Match
from leagues.models import TeamStanding
from .models import News, TicketOrder, Viewer


def home(request):
    """首页：顶部按钮、新闻、积分榜"""
    news_list = News.objects.all()[:5]
    # 默认显示2026年的积分榜
    standings = TeamStanding.objects.select_related("team").filter(
        year=2026
    ).order_by(
        "-points", "-goals_for", "goals_against"
    )
    context = {
        "news_list": news_list,
        "standings": standings,
    }
    return render(request, "core/home.html", context)


@login_required(login_url="/tickets/login/")
def tickets(request):
    """购票页：列出16支球队"""
    teams = Team.objects.all()
    return render(request, "core/tickets.html", {"teams": teams})


def tickets_login(request):
    """购票登录：邮箱+密码"""
    if request.user.is_authenticated:
        return redirect("core:tickets")
    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")
        if not email or not password:
            messages.error(request, "请输入邮箱和密码")
            return render(request, "core/tickets_login.html")
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            next_url = request.GET.get("next") or "core:tickets"
            return redirect(next_url)
        messages.error(request, "邮箱或密码错误")
    return render(request, "core/tickets_login.html")


def tickets_logout(request):
    """购票登出"""
    logout(request)
    return redirect("core:home")


@login_required(login_url="/tickets/login/")
def team_tickets(request, team_id):
    """某球队的购票：下一场比赛的票档或未开票提示"""
    team = get_object_or_404(Team, pk=team_id)
    now = timezone.now()
    next_match = (
        Match.objects.filter(Q(home_team=team) | Q(away_team=team))
        .select_related("home_team", "away_team")
        .filter(match_time__gte=now)
        .order_by("match_time")
        .first()
    )
    ticket_prices = [80, 140, 260, 380] if next_match and next_match.is_tickets_open else None
    viewers = Viewer.objects.filter(user=request.user)
    context = {
        "team": team,
        "next_match": next_match,
        "ticket_prices": ticket_prices,
        "viewers": viewers,
    }
    return render(request, "core/team_tickets.html", context)


def schedule(request):
    """赛程页：按时间顺序展示中超全部比赛"""
    # 获取年份参数，默认为2026
    try:
        year = int(request.GET.get('year', 2026))
        if year < 1994 or year > 2026:
            year = 2026
    except (ValueError, TypeError):
        year = 2026
    years = list(range(1994, 2027))
    
    # 根据年份过滤比赛：只显示该年份的比赛
    from django.db.models import Q
    matches = Match.objects.select_related("home_team", "away_team").filter(
        match_time__year=year
    ).order_by("match_time")
    
    context = {
        "matches": matches,
        "years": years,
        "current_year": year,
    }
    return render(request, "core/schedule.html", context)


def team_standings(request):
    """球队榜"""
    # 获取年份参数，默认为2026
    try:
        year = int(request.GET.get('year', 2026))
        if year < 1994 or year > 2026:
            year = 2026
    except (ValueError, TypeError):
        year = 2026
    years = list(range(1994, 2027))
    
    # #region agent log
    import json
    log_data = {
        "sessionId": "cb5851",
        "runId": "initial",
        "hypothesisId": "A",
        "location": "core/views.py:126",
        "message": "年份参数值",
        "data": {"year": year, "year_from_request": request.GET.get('year', 'default')},
        "timestamp": int(time.time() * 1000)
    }
    try:
        with open('/Users/yaccyan/Desktop/Django/soccer_admin/.cursor/debug-cb5851.log', 'a') as f:
            f.write(json.dumps(log_data) + '\n')
    except:
        pass
    # #endregion
    
    standings = TeamStanding.objects.select_related("team").filter(
        year=year
    ).order_by(
        "-points", "-goals_for", "goals_against"
    )
    
    # #region agent log
    log_data2 = {
        "sessionId": "cb5851",
        "runId": "initial",
        "hypothesisId": "B",
        "location": "core/views.py:140",
        "message": "查询结果数量",
        "data": {"count": standings.count(), "year": year},
        "timestamp": int(time.time() * 1000)
    }
    try:
        with open('/Users/yaccyan/Desktop/Django/soccer_admin/.cursor/debug-cb5851.log', 'a') as f:
            f.write(json.dumps(log_data2) + '\n')
    except:
        pass
    # #endregion
    # 为各个统计项创建排序后的列表
    standings_list = list(standings)
    standings_by_goals_for = sorted(standings_list, key=lambda x: x.goals_for, reverse=True)
    standings_by_goals_against = sorted(standings_list, key=lambda x: x.goals_against)
    standings_by_assists = sorted(standings_list, key=lambda x: x.assists, reverse=True)
    standings_by_yellow_cards = sorted(standings_list, key=lambda x: x.yellow_cards, reverse=True)
    standings_by_red_cards = sorted(standings_list, key=lambda x: x.red_cards, reverse=True)
    standings_by_penalties = sorted(standings_list, key=lambda x: x.penalties, reverse=True)
    standings_by_shots = sorted(standings_list, key=lambda x: x.shots, reverse=True)
    standings_by_shots_on_target = sorted(standings_list, key=lambda x: x.shots_on_target, reverse=True)
    standings_by_offsides = sorted(standings_list, key=lambda x: x.offsides, reverse=True)
    standings_by_corners = sorted(standings_list, key=lambda x: x.corners, reverse=True)
    standings_by_passes = sorted(standings_list, key=lambda x: x.passes, reverse=True)
    standings_by_fouls = sorted(standings_list, key=lambda x: x.fouls, reverse=True)
    standings_by_saves = sorted(standings_list, key=lambda x: x.saves, reverse=True)
    
    context = {
        "standings": standings,
        "standings_by_goals_for": standings_by_goals_for,
        "standings_by_goals_against": standings_by_goals_against,
        "standings_by_assists": standings_by_assists,
        "standings_by_yellow_cards": standings_by_yellow_cards,
        "standings_by_red_cards": standings_by_red_cards,
        "standings_by_penalties": standings_by_penalties,
        "standings_by_shots": standings_by_shots,
        "standings_by_shots_on_target": standings_by_shots_on_target,
        "standings_by_offsides": standings_by_offsides,
        "standings_by_corners": standings_by_corners,
        "standings_by_passes": standings_by_passes,
        "standings_by_fouls": standings_by_fouls,
        "standings_by_saves": standings_by_saves,
        "years": years,
        "current_year": year,
    }
    return render(request, "core/team_standings.html", context)


def player_rankings(request):
    """球员榜"""
    # 获取年份参数，默认为2026
    try:
        year = int(request.GET.get('year', 2026))
        if year < 1994 or year > 2026:
            year = 2026
    except (ValueError, TypeError):
        year = 2026
    years = list(range(1994, 2027))
    
    players = Player.objects.select_related("team").filter(year=year).all()
    players_list = list(players)
    
    # 为各个统计项创建排序后的列表，过滤掉总计为0的数据，只取前100条
    def get_sorted_players(key_func, filter_func):
        """辅助函数：排序并过滤球员列表"""
        return [p for p in sorted(players_list, key=key_func, reverse=True) if filter_func(p)][:100]
    
    players_by_goals = get_sorted_players(lambda p: p.goals, lambda p: p.goals > 0)
    players_by_assists = get_sorted_players(lambda p: p.assists, lambda p: p.assists > 0)
    players_by_yellow_cards = get_sorted_players(lambda p: p.yellow_cards, lambda p: p.yellow_cards > 0)
    players_by_red_cards = get_sorted_players(lambda p: p.red_cards, lambda p: p.red_cards > 0)
    players_by_penalties = get_sorted_players(lambda p: p.penalties, lambda p: p.penalties > 0)
    players_by_shots = get_sorted_players(lambda p: p.shots, lambda p: p.shots > 0)
    players_by_shots_on_target = get_sorted_players(lambda p: p.shots_on_target, lambda p: p.shots_on_target > 0)
    players_by_dribbles = get_sorted_players(lambda p: p.dribbles, lambda p: p.dribbles > 0)
    players_by_fouls = get_sorted_players(lambda p: p.fouls, lambda p: p.fouls > 0)
    players_by_fouls_suffered = get_sorted_players(lambda p: p.fouls_suffered, lambda p: p.fouls_suffered > 0)
    players_by_passes = get_sorted_players(lambda p: p.passes, lambda p: p.passes > 0)
    players_by_crosses = get_sorted_players(lambda p: p.crosses, lambda p: p.crosses > 0)
    players_by_tackles = get_sorted_players(lambda p: p.tackles, lambda p: p.tackles > 0)
    players_by_clearances = get_sorted_players(lambda p: p.clearances, lambda p: p.clearances > 0)
    players_by_saves = get_sorted_players(lambda p: p.saves, lambda p: p.saves > 0)
    players_by_market_value = get_sorted_players(lambda p: float(p.market_value), lambda p: float(p.market_value) > 0)
    
    context = {
        "players_by_goals": players_by_goals,
        "players_by_assists": players_by_assists,
        "players_by_yellow_cards": players_by_yellow_cards,
        "players_by_red_cards": players_by_red_cards,
        "players_by_penalties": players_by_penalties,
        "players_by_shots": players_by_shots,
        "players_by_shots_on_target": players_by_shots_on_target,
        "players_by_dribbles": players_by_dribbles,
        "players_by_fouls": players_by_fouls,
        "players_by_fouls_suffered": players_by_fouls_suffered,
        "players_by_passes": players_by_passes,
        "players_by_crosses": players_by_crosses,
        "players_by_tackles": players_by_tackles,
        "players_by_clearances": players_by_clearances,
        "players_by_saves": players_by_saves,
        "players_by_market_value": players_by_market_value,
        "years": years,
        "current_year": year,
    }
    return render(request, "core/player_rankings.html", context)


@login_required(login_url="/tickets/login/")
@require_http_methods(["POST"])
def add_viewer(request):
    """添加观影人"""
    try:
        name = request.POST.get("name", "").strip()
        id_card = request.POST.get("id_card", "").strip()
        phone = request.POST.get("phone", "").strip()
        if not name or not id_card or not phone:
            return JsonResponse({"success": False, "message": "请填写完整信息"})
        if Viewer.objects.filter(user=request.user, id_card=id_card).exists():
            return JsonResponse({"success": False, "message": "该身份证号已存在"})
        viewer = Viewer.objects.create(user=request.user, name=name, id_card=id_card, phone=phone)
        return JsonResponse({
            "success": True,
            "viewer": {"id": viewer.id, "name": viewer.name, "id_card": viewer.id_card, "phone": viewer.phone},
        })
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)})


@login_required(login_url="/tickets/login/")
@require_http_methods(["POST"])
def edit_viewer(request, viewer_id):
    """编辑观影人"""
    try:
        viewer = get_object_or_404(Viewer, pk=viewer_id, user=request.user)
        name = request.POST.get("name", "").strip()
        id_card = request.POST.get("id_card", "").strip()
        phone = request.POST.get("phone", "").strip()
        if not name or not id_card or not phone:
            return JsonResponse({"success": False, "message": "请填写完整信息"})
        if Viewer.objects.filter(user=request.user, id_card=id_card).exclude(pk=viewer_id).exists():
            return JsonResponse({"success": False, "message": "该身份证号已被其他观影人使用"})
        viewer.name = name
        viewer.id_card = id_card
        viewer.phone = phone
        viewer.save()
        return JsonResponse({
            "success": True,
            "viewer": {"id": viewer.id, "name": viewer.name, "id_card": viewer.id_card, "phone": viewer.phone},
        })
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)})


@login_required(login_url="/tickets/login/")
@require_http_methods(["POST"])
def delete_viewer(request, viewer_id):
    """删除观影人"""
    try:
        viewer = get_object_or_404(Viewer, pk=viewer_id, user=request.user)
        viewer.delete()
        return JsonResponse({"success": True})
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)})


@login_required(login_url="/tickets/login/")
@require_http_methods(["POST"])
def create_order(request):
    """创建购票订单"""
    try:
        match_id = request.POST.get("match_id")
        ticket_price = int(request.POST.get("ticket_price"))
        ticket_count = int(request.POST.get("ticket_count", 1))
        viewer_id = request.POST.get("viewer_id", "").strip()
        id_card = request.POST.get("id_card", "").strip()
        phone = request.POST.get("phone", "").strip()

        if viewer_id:
            viewer = get_object_or_404(Viewer, pk=viewer_id, user=request.user)
            id_card, phone = viewer.id_card, viewer.phone

        if not match_id or not ticket_price or not id_card or not phone:
            return JsonResponse({"success": False, "message": "请选择观影人或填写完整信息"})

        match = get_object_or_404(Match, pk=match_id)
        if not match.tickets_open:
            return JsonResponse({"success": False, "message": "该场比赛尚未开票"})

        total_amount = Decimal(str(ticket_price * ticket_count))
        order_number = f"T{timezone.now().strftime('%Y%m%d%H%M%S')}{uuid.uuid4().hex[:8].upper()}"

        order = TicketOrder.objects.create(
            user=request.user,
            match=match,
            ticket_price=ticket_price,
            ticket_count=ticket_count,
            id_card=id_card,
            phone=phone,
            total_amount=total_amount,
            order_number=order_number,
        )

        return JsonResponse({
            "success": True,
            "order_id": order.id,
            "order_number": order_number,
            "total_amount": str(total_amount),
        })
    except Exception as e:
        return JsonResponse({"success": False, "message": f"创建订单失败：{str(e)}"})


@login_required(login_url="/tickets/login/")
def payment_qr(request, order_number):
    """显示支付二维码页面"""
    order = get_object_or_404(TicketOrder, order_number=order_number, user=request.user)
    qr_data = json.loads(order.payment_qr_code) if order.payment_qr_code else {}
    return render(request, "core/payment_qr.html", {
        "order": order,
        "qr_url": qr_data.get("url", ""),
    })


@login_required(login_url="/tickets/login/")
@require_http_methods(["POST"])
def confirm_payment(request, order_number):
    """确认支付（模拟支付成功）"""
    order = get_object_or_404(TicketOrder, order_number=order_number, user=request.user)
    if order.status == "paid":
        return JsonResponse({"success": False, "message": "订单已支付"})
    
    order.status = "paid"
    order.paid_at = timezone.now()
    order.save()
    
    return JsonResponse({"success": True, "message": "支付成功！"})


@login_required(login_url="/tickets/login/")
def payment_success(request, order_number):
    """支付成功页面"""
    order = get_object_or_404(TicketOrder, order_number=order_number, user=request.user)
    return render(request, "core/payment_success.html", {"order": order})

