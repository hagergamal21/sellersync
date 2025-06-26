# price_suggestion/admin.py

from django.contrib import admin
from .models import PricePredictionRequest

@admin.register(PricePredictionRequest)
class PricePredictionRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'sub_category', 'price', 'predicted_sales', 'created_at')
    list_filter = ('sub_category', 'created_at')
    search_fields = ('sub_category',)
    ordering = ('-created_at',)
