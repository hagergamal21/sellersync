# demand_forecasting/views.py

from django.shortcuts import render, redirect
from django.contrib import messages
from .services.forecasting import forecast_demand
from .models import SubCategory, SemanticLabel, Inventory, ForecastResult

def forecast_view(request):
    if request.method == 'POST':
        subcategory_name = request.POST.get('subcategory')
        semantic_label_name = request.POST.get('semantic_label')
        days_to_predict = int(request.POST.get('days_to_predict', 30))
        current_inventory = float(request.POST.get('current_inventory', 0))
        base_price = float(request.POST.get('base_price', 100))

        try:
            # Get model instances
            subcategory_obj = SubCategory.objects.get(name=subcategory_name)
            semantic_label_obj = SemanticLabel.objects.get(label=semantic_label_name)

            # Run forecasting
            forecast, plot_url_demand, plot_url_inventory, inventory_status = forecast_demand(
                subcategory=subcategory_name,
                semantic_label=semantic_label_name,
                days_to_predict=days_to_predict,
                current_inventory=current_inventory,
                base_price=base_price,
            )

            # Save or update inventory
            inventory_obj, created = Inventory.objects.update_or_create(
                subcategory=subcategory_obj,
                semantic_label=semantic_label_obj,
                defaults={
                    'current_quantity': current_inventory,
                    'base_price': base_price
                }
            )

            # Calculate projected revenue
            projected_revenue = inventory_status['total_forecasted_demand'] * base_price

            # Save forecast results
            for day_data in forecast:
                ForecastResult.objects.update_or_create(
                    subcategory=subcategory_obj,
                    semantic_label=semantic_label_obj,
                    date=day_data['ds'],
                    defaults={
                        'predicted_quantity': day_data['yhat'],
                        'yhat_lower': day_data['yhat_lower'],
                        'yhat_upper': day_data['yhat_upper'],
                        'days_predicted': days_to_predict,
                        'current_inventory': current_inventory,
                        'inventory_shortfall': inventory_status['inventory_shortfall'],
                        'inventory_excess': inventory_status['inventory_excess'],
                        'projected_revenue': projected_revenue,
                        'plot_path': '',  # Can be used if you save plots as files
                    }
                )

            return render(request, 'demand_forecasting/forecast_result.html', {
                'forecast': forecast,
                'plot_url_demand': plot_url_demand,
                'plot_url_inventory': plot_url_inventory,
                'inventory_status': inventory_status,
                'subcategory': subcategory_name,
                'semantic_label': semantic_label_name,
                'projected_revenue': projected_revenue,
            })

        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
            return redirect('demand_forecasting:forecast')

    else:
        subcategories = SubCategory.objects.all()
        semantic_labels = SemanticLabel.objects.all()
        return render(request, 'demand_forecasting/forecast_form.html', {
            'subcategories': subcategories,
            'semantic_labels': semantic_labels,
        })
