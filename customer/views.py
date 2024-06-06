import email
from os import name
from django.shortcuts import render
from django.shortcuts import redirect
from django.views import View
from django.core.mail import send_mail 
from .models import MenuItem , Category , OrderModel

# Create your views here.

class Index(View):
    def get(self , request , *args , **kwargs):
        return render(request , 'customer/index.html')
    
class About(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/about.html')

#hadi lclass t3 l'ordre li ydiro lclient
#function get bah njibo l'items mn bdd w naffichiwhom f interface 
#
class Order(View):
    def get(self, request, *args, **kwargs):
        # get every item from each category
        FastFoods = MenuItem.objects.filter( category__name__contains='FastFood')
        TraditionalFoods = MenuItem.objects.filter(category__name__contains='TraditionalFood')
        desserts = MenuItem.objects.filter(category__name__contains='Dessert')
        drinks = MenuItem.objects.filter(category__name__contains='Drink')


            # pass into context
        context = {
            'FastFoods': FastFoods,
            'TraditionalFoods': TraditionalFoods,
            'desserts': desserts,
            'drinks': drinks,
        }

            # render the template
        return render(request, 'customer/order.html', context)
    
    #had function nst9blo les data li khyrhom lclient 
    # ytzado f l bdd 
    # nafichiw confirmation d'ordre fiha prix w l'ordre
    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        price = request.POST.get('price')
        email = request.POST.get('email')
        street = request.POST.get('street')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip')

        order_items = {  
            'items': []
        } 

        items = request.POST.getlist('items[]')

        for item in items:
            menu_item = MenuItem.objects.get(pk=int(item))
            item_data = {
                'id': menu_item.pk,
                'name': menu_item.name,
                'price': menu_item.price
            }

            order_items['items'].append(item_data)

            price = 0
            item_ids = []

        for item in order_items['items']:
            price += item['price']
            item_ids.append(item['id'])

        order = OrderModel.objects.create(
            price=price , 
            name=name ,
            email=email,
            city=city,
            street=street,
            state = state,
            zip_code=zip_code
           )
        order.items.add(*item_ids)
        
        body = ('Thank you for your order! Your food is being made and will be delivered soon!\n'
                f'Your total: {price}\n'
                'Thank you again for your order!')
        
        send_mail(
            'Thank You For Your Order!',
            body,
            'example@example.com',
            [email],
            fail_silently=False
        )
        context = {
            'items': order_items['items'],
            'price': price
        }

        return redirect('order-confirmation', pk=order.pk)
        
    

    class OrderConfirmation (View):
        def get(self , request, pk , *args, **kwargs ):
            order = OrderModel.objects.get(pk=pk)
            context ={
                'pk' : Order.pk ,
                'items' : Order.Item , 
                'price' : Order.price

            }
            return render(request, 'customer/order_confirmation.html', context)
        def post (self , request , pk , *args, **kwargs):
            return(request.body)