# price_suggestion/models.py

from django.db import models

class PricePredictionRequest(models.Model):
    sub_category = models.CharField(max_length=255)
    price = models.FloatField()
    predicted_sales = models.FloatField()
    suggested_price = models.FloatField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sub_category} - {self.price} USD ➔ {self.predicted_sales} sales"
