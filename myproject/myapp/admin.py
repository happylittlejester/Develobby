from django.contrib import admin
from .models import HobbyDetail, Hobby, Level, Challenge, UserStats, UserChallenges, Product, Subscription


# HOBBY DETAIL
@admin.register(HobbyDetail)
class HobbyDetailAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
    list_filter = ('name',)


# HOBBY
@admin.register(Hobby)
class HobbyAdmin(admin.ModelAdmin):
    list_display = ('user', 'detail')
    list_filter = ('detail', 'user')
    search_fields = ('user__username', 'detail__name')


# LEVEL
@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = ('level_number_and_title', 'xp_required')  # zmienione
    list_editable = ('xp_required',)
    search_fields = ('title',)
    ordering = ('xp_required',)

    def level_number_and_title(self, obj):
        all_levels = list(Level.objects.all().order_by('xp_required'))
        level_number = all_levels.index(obj) + 1
        return f"Level {level_number}: {obj.title}"

    level_number_and_title.short_description = 'Level'


# CHALLENGE
@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    list_display = ('title', 'xp_reward', 'hobby_detail')
    list_filter = ('hobby_detail',)
    search_fields = ('title', 'hobby_detail__name')
    list_editable = ('xp_reward',)


# USER STATS
@admin.register(UserStats)
class UserStatsAdmin(admin.ModelAdmin):
    list_display = ('user', 'level', 'xp_total')
    list_filter = ('level',)
    search_fields = ('user__username',)
    list_editable = ('xp_total',)


# USER CHALLENGES
@admin.register(UserChallenges)
class UserChallengesAdmin(admin.ModelAdmin):
    list_display = ('user', 'challenge', 'completed', 'completion_date')
    list_filter = ('completed', 'challenge', 'challenge__hobby_detail')
    search_fields = ('user__username', 'challenge__title')
    list_editable = ('completed', 'completion_date')
    ordering = ('user',)


# PRODUCT
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category')
    list_filter = ('category',)
    search_fields = ('name', 'category__name')


# SUBSCRIPTION
@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'duration_days')
    list_filter = ('duration_days', 'price')
    search_fields = ('name',)
