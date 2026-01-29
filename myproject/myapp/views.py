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




def homepage(request):
    return render(request, 'myapp/homepage.html')


def upgrade(request):
    currency = request.GET.get("currency", "USD")

    # Ceny subskrypcji w USD
    base_prices = {
        "student": Decimal("5"),
        "premium": Decimal("10"),
    }

    currency_symbols = { "USD": "$", "EUR": "€", "GBP": "£", "PLN": "zł", }

    rates = get_exchange_rates()  # NBP → kursy do PLN
    usd_to_pln = Decimal(str(rates["USD"]))

    final_prices = {}

    for name, usd_price in base_prices.items():
        # USD → PLN
        pln_value = usd_price * usd_to_pln

        # PLN → wybrana waluta
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


def faq(request):
    return render(request, 'myapp/faq.html')


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = RegisterForm()

    return render(request, "myapp/register.html", {"form": form})


@login_required
def profile(request):
    user_hobbies = Hobby.objects.filter(user=request.user)

    user_stats, _ = UserStats.objects.get_or_create(user=request.user)
    current_xp = user_stats.xp_total

    levels = Level.objects.all().order_by('xp_required')
    current_level = None
    next_level = None
    level_number = None

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

    return render(request, 'myapp/profile.html', {
        "hobbies": user_hobbies,
        "current_level": current_level,
        "next_level": next_level,
        "current_xp": current_xp,
        "progress_percent": progress_percent,
        "level_number": level_number,
    })


def get_exchange_rates():
    """
    Pobiera kursy walut z NBP API.
    """
    url = "https://api.nbp.pl/api/exchangerates/tables/A/?format=json"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()[0]["rates"]

        rates = {"PLN": 1}
        for r in data:
            rates[r["code"]] = r["mid"]
        return rates

    except (requests.RequestException, KeyError, IndexError):
        return {"PLN": 1, "USD": 4, "EUR": 4.5, "GBP": 5}


@login_required
def store(request):
    currency = request.GET.get("currency", "PLN")
    selected_category = request.GET.get("category")

    categories = HobbyDetail.objects.all()
    products = Product.objects.all()

    # Filtracja po kategorii
    if selected_category:
        try:
            selected_category = int(selected_category)
            products = products.filter(category_id=selected_category)
        except ValueError:
            selected_category = None  # jeśli GET był niepoprawny

    # Pobranie kursów walut
    rates = get_exchange_rates()
    rate = rates.get(currency)
    safe_rate = float(rate) if rate else 1  # bezpieczne dzielenie

    # Konwersja cen
    converted_products = []
    for p in products:
        price = float(p.price or 0)
        converted_price = round(price / safe_rate, 2) if currency != "PLN" else price
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


def logout_view(request):
    logout(request)
    return redirect('homepage')


def coming_soon(request):
    return render(request, "myapp/coming_soon.html")


@login_required
def hobby_panel(request):
    hobby_details = HobbyDetail.objects.all()
    return render(request, "myapp/hobby_panel.html", {"hobbies": hobby_details})


@login_required
def add_hobby_choice(request, detail_id):
    detail = HobbyDetail.objects.get(id=detail_id)

    current_count = Hobby.objects.filter(user=request.user).count()
    if current_count >= 3:
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
    return render(request, 'myapp/hobbies.html', {"hobbies": user_hobbies})


@login_required
def hobby_detail(request, detail_id):
    detail = HobbyDetail.objects.get(id=detail_id)
    challenges = Challenge.objects.filter(hobby_detail=detail)

    user_hobbies = request.user.hobbies.all()
    user_challenges = UserChallenges.objects.filter(
        user=request.user,
        challenge__in=challenges
    )

    progress_map = {uc.challenge.id: uc for uc in user_challenges}

    for ch in challenges:
        uc = progress_map.get(ch.id)

        if uc is None:
            ch.user_state = "not_started"
        elif uc.completed:
            ch.user_state = "completed"
        else:
            ch.user_state = "done"

    return render(request, "myapp/hobby_detail.html", {
        "detail": detail,
        "hobbies": user_hobbies,
        "challenges": challenges,
    })


@login_required
def challenge_done(request, challenge_id):
    challenge = Challenge.objects.get(id=challenge_id)

    user_challenge, _ = UserChallenges.objects.get_or_create(
        user=request.user,
        challenge=challenge
    )

    user_challenge.completed = False
    user_challenge.save()

    return redirect('hobby_detail', detail_id=challenge.hobby_detail.id)


@login_required
def challenge_collect(request, challenge_id):
    challenge = Challenge.objects.get(id=challenge_id)

    user_challenge = UserChallenges.objects.get(
        user=request.user,
        challenge=challenge
    )

    if not user_challenge.completed:
        user_challenge.completed = True
        user_challenge.completion_date = timezone.now().date()
        user_challenge.save()

        user_stats, _ = UserStats.objects.get_or_create(user=request.user)
        user_stats.xp_total += challenge.xp_reward

        levels = Level.objects.all().order_by('xp_required')
        new_level = None
        for lvl in levels:
            if user_stats.xp_total >= lvl.xp_required:
                new_level = lvl

        if new_level:
            user_stats.level = new_level

        user_stats.save()

    return redirect('hobby_detail', detail_id=challenge.hobby_detail.id)
