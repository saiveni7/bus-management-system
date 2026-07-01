"""
URL configuration for bus1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from home import views as v1
from about import views as v2
from contact import views as v3
from data import views as v4
from dashboard import views as v5
from signup import views as v6
from service import views as v7
from login import views as v8
from payment import views as v9

urlpatterns = [
    path('admin/', admin.site.urls),

    # Static Pages
    path('', v1.home, name="home"),
    path('home/', v1.home),
    path('about/', v2.about, name="about"),
    path('contact/', v3.contact, name="contact"),
    path('service/', v7.service, name="service"),
    path('data/', v4.data, name="data"),

    # Authentication
    path('signup/', v6.signup, name="signup"),
    path('login/', v8.login, name="login"),

    # Dashboard
    path('dashboard/', v5.dashboard, name="dashboard"),
    path('vendor/', v5.vendor_dashboard, name="vendor_dashboard"),
    path('customer/', v5.customer_dashboard, name="customer_dashboard"),

    # Vendor CRUD
    path('add_bus/', v5.add_bus, name="add_bus"),
    path('update_bus/<int:bus_id>/', v5.update_bus, name="update_bus"),
    path('delete_bus/<int:bus_id>/', v5.delete_bus, name="delete_bus"),

    # Customer Actions
    path('search_bus/', v5.search_bus, name="search_bus"),
    path('book_bus/<int:bus_id>/', v5.book_bus, name="book_bus"),
    path('cancel_booking/<int:booking_id>/', v5.cancel_booking, name="cancel_booking"),

    # Payment
    path('payment/', v9.payment, name="payment"),
]