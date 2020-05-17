"""Unlike the products app, where we created a model which then puts products into our database,
in this case, the cart items will not go into the database.
They will just be stored in the session when the user is logged in.
So a user can add products to their cart, but when they log out, that cart will be lost.
"""

from django.shortcuts import get_object_or_404
from products.models import Product

"""We're going to give it the name contexts.py.
Unlike the products app, where we created a model which then puts products into our database, in this case, the cart items will not go into the database.
They will just be stored in the session when the user is logged in.
So a user can add products to their cart, but when they log out, that cart will be lost.
So this is a little bit different from what we've done before.
So you can see there, we've had to import our product from our products.models.
And we create a method called cart_contents().
What this is going to do is allow anything that's added to the cart to be available for display on any web page within the web app.
So whereas before, if you think back to our all_products view, that was only able to take products because we put the products into a dictionary within the render.
That's actually more properly called a context.
So in this case, we are creating a context that is available to all pages.
So we have a cart that requests the session.
So it requests the existing cart if there is one, or a blank dictionary if there's not.
And we initialize cart_items, total, and product_count.
And then we do a for loop.
It takes two things: an ID and a quantity from your cart_items.
So the ID will be which product ID it is, and the quantity is how many the user wishes to purchase.
We need our products, which we get from our product model.
And we use the primary key as our ID, as every product within our database will have a primary key, which is a unique ID.
So here, we have total +=.
So our total will just take the quantity of items multiplied by their price and add them to a continuous running total of the cost.
Our product_count just keeps on adding the quantity.
So as you add more quantity as a user, your product count goes up.
And then we append those cart_items to our cart.
So we have the ID and the quantity.
So we will always know the ID, the unique ID, of each product and the quantity of that product that has been added.
And then what we return here is a dictionary.
And we return key value pairs for cart_items, total, and product_count.
So we save this and go to our settings.
Under templates, you see we have this thing called context_processors.
Context_processors are a list of things that are available on every webpage.
So we add our own cart.contexts.cart_contents to this list.
"""

def cart_contents(request):
    """
    Ensures that the cart contents are available when rendering
    every page
    """
    cart = request.session.get('cart', {})

    cart_items = []
    total = 0
    product_count = 0
    
    for id, quantity in cart.items():
        product = get_object_or_404(Product, pk=id)
        total += quantity * product.price
        product_count += quantity
        cart_items.append({'id': id, 'quantity': quantity, 'product': product})
    
    return {'cart_items': cart_items, 'total': total, 'product_count': product_count}