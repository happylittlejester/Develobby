from django.shortcuts import render, redirect, get_object_or_404
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
)

# =========================
# HOMEPAGE
# =========================
def homepage(request):
    if request.user.is_authenticated:
        return redirect("profile")
    return render(request, "myapp/homepage.html")


# =========================
# AUTH
# =========================
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = RegisterForm()
    return render(request, "myapp/register.html", {"form": form})


# =========================
# PROFILE
# =========================
@login_required
def profile(request):
    user = request.user

    hobbies = (
        Hobby.objects
        .filter(user=user)
        .select_related("detail")
    )

    # 🔹 IKONY
    HOBBY_ICONS = {
        "Cooking": "fi fi-rr-hat-chef",
        "Drawing": "fi fi-rr-drawer-alt",
        "Coding": "fi fi-rr-square-terminal",
        "Music": "fi fi-rr-music-alt",
        "Fitness": "fi fi-tr-dumbbell-ray",
    }

    for hobby in hobbies:
        hobby.icon = HOBBY_ICONS.get(hobby.detail.name, "fi fi-rr-star")

        challenges = Challenge.objects.filter(hobby_detail=hobby.detail)
        total = challenges.count()

        completed = UserChallenges.objects.filter(
            user=user,
            challenge__in=challenges,
            completed=True
        ).count()

        hobby.progress = int((completed / total) * 100) if total > 0 else 0

    # 🔹 XP / LEVEL
    stats, _ = UserStats.objects.get_or_create(user=user)
    current_xp = stats.xp_total

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

    # 🔑 DOMYŚLNE WARTOŚCI (NAJWAŻNIEJSZE)
    progress_percent = 100
    xp_color = "xp-high"

    if current_level and next_level:
        xp_range = next_level.xp_required - current_level.xp_required
        xp_progress = current_xp - current_level.xp_required
        progress_percent = int((xp_progress / xp_range) * 100)
        progress_percent = max(0, min(progress_percent, 100))

    return render(request, "myapp/profile.html", {
        "user": user,
        "hobbies": hobbies,
        "current_level": current_level,
        "next_level": next_level,
        "current_xp": current_xp,
        "progress_percent": progress_percent,
        "level_number": level_number,
        "levels": levels,
        "xp_color": xp_color,
    })


# =========================
# UPGRADE
# =========================
def upgrade(request):
    currency = request.GET.get("currency", "USD")

    base_prices = {
        "student": Decimal("5"),
        "premium": Decimal("10"),
    }

    currency_symbols = {"USD": "$", "EUR": "€", "GBP": "£", "PLN": "zł"}
    rates = get_exchange_rates()
    usd_to_pln = Decimal(str(rates["USD"]))

    final_prices = {}
    for name, usd_price in base_prices.items():
        pln_value = usd_price * usd_to_pln

        if currency == "PLN":
            final = pln_value
        else:
            final = pln_value / Decimal(str(rates[currency]))

        final_prices[name] = round(final, 2)

    if request.headers.get("X-Requested-With") == "XMLHttpRequest": 
        return JsonResponse({ 
            "currency": currency, 
            "currency_symbol": currency_symbols[currency], 
            "student_price": final_prices["student"], 
            "premium_price": final_prices["premium"], 
        })

    return render(request, "myapp/upgrade.html", {
        "currency": currency,
        "currency_symbol": currency_symbols.get(currency, currency),
        "student_price": final_prices["student"],
        "premium_price": final_prices["premium"],
    })


# =========================
# STORE
# =========================
@login_required
def store(request):
    currency = request.GET.get("currency", "USD")
    products = Product.objects.all()

    # Ikony
    ICON_MAP = {
        "Coding": "fi fi-brands-python",
        "Drawing": "fi fi-sr-artist",
        "Music": "fi fi-sr-list-music",
        "Cooking": "fi fi-rs-recipe-book",
        "Fitness": "fi fi-sr-person-lunge",
    }

    rates = get_exchange_rates()

    currency_symbols = {
        "USD": "$",
        "EUR": "€",
        "GBP": "£",
        "PLN": "zł",
    }

    usd_to_pln = Decimal(str(rates["USD"]))

    selected_category = request.GET.get("category")

    if selected_category and selected_category != "All":
        products = products.filter(category__name=selected_category)

    converted_products = []

    for p in products:
        usd_price = Decimal(str(p.price))
        pln_value = usd_price * usd_to_pln

        if currency == "PLN":
            final = pln_value
        else:
            final = pln_value / Decimal(str(rates[currency]))

        converted_products.append({
            "name": p.name,
            "description": p.description,
            "price": round(final, 2),
            "category": p.category.name if p.category else "Uncategorized",
            "icon": ICON_MAP.get(p.category.name if p.category else "", "fi fi-rr-box"),
        })

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return JsonResponse({
            "currency": currency,
            "currency_symbol": currency_symbols[currency],
            "products": converted_products,
        })

    return render(request, "myapp/store.html", {
        "products": converted_products,
        "currency": currency,
        "currency_symbol": currency_symbols[currency],
        "rates": rates.keys(),
    })


# =========================
# HOBBIES
# =========================
@login_required
def hobby_panel(request):
    hobbies = HobbyDetail.objects.all()

    HOBBY_ICONS = {
        "Cooking": "fi fi-rr-hat-chef",
        "Drawing": "fi fi-rr-drawer-alt",
        "Coding": "fi fi-rr-square-terminal",
        "Music": "fi fi-rr-music-alt",
        "Fitness": "fi fi-sr-person-lunge",
    }

    for hobby in hobbies:
        hobby.icon = HOBBY_ICONS.get(hobby.name, "fi fi-rr-star")

    return render(request, "myapp/hobby_panel.html", {
        "hobbies": hobbies
    })



@login_required
def add_hobby_choice(request, detail_id):
    detail = get_object_or_404(HobbyDetail, id=detail_id)

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
    hobbies = request.user.hobbies.all().select_related("detail")

    HOBBY_ICONS = {
        "Cooking": "fi fi-rr-hat-chef",
        "Drawing": "fi fi-rr-drawer-alt",
        "Coding": "fi fi-rr-square-terminal",
        "Music": "fi fi-rr-music-alt",
        "Fitness": "fi fi-tr-dumbbell-ray",
    }

    for h in hobbies:
        h.detail.icon = HOBBY_ICONS.get(h.detail.name, "fi fi-rr-star")  # fallback

    return render(request, "myapp/hobbies.html", {
        "hobbies": hobbies
    })


# =========================
# HOBBY DETAIL
# =========================
@login_required
def hobby_detail(request, detail_id):
    detail = get_object_or_404(HobbyDetail, id=detail_id)
    challenges = Challenge.objects.filter(hobby_detail=detail)

    HOBBY_BANNERS = {
        "Cooking": "hobby_cooking.png",
        "Drawing": "hobby_drawing.png",
        "Coding": "hobby_coding.png",
        "Music": "hobby_music.png",
        "Fitness": "hobby_fitness.png",
    }

    # IKONY
    HOBBY_ICONS = {
        "Cooking": "fi fi-rr-hat-chef",
        "Drawing": "fi fi-rr-drawer-alt",
        "Coding": "fi fi-rr-square-terminal",
        "Music": "fi fi-rr-music-alt",
        "Fitness": "fi fi-tr-dumbbell-ray",
    }

    CHALLENGE_ICONS = {
        # Cooking
        "Thai Cuisine": "fi fi-sr-bowl-chopsticks-noodles",
        "Spanish Sweets": "fi fi-sr-candy",
        "Paprika Dish": "fi fi-sr-pepper-alt",
        "Green Plate": "fi fi-sr-salad",
        "Chicken In 5 Ways": "fi fi-sr-turkey",

        # Drawing
        "Basic Shapes": "fi fi-ss-resources",
        "Still Life Study": "fi fi-sr-apple-whole",
        "Texture Practice": "fi fi-br-fabric",
        "Gesture Sketching": "fi fi-sr-transporter",
        "14 Days Drawing Challenge": "fi fi-br-paintbrush-pencil",

        # Coding
        "Simple Calculator": "fi fi-br-calculator",
        "Data Structures Practice": "fi fi-sr-folder-open",
        "Calendar": "fi fi-br-calendar-day",
        "Rock, Paper, Scissors": "fi fi-sc-gamepad",
        "Roman to Arabic Converter": "fi fi-sr-pillar",

        # Music
        "Rhythm Foundations": "fi fi-sr-headphones-rhythm",
        "Chill Lo-Fi Vibes": "fi fi-sr-circle-waveform-lines",
        "Sound Collector": "fi fi-sr-microphone",
        "Music for Motion": "fi fi-rr-film",
        "Latin Heat": "fi fi-rs-temperature-high",

        # Fitness
        "Warm-Up Essentials": "fi fi-br-yoga-moon",
        "Cardio Exploration": "fi fi-br-treadmill",
        "Build Endurance": "fi fi-rr-dumbbell-weightlifting",
        "Dumbbell Training": "fi fi-sr-gym",
        "Mobility Improvement": "fi fi-br-meditation",
    }

    detail.banner = HOBBY_BANNERS.get(detail.name, "default_banner.png")

    # ikona aktualnego hobby
    detail.icon = HOBBY_ICONS.get(detail.name, "bi bi-star")

    # ikony challenges
    for ch in challenges:
        ch.icon = CHALLENGE_ICONS.get(ch.title, "bi bi-circle-half")

    hobbies = request.user.hobbies.all()

    # ikony hobby w pasku
    for h in hobbies:
        h.detail.icon = HOBBY_ICONS.get(h.detail.name, "bi bi-star")

    # user progress
    user_challenges = UserChallenges.objects.filter(
        user=request.user,
        challenge__in=challenges
    )

    progress_map = {uc.challenge_id: uc for uc in user_challenges}

    for ch in challenges:
        uc = progress_map.get(ch.id)
        if uc is None:
            ch.user_state = "not_started"
        elif uc.completed:
            ch.user_state = "completed"
        else:
            ch.user_state = "done"

    total = challenges.count()
    completed = len([c for c in challenges if c.user_state == "completed"])
    percent = int((completed / total) * 100) if total > 0 else 0

    return render(request, "myapp/hobby_detail.html", {
        "detail": detail,
        "challenges": challenges,
        "hobbies": hobbies,
        "completed": completed,
        "total": total,
        "percent": percent,
    })


# =========================
# CHALLENGES
# =========================
@login_required
def challenge_done(request, challenge_id):
    challenge = get_object_or_404(Challenge, id=challenge_id)
    uc, _ = UserChallenges.objects.get_or_create(
        user=request.user,
        challenge=challenge
    )
    uc.completed = False
    uc.save()
    return redirect("hobby_detail", detail_id=challenge.hobby_detail.id)


@login_required
def challenge_collect(request, challenge_id):
    challenge = get_object_or_404(Challenge, id=challenge_id)
    uc = UserChallenges.objects.get(user=request.user, challenge=challenge)

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
    


# =========================
# STATIC
# =========================
def faq(request):
    return render(request, "myapp/faq.html")


def coming_soon(request):
    return render(request, "myapp/coming_soon.html")


# =========================
# UTILS
# =========================
def get_exchange_rates():
    try:
        r = requests.get(
            "https://api.nbp.pl/api/exchangerates/tables/A/?format=json",
            timeout=5
        )
        data = r.json()[0]["rates"]
        rates = {"PLN": 1}
        for x in data:
            rates[x["code"]] = x["mid"]
        return rates
    except Exception:
        return {"PLN": 1, "USD": 4, "EUR": 4.5, "GBP": 5}
