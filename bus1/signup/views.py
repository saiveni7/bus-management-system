from django.shortcuts import render, redirect
from data.models import User

def signup(request):
    if request.method == "POST":
        fname = request.POST['firstname']
        lname = request.POST['lastname']
        email = request.POST['email']
        password = request.POST['password']
        mobileno = request.POST['mobileno']
        user_type = request.POST['user_type']   # vendor or customer

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
