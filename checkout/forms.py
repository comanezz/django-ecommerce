from django import forms
from .models import Order
"""
    We let Stripe deal with the encryption of the credit card details.
And that's done through Stripe's JavaScript.
That means we can do required=false here in THE Django forms so that the plain text is not transmitted through the browser.
Therefore, it makes it more secure.
It's not visible to people who might be snooping on the webpage.
And Stripe actually requires an ID.
And although we're adding this to the form, the user won't actually see this.
So it's still a CharField.
And we're using this widget within forms called HiddenInput.
So this means that something will be inputted into the form, but it will be hidden from the user.
And that's something we'll look at in a future unit. You'll see where that data comes from.
So that's the payment form.
"""
class MakePaymentForm(forms.Form):

    MONTH_CHOICES = [(i, i) for i in range(1, 12+1)]
    YEAR_CHOICES = [(i, i) for i in range(2020, 2036+1)]

    credit_card_number = forms.CharField(label='Credit card number', required=False)
    cvv = forms.CharField(label='Security code (CVV)', required=False)
    expiry_month = forms.ChoiceField(label='Month', choices=MONTH_CHOICES, required=False)
    expiry_year = forms.ChoiceField(label='Year', choices=YEAR_CHOICES, required=False)
    stripe_id = forms.CharField(widget=forms.HiddenInput)


class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = (
            'full_name', 'phone_number', 'country', 'postcode',
            'town_or_city', 'street_address1', 'street_address2',
            'county'
        )