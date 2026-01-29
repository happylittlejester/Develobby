from django.db import models
from django.contrib.auth.models import User


class HobbyDetail(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name


class Hobby(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="hobbies")
    detail = models.ForeignKey(HobbyDetail, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} – {self.detail.name}"


class Level(models.Model):
    title = models.CharField(max_length=100, unique=True)
    xp_required = models.PositiveIntegerField()

    class Meta:
        ordering = ['xp_required']

    def __str__(self):
        return f"{self.title} ({self.xp_required} XP)"


class Challenge(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    xp_reward = models.PositiveIntegerField()
    hobby_detail = models.ForeignKey(HobbyDetail, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} – {self.xp_reward} XP"


class Subscription(models.Model):
    name = models.CharField(max_length=100, unique=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    duration_days = models.PositiveIntegerField(default=30)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class UserStats(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.SET_NULL, null=True)
    xp_total = models.PositiveIntegerField(default=0)

    subscription = models.ForeignKey(
        Subscription,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    subscription_expiry = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} – {self.xp_total} XP"


class UserChallenges(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    completion_date = models.DateField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'challenge')

    def __str__(self):
        return f"{self.user.username} – {self.challenge.title}"


class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    category = models.ForeignKey(
        HobbyDetail,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="products"
    )

    def __str__(self):
        return self.name