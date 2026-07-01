from django.shortcuts import render, redirect
from data.models import User

def signup(request):
    if request.method == "POST":
        fname = request.POST.get('firstname')
        lname = request.POST.get('lastname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        mobileno = request.POST.get('mobileno')
        user_type = request.POST.get('user_type')   # vendor or customer

        User.objects.create(
            firstname=fname,
            lastname=lname,
            email=email,
            password=password,
            mobileno=mobileno,
            user_type=user_type
        )

        return redirect("/login/")

    return render(request, "signup.html")