from django.shortcuts import render, redirect, reverse
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from accounts.forms import UserLoginForm, UserRegistrationForm

# Create your views here.
def index(request):
    """Return the index.html file"""
    return render(request, "index.html")

# @login_required is a decorator that check to see if the user is logged in before executing any more of the code
@login_required
def logout(request):
    """Log the user out"""
    auth.logout(request)
    messages.success(request, "You have successfully been logged out!")
    """in order for this to work is we need to update our settings.py file so open up my settings.py file
    and then scroll down to the very bottom I'm going to create a new setting called message storage 
    I'm going to say give it a string that says django.contrib .messages.storage.session.SessionStorage
    MESSAGE_STORAGE = "django.contrib.messages.storage.session.SessionStorage"
    """
    # the reverse allows us to pass the name of a URLs instead of a name of a view
    return redirect(reverse('index'))

def login(request):
    """Return a login page"""
    if request.user.is_authenticated:
        # Avoid user already logged in to be able to view the login page and being redirected to index page
        # User won't be able to access the login page even if he enters the URL
        return redirect(reverse('index'))

    if request.method == "POST":
        login_form = UserLoginForm(request.POST)

        if login_form.is_valid():
            """this will authenticate the user this will tell us whether or not this user has provided the right
            username and password
            """
            user = auth.authenticate(username=request.POST['username'],
                                    password=request.POST['password'])
            

            if user:
                auth.login(user=user, request=request)
                messages.success(request, "You have successfully logged in!")
                return redirect(reverse('index'))
            else:
                # we can say none so this will just display on the form as opposed to a specific input
                login_form.add_error(None, "Your username or password is incorrect")
    else:
        login_form = UserLoginForm()
    return render(request, "login.html", {"login_form": login_form})

def registration(request):
    """Render the registration page"""
    if request.user.is_authenticated:
        return redirect(reverse('index'))

    if request.method == "POST":
        registration_form = UserRegistrationForm(request.POST)

        """we already specified the model inside of our meta class on our registration form
        we don't need to specify model again here
        """
        if registration_form.is_valid():
            registration_form.save()

            """once weve created the user then we're just going to log the user in"""
            user = auth.authenticate(username=request.POST['username'],
                                     password=request.POST['password1'])
            # Once the user has been authenticated we can log him in
            if user:
                auth.login(user=user, request=request)
                messages.success(request, "You have successfully registered")
            else:
                messages.error(request, "Unable to register your account at this time")
    else:
        registration_form = UserRegistrationForm()
    return render(request, 'registration.html', {
        "registration_form": registration_form})

def user_profile(request):
    """The user's profile page"""
    user = User.objects.get(email=request.user.email)
    return render(request, 'profile.html', {"profile": user})