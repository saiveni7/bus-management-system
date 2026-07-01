from django.db import models

class User(models.Model):
    USER_TYPES = (
        ('customer', 'Customer'),
        ('vendor', 'Vendor'),
    )

    user_id = models.AutoField(primary_key=True)
    firstname = models.CharField(max_length=150)
    lastname = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    mobileno = models.CharField(max_length=15)
    user_type = models.CharField(max_length=20, choices=USER_TYPES)

    def __str__(self):
        return self.email



class Bus(models.Model):
    bus_id = models.AutoField(primary_key=True)

    bus_name = models.CharField(max_length=100)
    source = models.CharField(max_length=100)
    dest = models.CharField(max_length=100)

    nos = models.IntegerField()   # total seats
    rem = models.IntegerField()   # remaining seats

    price = models.DecimalField(max_digits=8, decimal_places=2)
    date = models.DateField()
    time = models.TimeField()

    vendor = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.bus_name



class Book(models.Model):
    BOOKED = 'BOOKED'
    CANCELLED = 'CANCELLED'

    STATUS = (
        (BOOKED, 'Booked'),
        (CANCELLED, 'Cancelled'),
    )

    booking_id = models.AutoField(primary_key=True)

    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)

    seats_booked = models.IntegerField()
    total_price = models.DecimalField(max_digits=8, decimal_places=2)

    date = models.DateField()
    time = models.TimeField()

    status = models.CharField(max_length=20, choices=STATUS, default=BOOKED)

    def __str__(self):
        return f"{self.customer.email} - {self.bus.bus_name}"
