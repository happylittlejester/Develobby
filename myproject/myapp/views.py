from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from decimal import Decimal
from django.http import JsonResponse
import requests

from .forms import RegisterForm
from .models import (
    Hobby,
    HobbyDetail,
    Challenge,
    UserChallenges,
    UserStats,
    Level,
    Product,
    Subscription,
)

# ======================================================
# HOMEPAGE
# ======================================================

def homepage(request):
    if request.user.is_authenticated:
        return redirect('profile')
    return render(request, 'myapp/homepage.html')


# ======================================================
# AUTH
# ======================================================

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = RegisterForm()

    return render(request, "myapp/register.html", {"form": form})


# ======================================================
# PROFILE
# ======================================================

@login_required
def profile(request):
    user = request.user
    user_hobbies = Hobby.objects.filter(user=user)

    user_stats, _ = UserStats.objects.get_or_create(user=user)
    current_xp = user_stats.xp_total

    levels = Level.objects.all().order_by("xp_required")

    current_level = None
    next_level = None
    level_number = 0

    for i, lvl in enumerate(levels):
        if current_xp >= lvl.xp_required:
            current_level = lvl
            level_number = i + 1
            if i + 1 < len(levels):
                next_level = levels[i + 1]

    if current_level and next_level:
        xp_range = next_level.xp_required - current_level.xp_required
        xp_progress = current_xp - current_level.xp_required
        progress_percent = int((xp_progress / xp_range) * 100)
    else:
        progress_percent = 100

    progress_percent = max(0, min(progress_percent, 100))

    return render(request, "myapp/profile.html", {
        "user": user,
        "hobbies": user_hobbies,
        "current_level": current_level,
        "next_level": next_level,
        "current_xp": current_xp,
        "progress_percent": progress_percent,
        "level_number": level_number,
        "levels": levels,
    })


# ======================================================
# STORE
# ======================================================

@login_required
def store(request):
    currency = request.GET.get("currency", "PLN")
    selected_category = request.GET.get("category")

    categories = HobbyDetail.objects.all()
    products = Product.objects.all()

    if selected_category:
        try:
            products = products.filter(category_id=int(selected_category))
        except ValueError:
            selected_category = None

    rates = get_exchange_rates()
    rate = rates.get(currency, 1)

    converted_products = []
    for p in products:
        price = float(p.price or 0)
        converted_price = round(price / rate, 2) if currency != "PLN" else price
        converted_products.append({
            "name": p.name,
            "description": p.description,
            "price": converted_price,
            "category": p.category.name if p.category else "Uncategorized",
        })

    return render(request, "myapp/store.html", {
        "products": converted_products,
        "currency": currency,
        "categories": categories,
        "selected_category": selected_category,
        "rates": rates.keys(),
    })


# ======================================================
# HOBBIES
# ======================================================

@login_required
def hobby_panel(request):
    hobbies = HobbyDetail.objects.all()
    return render(request, "myapp/hobby_panel.html", {"hobbies": hobbies})


@login_required
def add_hobby_choice(request, detail_id):
    detail = HobbyDetail.objects.get(id=detail_id)

    if Hobby.objects.filter(user=request.user).count() >= 3:
        return redirect("hobby_panel")

    Hobby.objects.get_or_create(user=request.user, detail=detail)
    return redirect("hobby_panel")


@login_required
def remove_hobby_choice(request, detail_id):
    Hobby.objects.filter(user=request.user, detail_id=detail_id).delete()
    return redirect("hobby_panel")


@login_required
def hobbies(request):
    user_hobbies = request.user.hobbies.all()
    return render(request, "myapp/hobbies.html", {"hobbies": user_hobbies})


@login_required
def hobby_detail(request, detail_id):
    detail = HobbyDetail.objects.get(id=detail_id)
    challenges = Challenge.objects.filter(hobby_detail=detail)

    user_challenges = UserChallenges.objects.filter(
        user=request.user,
        challenge__in=challenges
    )

    progress_map = {uc.challenge_id: uc for uc in user_challenges}

    for ch in challenges:
        uc = progress_map.get(ch.id)
        if not uc:
            ch.user_state = "not_started"
        elif uc.completed:
            ch.user_state = "completed"
        else:
            ch.user_state = "done"

    return render(request, "myapp/hobby_detail.html", {
        "detail": detail,
        "hobbies": request.user.hobbies.all(),
        "challenges": challenges,
    })


# ======================================================
# CHALLENGES
# ======================================================

@login_required
def challenge_done(request, challenge_id):
    challenge = Challenge.objects.get(id=challenge_id)

    uc, _ = UserChallenges.objects.get_or_create(
        user=request.user,
        challenge=challenge
    )
    uc.completed = False
    uc.save()

    return redirect("hobby_detail", detail_id=challenge.hobby_detail.id)


@login_required
def challenge_collect(request, challenge_id):
    challenge = Challenge.objects.get(id=challenge_id)

    uc = UserChallenges.objects.get(
        user=request.user,
        challenge=challenge
    )

    if not uc.completed:
        uc.completed = True
        uc.completion_date = timezone.now().date()
        uc.save()

        stats, _ = UserStats.objects.get_or_create(user=request.user)
        stats.xp_total += challenge.xp_reward

        for lvl in Level.objects.all().order_by("xp_required"):
            if stats.xp_total >= lvl.xp_required:
                stats.level = lvl

        stats.save()

    return redirect("hobby_detail", detail_id=challenge.hobby_detail.id)


# ======================================================
# STATIC PAGES
# ======================================================

def faq(request):
    return render(request, "myapp/faq.html")


def coming_soon(request):
    return render(request, "myapp/coming_soon.html")


# ======================================================
# UTILS
# ======================================================

def get_exchange_rates():
    url = "https://api.nbp.pl/api/exchangerates/tables/A/?format=json"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()[0]["rates"]

        rates = {"PLN": 1}
        for r in data:
            rates[r["code"]] = r["mid"]
        return rates
    except Exception:
        return {"PLN": 1, "USD": 4, "EUR": 4.5, "GBP": 5}
