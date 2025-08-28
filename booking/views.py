from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import TravelOption, Booking
from .forms import BookingForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('travel_options')
    else:
        form = UserCreationForm()
    return render(request, 'booking/register.html', {'form': form})




# views.py
from django.shortcuts import render
from datetime import datetime
from .models import TravelOption

from django.shortcuts import render
from datetime import datetime
from .models import TravelOption

def travel_options(request):
    # Get all travel options
    base_qs = TravelOption.objects.all()

    # Get filters from request
    selected_source = request.GET.get('source')
    selected_destination = request.GET.get('destination')
    selected_type = request.GET.get('type')
    selected_date_str = request.GET.get('date')

    # Start with unfiltered queryset to derive options per dropdown
    # Helper function to filter by all but one field
    def qs_except(exclude_field):
        qs = base_qs
        if exclude_field != 'source' and selected_source:
            qs = qs.filter(source=selected_source)
        if exclude_field != 'destination' and selected_destination:
            qs = qs.filter(destination=selected_destination)
        if exclude_field != 'type' and selected_type:
            qs = qs.filter(type=selected_type)
        if exclude_field != 'date' and selected_date_str:
            try:
                d = datetime.strptime(selected_date_str, '%Y-%m-%d').date()
                qs = qs.filter(datetime__date=d)
            except ValueError:
                pass
        return qs

    # Compute dropdown choices to show only valid options
    sources = qs_except('source').values_list('source', flat=True).distinct()
    destinations = qs_except('destination').values_list('destination', flat=True).distinct()
    types = qs_except('type').values_list('type', flat=True).distinct()
    dates = qs_except('date').dates('datetime', 'day').distinct()

    # Finally, filter the queryset with all selected filters
    options = base_qs
    if selected_source:
        options = options.filter(source=selected_source)
    if selected_destination:
        options = options.filter(destination=selected_destination)
    if selected_type:
        options = options.filter(type=selected_type)
    if selected_date_str:
        try:
            filter_date = datetime.strptime(selected_date_str, '%Y-%m-%d').date()
            options = options.filter(datetime__date=filter_date)
        except ValueError:
            pass

    context = {
        'options': options,
        'filters': request.GET,
        'sources': sources,
        'destinations': destinations,
        'types': types,
        'dates': dates,
    }
    return render(request, 'booking/travel_options.html', context)


@login_required
def book_travel(request, travel_id):
    travel_option = get_object_or_404(TravelOption, id=travel_id)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.travel_option = travel_option
            booking.total_price = booking.number_of_seats * travel_option.price
            # Check for available seats
            if booking.number_of_seats > travel_option.available_seats:
                form.add_error('number_of_seats', 'Not enough available seats.')
            else:
                travel_option.available_seats -= booking.number_of_seats
                travel_option.save()
                booking.save()
                return redirect('my_bookings')
    else:
        form = BookingForm()
    return render(request, 'book_travel.html', {'form': form, 'travel_option': travel_option})

@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'my_bookings.html', {'bookings': bookings})

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    if booking.status == 'Confirmed':
        booking.status = 'Cancelled'
        # Return seats to availability
        booking.travel_option.available_seats += booking.number_of_seats
        booking.travel_option.save()
        booking.save()
    return redirect('my_bookings')


from django.shortcuts import redirect

@login_required
def toggle_theme(request):
    current = request.session.get('theme', 'light')
    request.session['theme'] = 'dark' if current == 'light' else 'light'
    return redirect(request.META.get('HTTP_REFERER', 'travel_options'))


from django.contrib.auth import logout as auth_logout
from django.shortcuts import render
from .models import TravelOption

@login_required
def logout_view(request):
    auth_logout(request)
    options = TravelOption.objects.all()
    return render(request, 'booking/logged_out.html', {'options': options})