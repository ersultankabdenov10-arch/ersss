from django.contrib import admin
from .models import Car, Booking, Employee, ProfitRecord

admin.site.register(Car)
admin.site.register(Booking)
admin.site.register(Employee)

@admin.register(ProfitRecord)
class ProfitRecordAdmin(admin.ModelAdmin):
    list_display = ('car', 'start_date', 'end_date', 'duration_minutes', 'total_profit')
    list_filter = ('car', 'start_date', 'end_date')
    search_fields = ('car__brand', 'car__model')