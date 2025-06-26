# price_suggestion/views.py

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .predictor import predict_sales
from .models import PricePredictionRequest
import json
from django.http import JsonResponse

@csrf_exempt
def predict_price_and_save(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            sub_category = data.get('sub_category')
            price = data.get('price')

            if sub_category is None or price is None:
                return JsonResponse({"error": "sub_category and price are required."}, status=400)

            prediction = predict_sales(sub_category, float(price))

            # Save to DB
            record = PricePredictionRequest.objects.create(
                sub_category=sub_category,
                price=price,
                predicted_sales=prediction
            )

            return JsonResponse({
                "id": record.id,
                "sub_category": record.sub_category,
                "price": record.price,
                "predicted_sales": record.predicted_sales,
                "created_at": record.created_at
            })

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Only POST method allowed."}, status=405)


# ✅ Helper function to suggest a price
def calculate_suggested_price(predicted_sales, current_price):
    if predicted_sales < 16:
        return round(current_price * 0.9, 2)
    elif predicted_sales > 19:
        return round(current_price * 1.1, 2)
    else:
        return round(current_price, 2)


# ✅ Updated form view to include chart values
def price_suggestion_form(request):
    if request.method == "POST":
        sub_category = request.POST.get("sub_category")
        price = request.POST.get("price")

        if sub_category and price:
            price = float(price)
            predicted_sales = predict_sales(sub_category, price)
            suggested_price = calculate_suggested_price(predicted_sales, price)

            # Save to DB
            PricePredictionRequest.objects.create(
                sub_category=sub_category,
                price=price,
                predicted_sales=predicted_sales,
                suggested_price=suggested_price
            )

            return render(request, "price_suggestion/suggestion_result.html", {
                "sub_category": sub_category,
                "price": price,
                "predicted_sales": predicted_sales,
                "suggested_price": suggested_price, 
                "chart_labels": ["Current", "Suggested"],
                "chart_current": [price, price],
                "chart_suggested": [price, suggested_price]
            })

    return render(request, "price_suggestion/form.html")


def prediction_history(request):
    predictions = PricePredictionRequest.objects.all().order_by('-created_at')
    return render(request, "price_suggestion/history.html", {
        "predictions": predictions
    })
