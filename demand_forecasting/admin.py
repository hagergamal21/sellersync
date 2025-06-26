from django.contrib import admin
from .models import SubCategory, SemanticLabel, Inventory, ForecastResult

@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    list_per_page = 25
    ordering = ('name',)

@admin.register(SemanticLabel)
class SemanticLabelAdmin(admin.ModelAdmin):
    list_display = ('id', 'label')
    search_fields = ('label',)
    list_per_page = 25
    ordering = ('label',)

@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'subcategory', 'semantic_label', 'current_quantity', 'base_price', 'updated_at')
    list_filter = ('subcategory', 'semantic_label')
    search_fields = ('subcategory__name', 'semantic_label__label')
    list_per_page = 25
    date_hierarchy = 'updated_at'
    ordering = ('-updated_at',)

@admin.register(ForecastResult)
class ForecastResultAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'subcategory', 'semantic_label', 'date', 'predicted_quantity',
        'yhat_lower', 'yhat_upper', 'days_predicted', 'created_at'
    )
    list_filter = ('subcategory', 'semantic_label', 'date')
    search_fields = ('subcategory__name', 'semantic_label__label')
    list_per_page = 25
    date_hierarchy = 'date'
    ordering = ('-date',)
