from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from inventory.models import Product
from bookings.models import Rental
from payments.models import Order
from django.db.models import Sum

@api_view(['GET'])
@permission_classes([AllowAny])
def dashboard_data(request):
    """
    Returns stats for dashboard: total products, orders, rentals, revenue
    Optional query param: ?season=summer
    """
    total_products = Product.objects.count()
    total_orders = Order.objects.count()
    total_rentals = Rental.objects.count()

    monthly_revenue = (
        Order.objects.filter(status='paid').aggregate(total=Sum('amount'))['total'] or 0
    )

    season = request.GET.get('season')
    if season:
        seasonal_products = Product.objects.filter(season=season).count()
    else:
        seasonal_products = total_products

    data = {
        "total_products": total_products,
        "total_orders": total_orders,
        "total_rentals": total_rentals,
        "monthly_revenue": monthly_revenue,
        "season": season or "all",
        "seasonal_products": seasonal_products
    }

    return Response(data)