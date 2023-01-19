from datetime import datetime
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import User, Class, Book
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required



def home(request):
    if request.user.is_authenticated:
        return render(request, 'myapp/home.html')
    else:
        return render(request, 'myapp/signin.html')


@login_required(login_url='signin')
def findclass(request):
    context = {}
    if request.method == 'POST':
        category = request.POST.get('category')

        date_r = request.POST.get('date')
        date_r = datetime.strptime(date_r, "%Y-%m-%d").date()
        year = date_r.strftime("%Y")
        month = date_r.strftime("%m")
        day = date_r.strftime("%d")
        class_list = Class.objects.filter(category=category,date__year=year, date__month=month, date__day=day)

        if class_list:
            return render(request, 'myapp/list.html', locals())
        else:
            context['data'] = request.POST
            context["error"] = "No available Class Schedule for entered Category and Date"
            return render(request, 'myapp/findclass.html', context)
    else:
        return render(request, 'myapp/findclass.html')


@login_required(login_url='signin')
def bookings(request):
    context = {}
    if request.method == 'POST':
        id_r = request.POST.get('class_id')
        tickets_r = int(request.POST.get('no_of_tickets'))
        class_r = Class.objects.get(id=id_r)
        if class_r:
            if class_r.rem > int(tickets_r):
                name_r = class_r.class_name
                cost = int(tickets_r) * class_r.price
                category_r = class_r.category


                price_r = class_r.price
                date_r = class_r.date
                time_r = class_r.time
                username_r = request.user.username
                email_r = request.user.email
                userid_r = request.user.id
                rem_r = class_r.rem - tickets_r

                Class.objects.filter(id=id_r).update(rem=rem_r)

                book = Book.objects.create(name=username_r, email=email_r, user_id=userid_r, class_name=name_r,
                                           category=category_r, class_id=id_r,
                                           price=price_r, no_of_tickets=tickets_r, date=date_r, time=time_r,
                                           status='BOOKED')

                print('------------book id-----------', book.id)
                book.save()

                return render(request, 'myapp/bookings.html', locals())
            else:
                context["error"] = "Sorry select fewer number of tickets"
                return render(request, 'myapp/findclass.html', context)

    else:
        return render(request, 'myapp/findclass.html')


@login_required(login_url='signin')
def cancellings(request):
    context = {}
    if request.method == 'POST':
        id_r = request.POST.get('class_id')


        try:
            book = Book.objects.get(id=id_r)
            class_r = Class.objects.get(id=book.class_id)
            rem_r = class_r.rem + book.no_of_tickets
            Class.objects.filter(id=book.class_id).update(rem=rem_r)
            #no_of_tickets_r = book.no_of_tickets - tickets_r
            Book.objects.filter(id=id_r).update(status='CANCELLED', no_of_tickets=0)
            messages.success(request, "Booked Class has been cancelled.")
            return redirect(seebookings)
        except Book.DoesNotExist:
            context["error"] = "Sorry You have not booked that Class"
            return render(request, 'myapp/error.html', context)
    else:
        return render(request, 'myapp/findclass.html')


@login_required(login_url='signin')
def seebookings(request,new={}):
    context = {}
    id_r = request.user.id
    book_list = Book.objects.filter(user_id=id_r)
    if book_list:
        return render(request, 'myapp/booklist.html', locals())
    else:
        context["error"] = "Sorry no classes booked"
        return render(request, 'myapp/findclass.html', context)


def signup(request):
    context = {}
    if request.method == 'POST':
        name_r = request.POST.get('name')
        email_r = request.POST.get('email')
        password_r = request.POST.get('password')
        user = User.objects.create_user(name_r, email_r, password_r, )
        if user:
            login(request, user)
            return render(request, 'myapp/thank.html')
        else:
            context["error"] = "Provide valid credentials"
            return render(request, 'myapp/signup.html', context)
    else:
        return render(request, 'myapp/signup.html', context)


def signin(request):
    context = {}
    if request.method == 'POST':
        name_r = request.POST.get('name')
        password_r = request.POST.get('password')
        user = authenticate(request, username=name_r, password=password_r)
        if user:
            login(request, user)

            context["user"] = name_r
            context["id"] = request.user.id
            return render(request, 'myapp/success.html', context)

        else:
            context["error"] = "Provide valid credentials"
            return render(request, 'myapp/signin.html', context)
    else:
        context["error"] = "You are not logged in"
        return render(request, 'myapp/signin.html', context)


def signout(request):
    context = {}
    logout(request)
    context['error'] = "You have been logged out"
    return render(request, 'myapp/signin.html', context)


def success(request):
    context = {}
    context['user'] = request.user
    return render(request, 'myapp/success.html', context)
