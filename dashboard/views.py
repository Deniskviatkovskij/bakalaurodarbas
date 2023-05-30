from django.shortcuts import render
from django.http import JsonResponse
from django.db import connection
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.decorators import login_required
from .models import Thresholds, LayoutData
from decimal import Decimal
from django.shortcuts import get_object_or_404
from datetime import datetime, timedelta
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_exempt


def check_login(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return None

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required(login_url='/login/')
def dashboard_view(request):
    user = request.user
    thresholds, created = Thresholds.objects.get_or_create(user_id=user.id)

    # process form data and update threshold values
    if request.method == 'POST':
        thresholds.temperature_min = Decimal(request.POST.get('temperature-min', None))
        thresholds.temperature_max = Decimal(request.POST.get('temperature-max', None))
        thresholds.power_min = Decimal(request.POST.get('power-min', None))
        thresholds.power_max = Decimal(request.POST.get('power-max', None))
        thresholds.save()

    # prepopulate form with existing threshold values
    temperature_min = thresholds.temperature_min if thresholds.temperature_min is not None else ''
    temperature_max = thresholds.temperature_max if thresholds.temperature_max is not None else ''
    power_min = thresholds.power_min if thresholds.power_min is not None else ''
    power_max = thresholds.power_max if thresholds.power_max is not None else ''

    return render(request, 'dashboard.html', {
        'thresholds': thresholds,
        'temperature_min': temperature_min,
        'temperature_max': temperature_max,
        'power_min': power_min,
        'power_max': power_max,
    })


def check_thresholds(user_id):
    # Get the user's thresholds
    thresholds = Thresholds.objects.get(user_id=user_id)
    print("Thresholds for user_id", user_id)
    print(thresholds)
    # Get the latest parameter data for the user
    latest_data = LayoutData.objects.filter(user_id=user_id).latest('date')
    print("Latest data for user_id", user_id)
    print(latest_data)
    # Check if the latest data violates any thresholds
    if (latest_data.temperature < thresholds.temperature_min
        or latest_data.temperature > thresholds.temperature_max):
        return True  # Thresholds are violated
    else:
        return False  # Thresholds are not violated


@login_required(login_url='/login/')
def get_temperature(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT Temperature FROM layout_data ORDER BY Date DESC;")
        temperature = Decimal(str(cursor.fetchone()[0]))

    user_id = request.user.id

    if check_thresholds(user_id):
        status = "threshold_violated"
        thresholds = get_object_or_404(Thresholds, user_id=user_id)
        min_temperature = thresholds.temperature_min
        max_temperature = thresholds.temperature_max
        if temperature < min_temperature:
            message = "Temperature is below the minimum threshold value."
        elif temperature > max_temperature:
            message = "Temperature is above the maximum threshold value."
    else:
        thresholds = get_object_or_404(Thresholds, user_id=user_id)
        min_temperature = thresholds.temperature_min
        max_temperature = thresholds.temperature_max
        temperature = Decimal(str(temperature))
        if temperature < min_temperature:
            status = "below_min"
            message = "Temperature is below the minimum threshold value."
        elif temperature > max_temperature:
            status = "above_max"
            message = "Temperature is above the maximum threshold value."
        else:
            status = "within_range"
            message = "Temperature is within the range."

    return JsonResponse({
        "temperature": int(temperature),
        "status": status,
        "message": message,
        "min_temperature": int(min_temperature),
        "max_temperature": int(max_temperature)
    })




@login_required(login_url='/login/')
def get_power(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT Date, Power FROM layout_data ORDER BY Date DESC LIMIT 10;")
        rows = cursor.fetchall()
        power_data = [{'Date': row[0].strftime('%Y-%m-%d %H:%M:%S'), 'Power': row[1]} for row in rows]
        print(power_data)
    # Ribiniu verciu tikrinimas
    user_id = request.user.id
    print(user_id)
    thresholds = get_object_or_404(Thresholds, user_id=user_id)
    min_power = thresholds.power_min
    max_power = thresholds.power_max
    for data_point in power_data:
        power = Decimal(str(data_point['Power']))
        if power < min_power:
            data_point['status'] = "below_min"
            data_point['message'] = "Energy production is below the minimum threshold value."
        elif power > max_power:
            data_point['status'] = "above_max"
            data_point['message'] = "Energy production is above the maximum threshold value."
        else:
            data_point['status'] = "within_range"
            data_point['message'] = "within_range"
    return JsonResponse(power_data, encoder=DjangoJSONEncoder, safe=False)



@login_required(login_url='/login/')
def get_predicted_data(request):
    # Get the current UTC time
    now = datetime.utcnow()

    # Set the start time for the prediction (1 hour from now)
    start_time = now + timedelta(hours=0)

    # Set the end time for the prediction (24 hours from now)
    end_time = now + timedelta(hours=24)

    # Retrieve the predicted data from the database
    with connection.cursor() as cursor:
        cursor.execute("SELECT Windspeed, Predicted_voltage, Date FROM prediction WHERE Date >= %s AND Date < %s;",
                       [start_time, end_time])
        rows = cursor.fetchall()
        predicted_data = [{'Date': row[2].strftime('%Y-%m-%d %H:%M:%S'), 'Windspeed': row[0], 'Predicted_voltage': row[1]} for row in rows]

    return JsonResponse(predicted_data, encoder=DjangoJSONEncoder, safe=False)
