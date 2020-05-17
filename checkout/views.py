from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import MakePaymentForm, OrderForm
from .models import OrderLineItem
from django.conf import settings
from django.utils import timezone
from products.models import Product
import stripe

# Create your views here.
"""
We also are going to import auth.decorators login_required because you want your customer to be logged 
in when they actually purchase something.
When they actually go to the checkout and say I want to pay, they should be logged in.
"""
stripe.api_key = settings.STRIPE_SECRET


@login_required()
def checkout(request):
    if request.method == "POST":
        order_form = OrderForm(request.POST)
        payment_form = MakePaymentForm(request.POST)

        if order_form.is_valid() and payment_form.is_valid():
            order = order_form.save(commit=False)
            order.date = timezone.now()
            order.save()

            cart = request.session.get('cart', {})
            total = 0
            for id, quantity in cart.items():
                product = get_object_or_404(Product, pk=id)
                total += quantity * product.price
                order_line_item = OrderLineItem(
                    order=order,
                    product=product,
                    quantity=quantity
                )
                order_line_item.save()
            
            """Now that we know what they want to buy, we're putting in a try except here.
                And that try except will create a customer charge.
                So that's using Stripe's in-built API here.
                And we have to give it an amount of money that we wish.
                So that's going to be an integer.
                And it's our total * 100 because Stripe uses everything in cents or pennies.
                So 10 Euro would be 1,000 cents, for example.
                We've defined here that our currency is Euro.
                And our description is going to be the request user email.
                And that just means that we can see from Stripe, if we go to our Stripe dashboard,
                you'll be able to see who the payment came from.
                And we also need the Stripe ID from that form.
                Now, that was the the item that was hidden from the user.
            """
            
            try:
                customer = stripe.Charge.create(
                    amount=int(total * 100),
                    currency="EUR",
                    description=request.user.email,
                    card=payment_form.cleaned_data['stripe_id']
                )
                """So the except part of this is the error.
                So this is if the card has been declined.
                So stripe will do all the security stuff behind this, but, of course, we still need to inform our customer if something has gone wrong in that process.
                """
            except stripe.error.CardError:
                messages.error(request, "Your card was declined!")
            
            if customer.paid:
                messages.error(request, "You have successfully paid")
                request.session['cart'] = {}
                return redirect(reverse('products'))
            else:
                messages.error(request, "Unable to take payment")
        else:
            print(payment_form.errors)
            messages.error(request, "We were unable to take a payment with that card!")
    else:
        payment_form = MakePaymentForm()
        order_form = OrderForm()
    
    return render(request, "checkout.html", {"order_form": order_form, "payment_form": payment_form, "publishable": settings.STRIPE_PUBLISHABLE})