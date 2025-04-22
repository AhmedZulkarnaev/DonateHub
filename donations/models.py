from django.db import models
from django.contrib.auth import get_user_model

from .constants import MAX_DIGITS, DECIMAL_PLACES

User = get_user_model()


class Collect(models.Model):
    """
    Модель для хранения информации о сборе средств.

    Поля:
    - author: Пользователь, создавший сбор.
    - title: Название сбора.
    - reason: Причина создания (например, День рождения, Свадьба или Другое).
    - description: Дополнительное описание сбора.
    - cover_image: Изображение-обложка, сохраняемое в 'collect_covers/'.
    - goal_amount: Целевая сумма (опционально, если сбор бесконечный).
    - is_infinite: Флаг, указывающий на бесконечный сбор.
    - collected_amount: Текущая сумма собранных средств.
    - donators_count: Количество уникальных донаторов.
    - ends_at: Дата и время завершения сбора.
    - created_at: Дата и время создания записи.
    """

    class Reason(models.TextChoices):
        BIRTHDAY = "birthday", "День рождения"
        WEDDING = "wedding", "Свадьба"
        OTHER = "other", "Другое"

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="collects")
    title = models.CharField(max_length=255)
    reason = models.CharField(max_length=20, choices=Reason.choices)
    description = models.TextField(blank=True)
    cover_image = models.ImageField(upload_to="collect_covers/", blank=True, null=True)
    goal_amount = models.DecimalField(
        max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, null=True, blank=True
    )
    is_infinite = models.BooleanField(default=False)
    collected_amount = models.DecimalField(
        max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, default=0
    )
    donators_count = models.PositiveIntegerField(default=0)
    ends_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} ({self.author})"


class Payment(models.Model):
    """
    Модель платежа для сбора средств.

    Поля:
    - collect: Сбор средств, к которому относится платёж.
    - donator: Пользователь, осуществивший платёж.
    - amount: Сумма платежа.
    - created_at: Дата и время создания платежа.
    """

    collect = models.ForeignKey(
        Collect, on_delete=models.CASCADE, related_name="payments"
    )
    donator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="payments")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.donator} → {self.collect}: {self.amount}"
