from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from data.models import User,Bus,Book

# ===============================
# MAIN DASHBOARD (ROLE REDIRECT)
# ===============================

def dashboard(request):

    user_type = request.session.get("user_type")

    if user_type == "vendor":
        return redirect("vendor_dashboard")

    elif user_type == "customer":
        return redirect("customer_dashboard")

    else:
        return redirect("login")


# ===============================
# VENDOR DASHBOARD
# ===============================

def vendor_dashboard(request):

    if request.session.get("user_type") != "vendor":
        return redirect("login")

    vendor_id = request.session.get("user_id")

    buses = Bus.objects.filter(vendor_id=vendor_id)

    return render(request, "vendor_dashboard.html", {"buses": buses})


# ===============================
# ADD BUS
# ===============================

def add_bus(request):

    if request.session.get("user_type") != "vendor":
        return redirect("login")

    if request.method == "POST":

        vendor_id = request.session.get("user_id")

        total_seats = int(request.POST.get("nos"))

        Bus.objects.create(
            bus_name=request.POST.get("bus_name"),
            source=request.POST.get("source"),
            dest=request.POST.get("dest"),
            nos=total_seats,
            rem=total_seats,  # initially remaining = total
            price=request.POST.get("price"),
            date=request.POST.get("date"),
            time=request.POST.get("time"),
            vendor_id=vendor_id
        )

        messages.success(request, "Bus Added Successfully!")
        return redirect("vendor_dashboard")

    return render(request, "add_bus.html")


# ===============================
# UPDATE BUS
# ===============================

def update_bus(request, bus_id):

    if request.session.get("user_type") != "vendor":
        return redirect("login")

    vendor_id = request.session.get("user_id")

    bus = get_object_or_404(Bus, bus_id=bus_id, vendor_id=vendor_id)

    if request.method == "POST":

        bus.bus_name = request.POST.get("bus_name")
        bus.source = request.POST.get("source")
        bus.dest = request.POST.get("dest")
        bus.nos = request.POST.get("nos")
        bus.price = request.POST.get("price")
        bus.date = request.POST.get("date")
        bus.time = request.POST.get("time")

        bus.save()

        messages.success(request, "Bus Updated Successfully!")
        return redirect("vendor_dashboard")

    return render(request, "update_bus.html", {"bus": bus})


# ===============================
# DELETE BUS
# ===============================

def delete_bus(request, bus_id):

    if request.session.get("user_type") != "vendor":
        return redirect("login")

    vendor_id = request.session.get("user_id")

    bus = get_object_or_404(Bus, bus_id=bus_id, vendor_id=vendor_id)

    bus.delete()

    messages.success(request, "Bus Deleted Successfully!")
    return redirect("vendor_dashboard")


# ===============================
# CUSTOMER DASHBOARD
# ===============================

def customer_dashboard(request):
    customer_id = request.session.get("user_id")
    bookings = Book.objects.filter(customer_id=customer_id)
    return render(request, "customer_dashboard.html", {"bookings": bookings})


# ===============================
# SEARCH BUS
# ===============================

def search_bus(request):

    if request.session.get("user_type") != "customer":
        return redirect("login")

    source = request.GET.get("source")
    dest = request.GET.get("dest")
    date = request.GET.get("date")

    buses = Bus.objects.filter(
        source=source,
        dest=dest,
        date=date,
        rem__gt=0  # only buses with available seats
    )

    return render(request, "search_results.html", {"buses": buses})


# ===============================
# BOOK BUS
# ===============================

def book_bus(request, bus_id):

    if request.session.get("user_type") != "customer":
        return redirect("login")

    bus = get_object_or_404(Bus, bus_id=bus_id)

    if request.method == "POST":

        seats = int(request.POST.get("seats"))
        customer_id = request.session.get("user_id")

        if not customer_id:
            return redirect("login")

        # Check seat availability
        if bus.rem >= seats:

            # Reduce remaining seats
            bus.rem -= seats
            bus.save()

            # Calculate total price
            total = seats * bus.price

            # Save booking
            Book.objects.create(
                customer_id=customer_id,
                bus=bus,
                seats_booked=seats,
                total_price=total,
                date=bus.date,
                time=bus.time
            )

            messages.success(request, "Booking Successful!")
            return redirect("customer_dashboard")

        else:
            messages.error(request, "Not enough seats available!")

    return render(request, "book_bus.html", {"bus": bus})


# ===============================
# CANCEL BOOKING
# ===============================

def cancel_booking(request, booking_id):

    if request.session.get("user_type") != "customer":
        return redirect("login")

    customer_id = request.session.get("user_id")

    booking = get_object_or_404(
        Book,
        booking_id=booking_id,
        customer_id=customer_id
    )

    if booking.status == "BOOKED":

        bus = booking.bus

        # Add seats back
        bus.rem += booking.seats_booked
        bus.save()

        booking.status = "CANCELLED"
        booking.save()

        messages.success(request, "Booking Cancelled Successfully!")

    return redirect("customer_dashboard")