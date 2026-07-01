from django.shortcuts import render, redirect
from data.models import User

# Show Login Page
def login_page(request):
    return render(request, "login.html")

# Login Logic
def login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_type = request.POST.get('user_type')

        user = User.objects.filter(email=email, password=password, user_type=user_type).first()

        if user:
            request.session["user_id"] = user.user_id
            request.session['user_type'] = user.user_type

            if user.user_type == "vendor":
                return redirect("/vendor/")
            else:
                return redirect("/customer/")

        return render(request, "login.html", {"error": "Invalid Email or Password"})

    return render(request, "login.html")