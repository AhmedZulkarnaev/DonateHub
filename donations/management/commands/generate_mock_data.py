import random
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from datetime import timezone
from faker import Faker
from decimal import Decimal

from donations.models import Collect, Payment

fake = Faker()
User = get_user_model()


class Command(BaseCommand):
    help = "Генерирует тестовые данные: пользователей, сборы и платежи"

    def add_arguments(self, parser):
        parser.add_argument("--users", type=int, default=100)
        parser.add_argument("--collects", type=int, default=500)
        parser.add_argument("--payments", type=int, default=2000)

    def handle(self, *args, **options):
        users_count = options["users"]
        collects_count = options["collects"]
        payments_count = options["payments"]

        self.stdout.write(self.style.MIGRATE_HEADING("Генерация пользователей..."))
        users = [User(username=fake.unique.user_name()) for _ in range(users_count)]
        User.objects.bulk_create(users)
        users = list(User.objects.all())
        self.stdout.write(self.style.SUCCESS(f"Создано пользователей: {len(users)}"))

        self.stdout.write(self.style.MIGRATE_HEADING("Генерация сборов..."))
        collect_created = 0
        for _ in range(collects_count):
            try:
                user = random.choice(users)
                is_infinite = random.choice([True, False])
                goal = (
                    Decimal(random.randint(1000, 100000)) if not is_infinite else None
                )
                collect = Collect(
                    author=user,
                    title=fake.sentence(nb_words=4),
                    reason=random.choice([r[0] for r in Collect.Reason.choices]),
                    description=fake.text(max_nb_chars=300),
                    cover_image="collect_covers/default.jpg",
                    goal_amount=goal,
                    is_infinite=is_infinite,
                    ends_at=fake.date_time_between(
                        start_date="+10d", end_date="+60d", tzinfo=timezone.utc
                    ),
                )
                collect.save()
                collect_created += 1
            except Exception as e:
                self.stderr.write(f"Ошибка при создании сбора: {e}")
        collects = list(Collect.objects.all())
        self.stdout.write(self.style.SUCCESS(f"Создано сборов: {collect_created}"))

        self.stdout.write(self.style.MIGRATE_HEADING("Генерация платежей..."))
        payment_created = 0
        for _ in range(payments_count):
            try:
                donator = random.choice(users)
                collect = random.choice(collects)
                amount = Decimal(random.randint(50, 10000))
                Payment.objects.create(donator=donator, collect=collect, amount=amount)
                payment_created += 1
            except Exception as e:
                self.stderr.write(f"Ошибка при создании платежа: {e}")

        self.stdout.write(self.style.SUCCESS(f"Создано платежей: {payment_created}"))
        self.stdout.write(self.style.SUCCESS("Все данные успешно сгенерированы!"))
