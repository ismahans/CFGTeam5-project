import datetime
from decimal import Decimal

from django.contrib import auth
from django.contrib.auth.models import User

# Importing test utilities from Django gives you A LOT of power
# We can basically simulate being a user in a browser.
# We can send GET and POST requests to Django's "test web server" using appropriate paths (defined in urls.py).
# This request then gets handled by views.py that returns a response. This is pretty much how the real
# web application will also behave once it is deployed.
from django.test import TestCase

from .models import Class, Book


# Simply creates a user in the database
def create_test_user(name, email, password):
    return User.objects.create_user(name, email, password)


class AuthenticationViewTests(TestCase):

    def sign_up(self, name, email, password):
        return self.client.post("/signup", {"name": name, "email": email, "password": password})

    def test_successful_signup(self):
        test_email = "Yeesha@myst.com"
        test_username = "Yeesha"
        response = self.sign_up(test_username, test_email, "SomethingPassword")

        # Check that the user object has been created in the database
        registered_user = User.objects.get(username=test_username)
        self.assertEqual(registered_user.email, test_email, "User should now be in the database")
        self.assertTrue(registered_user.is_authenticated)

        # Check that the web server returns success to "the user"
        self.assertEqual(response.status_code, 200)

        # The returned HTML has been encoded as bytes, so we need to decode it. (Your browser would do something like
        # this in real life as well).
        response_text = response.content.decode("utf-8")

        # Note: this is kind of testing the front-end. It might need to get updated if others still edit the code.
        self.assertIn("your account has been created", response_text.lower(),
                      "The returned page should contain some success text.")

    def test_signin_signout(self):
        # Register the user
        test_email = "Yeesha@myst.com"
        test_username = "Yeesha"
        test_password = "SomethingPassword"
        create_test_user(test_username, test_email, test_password)

        # At first, check that we're not yet authenticated
        user = auth.get_user(self.client)
        self.assertFalse(user.is_authenticated)

        # Sign in with the user
        self.client.post("/signin", {"name": test_username, "password": test_password})
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)

        # Sign out the user
        self.client.post("/signout")
        user = auth.get_user(self.client)
        self.assertFalse(user.is_authenticated)

    def test_bad_signin_attempt(self):
        create_test_user("Achenar", "achenar@myst.com", "my_password")

        # At first, check that we're not yet authenticated
        user = auth.get_user(self.client)
        self.assertFalse(user.is_authenticated)

        # Sign in with the user
        self.client.post("/signin", {"name": "Achenar", "password": "NOT MY PASSWORD"})
        user = auth.get_user(self.client)
        self.assertFalse(user.is_authenticated)


def make_dummy_class(capacity, category="Arms", difficulty="ADV", instructor="Esher", class_name="Linking Books", price=Decimal(4), date=datetime.date.min, time=datetime.time.min):
    return Class.objects.create(category=category, difficulty=difficulty, capacity=capacity,
                                rem=Decimal(capacity), instructor=instructor,
                                class_name=class_name, price=price, date=date,
                                time=time)


class TestViews(TestCase):

    home_template_path = 'myapp/home.html'
    signin_template_path = 'myapp/signin.html'
    findclass_template_path = 'myapp/findclass.html'
    class_list_template_path = 'myapp/list.html'
    bookings_template_path = 'myapp/bookings.html'

    # Creates a user object in the DB and authenticates our test client with that user
    # Most of our endpoints require the user to be authenticated
    def create_and_authenticate_user(self):
        user = create_test_user("Esher", email="esher@myst.com", password="whatever")
        self.assertTrue(self.client.login(username=user.username, password="whatever"))
        return user

    def test_home_authenticated(self):
        self.create_and_authenticate_user()
        response = self.client.post("")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.home_template_path)

    def test_home_not_authenticated(self):
        response = self.client.post("")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.signin_template_path)

    def test_find_class_with_no_classes(self):
        self.create_and_authenticate_user()

        # GET request
        response = self.client.get("/findclass")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.findclass_template_path)

        # POST request
        response = self.client.post("/findclass", {"category": "Doesn't Exist!", "date": "2010-10-20"})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.findclass_template_path)

        response_text = response.content.decode("utf-8")
        self.assertIn("no available class schedule for entered category and date", response_text.lower())

    def test_find_class_with_multiple_classes(self):
        self.create_and_authenticate_user()

        make_dummy_class(5, class_name="Edanna", category="Category1", date=datetime.date(2022, 8, 1))
        make_dummy_class(15, class_name="Tomahna", category="Category1", date=datetime.date(2022, 8, 1))
        make_dummy_class(10, class_name="Amateria", category="Category1", date=datetime.date(2022, 10, 1))
        make_dummy_class(10, class_name="Jnanin", category="Category2", date=datetime.date(2022, 10, 1))

        # Expecting to get 2 classes back
        response = self.client.post("/findclass", {"category": "Category1", "date": "2022-8-1"})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.class_list_template_path)

        response_text = response.content.decode("utf-8")
        self.assertIn("Edanna", response_text)
        self.assertIn("Tomahna", response_text)
        self.assertNotIn("Amateria", response_text)
        self.assertNotIn("Jnanin", response_text)

        # Expecting to get a single class back
        response = self.client.post("/findclass", {"category": "Category1", "date": "2022-10-1"})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.class_list_template_path)

        response_text = response.content.decode("utf-8")
        self.assertNotIn("Edanna", response_text)
        self.assertNotIn("Tomahna", response_text)
        self.assertIn("Amateria", response_text, "This should be the only result returned.")
        self.assertNotIn("Jnanin", response_text)

    def test_see_bookings_with_nothing_booked(self):
        self.create_and_authenticate_user()

        # GET request
        response = self.client.get("/seebookings")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.findclass_template_path)

        # POST request
        response = self.client.post("/seebookings", {"class_id": 123, "no_of_tickets": 234})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.findclass_template_path)

        response_text = response.content.decode("utf-8")
        self.assertIn("sorry no classes booked", response_text.lower())

    def test_make_and_view_bookings(self):
        # First we need to create an example Class
        initial_class_capacity = 10
        new_class = make_dummy_class(initial_class_capacity)

        # Then we want to make a booking for that class via a dummy user. Note, the number of tickets we request
        # needs to be less than "rem" ( - I believe this stands for "remaining places")
        self.create_and_authenticate_user()
        tickets_to_order = 4
        response = self.client.post("/bookings", {"class_id": new_class.id, "no_of_tickets": tickets_to_order})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.bookings_template_path)

        # Check that the class now has the adjusted remaining places
        adjusted_class = Class.objects.get(id=new_class.id)
        self.assertEqual(adjusted_class.rem, initial_class_capacity - tickets_to_order)

        # However when we try to request even more tickets for the same class, there won't be enough slots, so
        # we expect to get redirected with an error message
        response = self.client.post("/bookings", {"class_id": new_class.id, "no_of_tickets": 20})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.findclass_template_path)

        response_text = response.content.decode("utf-8")
        self.assertIn("sorry select fewer number of tickets", response_text.lower())

    def test_cancel_booking(self):
        # First make a class
        new_class = make_dummy_class(20)

        # Then make a booking for it
        user = self.create_and_authenticate_user()
        self.client.post("/bookings", {"class_id": new_class.id, "no_of_tickets": 10})

        # Check the booking looks good before we cancel it
        booking = Book.objects.filter(name=user.username).first()
        self.assertEqual(booking.no_of_tickets, 10)
        self.assertEqual(booking.status, "BOOKED")

        # Now cancel the booking
        self.client.post("/cancellings", {"class_id": new_class.id})
        booking = Book.objects.filter(name=user.username).first()
        self.assertEqual(booking.no_of_tickets, 0)
        self.assertEqual(booking.status, "CANCELLED")
