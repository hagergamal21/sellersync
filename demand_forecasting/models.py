from django.db import models

class SubCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Subcategory"
        verbose_name_plural = "Subcategories"
        ordering = ['name']  # Added ordering

class SemanticLabel(models.Model):
    label = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.label

    class Meta:
        verbose_name = "Semantic Label"
        verbose_name_plural = "Semantic Labels"
        ordering = ['label']  # Added ordering

class Inventory(models.Model):
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='inventories')
    semantic_label = models.ForeignKey(SemanticLabel, on_delete=models.CASCADE, related_name='inventories')
    current_quantity = models.FloatField(default=0.0)
    base_price = models.FloatField(default=0.0)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.subcategory} ({self.semantic_label}) - {self.current_quantity}"

    class Meta:
        verbose_name = "Inventory"
        verbose_name_plural = "Inventories"
        constraints = [
            models.UniqueConstraint(fields=['subcategory', 'semantic_label'], name='unique_inventory')
        ]
        ordering = ['subcategory', 'semantic_label']

class ForecastResult(models.Model):
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='forecasts')
    semantic_label = models.ForeignKey(SemanticLabel, on_delete=models.CASCADE, related_name='forecasts')
    date = models.DateField()
    predicted_quantity = models.FloatField()
    yhat_lower = models.FloatField()
    yhat_upper = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    days_predicted = models.PositiveIntegerField()
    current_inventory = models.FloatField()
    inventory_shortfall = models.FloatField(default=0.0)
    inventory_excess = models.FloatField(default=0.0)
    projected_revenue = models.FloatField(default=0.0)
    plot_path = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.subcategory} - {self.semantic_label} ({self.date})"

    class Meta:
        verbose_name = "Forecast Result"
        verbose_name_plural = "Forecast Results"
        constraints = [
            models.UniqueConstraint(fields=['subcategory', 'semantic_label', 'date'], name='unique_forecast')
        ]
        ordering = ['-date']  # Show recent forecasts first
