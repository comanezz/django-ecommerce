from django.contrib import admin
from .models import Order, OrderLineItem
"""So we import Order and OrderLineItem.
We're creating a class here, OrderLineAdmin.
And that inherits from the TabularInline within admin.
And it uses the OrderLineItem as a model for that.
And then we're creating a class, OrderAdmin, which inherits from the ModelAdmin of the admin Django.
That just takes inlines, which is the OrderLineAdmin inline that we created above.
And then we just need to register both of these with the admin site so that we can edit them if necessary.
Now, because we've created models, we have to do a makemigrations and then a migrate.
And that will create the tables within our database.
"""


"""
    TabularInline subclasses defines the template used to render the Order in the admin interface.
    StackedInline is another option
"""
class OrderLineAdminInline(admin.TabularInline):
    model = OrderLineItem


class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderLineAdminInline, )


admin.site.register(Order, OrderAdmin)