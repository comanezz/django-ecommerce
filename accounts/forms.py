from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

class UserLoginForm(forms.Form):
    """Form to be used to log users in"""

    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class UserRegistrationForm(UserCreationForm):
    """Form used to register a new user"""

    password1 = forms.CharField(
        label="password",
        widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password Confirmation",
        widget=forms.PasswordInput)
    
    """we need to do is create an inner class an inner class is a class that we can use that will provide
    just some information about this form these are called meta classes and Django usually uses them internally
    to determine things about the class but we can also use it to specify the model that we want store information
    in and we want we want to use it to specify the fields that we're going to expose which our email, username,
    password1 and password2
    """
    class Meta:
        model = User
        fields = ['email', 'username', 'password1', 'password2']

    """we need to implement some form validation and the way django handles this is it takes a form
    and any form object that contains a cleaned _field name method it will use that method to clean
    that field or validate that field so clean underscore email will allow us to clean the email field
    and it will expect us to return the email once we're done so we can do we can do this by passing
    in the self object and the self contains the cleaned data that has been cleaned by Django it's the
    clean data that we would use when we use the .is_valid method and these are called as a result so
    we get the email by doing self.cleaned_data.get('email') and we do the same for username and then
    what we do is we filter to check to see if we have someone in the database with that email address
    already and if we do then we return a validation error to say that the email address must be unique
    after that we just return the email
    """

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if User.objects.filter(email=email).exclude(username=username):
            raise forms.ValidationError(u'Email address must be unique')
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if not password1 or not password2:
            raise ValidationError("Please confirm your password")
        
        if password1 != password2:
            raise ValidationError("Passwords must match")
        
        return password2