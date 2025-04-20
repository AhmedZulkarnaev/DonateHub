from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Collect(models.Model):
    class Reason(models.TextChoices):
        BIRTHDAY = "birthday", "День рождения"
        WEDDING = "wedding", "Свадьба"
        OTHER = "other", "Другое"

    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="collects"
    )
    title = models.CharField(max_length=255)
    reason = models.CharField(max_length=20, choices=Reason.choices)
    description = models.TextField(blank=True)
    cover_image = models.ImageField(upload_to="collect_covers/")
    goal_amount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    is_infinite = models.BooleanField(default=False)
    collected_amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0
    )
    donators_count = models.PositiveIntegerField(default=0)
    ends_at = models.DateTimeField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.author})"


class Payment(models.Model):
    collect = models.ForeignKey(
        Collect, on_delete=models.CASCADE, related_name="payments"
    )
    donator = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="payments"
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.donator} → {self.collect}: {self.amount}"
