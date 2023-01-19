# Creating our models
from django.db import models


# Class class

class Class(models.Model):
    id = models.AutoField(primary_key=True)
    CLASS_CATEGORIES= (
        ('Arms','Arms'),
        ('Legs', 'Legs'),
        ('Chest','Chest'),
        ('Abs','Abs'),
        ('HIIT','Hiit'),
        ('Cardio','Cardio'),
        ('Yoga','Yoga'),
    )
    DIFFICULTY_LEVEL = (
        ('ADV', 'Advanced'),
        ('ITM', 'Intermediate'),
        ('BGN', 'Begginer'),

    )
    category = models.CharField(max_length=10, choices=CLASS_CATEGORIES)
    difficulty = models.CharField(max_length=3, choices=DIFFICULTY_LEVEL)
    capacity = models.IntegerField() # max number of people in a class
    rem = models.DecimalField(decimal_places=0, max_digits=2)
    instructor = models.CharField(max_length=30)
    class_name = models.CharField(max_length=100)
    price = models.DecimalField(decimal_places=2,max_digits=4)
    date = models.DateField()
    time = models.TimeField()


    class Meta:
        verbose_name_plural = "List of Classes"
    def __str__(self): # To display on our admin page once we have succesfully entered a new class
        return f'{self.class_name}: {self.difficulty} {self.category} for {self.capacity} people'




class User(models.Model): #to identify our users
    user_id = models.AutoField(primary_key=True)
    email = models.EmailField()
    name = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    
    class Meta:
        verbose_name_plural = "----"

    



class Book(models.Model): # to keep track of the bookings that have been made
    id = models.AutoField(primary_key=True)
    BOOKED = 'B'
    CANCELLED = 'C'

    TICKET_STATUSES = ((BOOKED, 'Booked'),
                       (CANCELLED, 'Cancelled'),)
    email = models.EmailField()
    name = models.CharField(max_length=30)
    user_id = models.DecimalField(decimal_places=0, max_digits=2)
    class_id = models.DecimalField(decimal_places=0, max_digits=2)
    class_name = models.CharField(max_length=30)
    category = models.CharField(max_length=30, default="Nothing")
    no_of_tickets = models.DecimalField(decimal_places=0, max_digits=2)
    price = models.DecimalField(decimal_places=2, max_digits=6)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(choices=TICKET_STATUSES, default=BOOKED, max_length=2)

    class Meta:
        verbose_name_plural = "List of Books"
    def __str__(self): # to display on our admin page once a booking has been made
        return f'{self.class_name} booked for {self.no_of_tickets} people by user {self.name}'
