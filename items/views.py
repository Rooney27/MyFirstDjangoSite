from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views import View
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from .forms import OrderForm
import json
import datetime
# Create your views here.

class ItemsListView(ListView):
    model = Item
    template_name = 'items/items_list.html'
    def get_queryset(self):
        categories = list(str(a.id) for a in Category.objects.all())
        query_category = self.request.GET.get('category')
        a = self.request.GET.dict()
        if query_category in categories:
            return Item.objects.filter(category=query_category)
        else: return Item.objects.all()
    def get_context_data(self):
        context = super().get_context_data()
        context['categories'] = {a.id:a.title for a in Category.objects.all()}
        if self.request.session.get('my_cart', '')!='':
            dict_cart = json.loads(self.request.session.get('my_cart', ''))
            print(dict_cart)
            cart_obj_list = list()
            cart_count_list = list()
            for key,value in dict_cart.items():
                obj = Item.objects.filter(id=key)
                count = value
                cart_obj_list.append((obj))
                cart_count_list.append(count)
            context['cart'] = zip(cart_obj_list,cart_count_list)

        return context


class ItemsDetailView(DetailView):
    model = Item
    template_name = 'items/items_detail.html'
    queryset = Item.objects.all()
    context_object_name = 'item'

class OrderFormView(View):

    def get(self,request):
        order_form = OrderForm()
        if self.request.session.get('my_cart', '')!='':
            dict_cart = json.loads(self.request.session.get('my_cart', ''))
            print(dict_cart)
            cart_obj_list = list()
            cart_count_list = list()
            for key,value in dict_cart.items():
                obj = Item.objects.filter(id=key)
                count = value
                cart_obj_list.append((obj))
                cart_count_list.append(count)
            cart = zip(cart_obj_list,cart_count_list)
        
        return render(request, 'items/order.html', context={'order_form':order_form,'cart':cart})
    def post(self, request):
        order_form = OrderForm(request.POST)
        print(order_form.is_valid())
        if self.request.session.get('my_cart', '')!='':
            print(self.request.session.get('my_cart', ''))
            
            if order_form.is_valid():
                print(order_form.cleaned_data)
                order = Order.objects.create(**order_form.cleaned_data)

                dict_cart = json.loads(self.request.session.get('my_cart', ''))
                cart_obj_list = list()
                cart_count_list = list()
                for key,value in dict_cart.items():
                    item = Item(id=key)
                    count = value
                    for obj in Item.objects.filter(id=key):
                        obj_price = obj.price
                    price = obj_price*count
                    item = OrderItem.objects.create(item=item,count=count,price=price,order=order)
                    self.request.session['my_cart']=''

                return render(request, 'items/order_ok.html', context={'order_form':order_form})
            return HttpResponse('Данные не валидны')
        return HttpResponse('Корзина пуста, для заказа добавьте в неё товар')

class Cart(View):
    def addToCart(self,request):
        if request.GET.get('item'):
            chek_item_in_bd = len(Item.objects.filter(id=request.GET.get('item')))
            if chek_item_in_bd==1:
                if request.session.get('my_cart', '')!='':
                    print('first if')
                    dict_cart = json.loads(request.session['my_cart'])
                    if request.GET.get('item') in dict_cart:
                        print('second if')
                        dict_cart[request.GET.get('item')] += 1
                        request.session['my_cart']= json.dumps(dict_cart)
                        return json.dumps(dict_cart)
                    else:
                        print('second else')
                        dict_cart[request.GET.get('item')] = 1
                        request.session['my_cart']= json.dumps(dict_cart)
                        return json.dumps(dict_cart)
                        
                else:
                    print('first else')
                    dict_cart = {request.GET.get('item'):1}
                    json.dumps(dict_cart)
                    request.session['my_cart']= json.dumps(dict_cart)
                    return json.dumps(dict_cart)
            else:
                return 'error'
        else:
            return 'error'
    def delFromCart(self,request):
        if request.session.get('my_cart', '')!='':
            if request.GET.get('item'):
                dict_cart = json.loads(request.session['my_cart'])
                if request.GET.get('item') in dict_cart:
                    if dict_cart[request.GET.get('item')]>1:
                        dict_cart[request.GET.get('item')]-=1
                    else:
                        del dict_cart[request.GET.get('item')]
                    request.session['my_cart']= json.dumps(dict_cart)
                    return json.dumps(dict_cart)
                else:
                    return 'error'
            else:
                return 'error'
        else:
            return 'error'
    def updateCart(self,request):
        if request.session.get('my_cart', '')!='':
            return request.session.get('my_cart', '')
        else:
            return ''
    def clearCart(self,request):
        request.session['my_cart']=''
        return ''



    def get(self,request):
        errors = dict()
        errors["400"] = "bad request"
            
        if request.GET.get('query'):
            if request.GET.get('query')=='add':
                add_result = self.addToCart(request)
                if  add_result != 'error':
                    print(add_result)
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))
                    #return HttpResponse(add_result, status=200, content_type="application/json")
                else:
                    return HttpResponse(errors['400'],status=400)
            if request.GET.get('query')=='del':
                del_result = self.delFromCart(request)
                if  del_result != 'error':
                    print(del_result)
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))
                    #return HttpResponse(del_result, status=200, content_type="application/json")
                else:
                    return HttpResponse(errors['400'],status=400)
            if request.GET.get('query')=='update':
                self.updateCart(request)
                return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))
            if request.GET.get('query')=='clear':
                self.clearCart(request)
                return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))


        else:
            return HttpResponse(errors['400'],status=400)
        