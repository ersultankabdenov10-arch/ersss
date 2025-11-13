from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Employee(models.Model):
    ROLE_CHOICES = [
        ('user', 'Пайдаланушы'),
        ('guest', 'Қонақ'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    contact_info = models.TextField(blank=True)
    phone = models.CharField(max_length=20, blank=True, verbose_name='Телефон нөмірі')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"

class Car(models.Model):
    STATUS_CHOICES = [
        ('available', 'Қолжетімді'),
        ('unavailable', 'Қол жетімсіз'),
    ]
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.PositiveIntegerField()
    car_type = models.CharField(max_length=50)
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='cars/')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    location = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='Автокөліктің мекенжайы'
    )

    coordinates = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Координаттар (лат,лон)'
    )

    def __str__(self):
        return f"{self.brand} {self.model}"

class Booking(models.Model):
    STATUS_CHOICES = [
        ('active', 'Белсенді'),
        ('completed', 'Аяқталған'),
        ('cancelled', 'Бас тартылды'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')

    def __str__(self):
        return f"{self.car} для {self.user} с {self.start_date} по {self.end_date}"

    def formatted_start(self):
        return self.start_date.strftime("%d.%m.%Y %H:%M") if self.start_date else "—"

    def formatted_now(self):
        return timezone.now().strftime("%d.%m.%Y %H:%M")

class ProfitRecord(models.Model):
    car = models.ForeignKey(Car, on_delete=models.SET_NULL, null=True)
    date_recorded = models.DateTimeField(auto_now_add=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    duration_minutes = models.PositiveIntegerField()
    total_profit = models.DecimalField(max_digits=12, decimal_places=2)

    def duration_human_readable(self):
        days = self.duration_minutes // 1440
        hours = (self.duration_minutes % 1440) // 60
        minutes = self.duration_minutes % 60
        parts = []
        if days:
            parts.append(f"{days} күн")
        if hours:
            parts.append(f"{hours} сағат")
        if minutes or not parts:
            parts.append(f"{minutes} минут")
        return " ".join(parts)

    def __str__(self):
        return f"{self.car} | {self.total_profit} ₸"

    @staticmethod
    def filter_by_date_range(start=None, end=None, car_id=None):
        qs = ProfitRecord.objects.all()
        if start:
            qs = qs.filter(start_date__gte=start)
        if end:
            qs = qs.filter(end_date__lte=end)
        if car_id:
            qs = qs.filter(car__id=car_id)
        return qs.order_by('-date_recorded')