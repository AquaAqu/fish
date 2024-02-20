import razorpay 
import six
from django.conf import settings
from django.http import JsonResponse #import this
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt #import this
from django.http import HttpResponseBadRequest #import this
razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
from django.shortcuts import render
from . models import reg,fishpro,addcart,pay


# Create your views here.
def index(request):
    return render(request,'index.html')

def contact(request):
    return render(request,'contact.html')


def home(request):
    return render(request,'home.html')


def adhome(request):
    return render(request,'adhome.html')


#def contact(request):
 #   return render(request,'contact.html')


def userreg(request):
    if request.method=="POST":
        a=request.POST.get("name")
        b=request.POST.get("address")
        c=request.POST.get("mobile")
        d=request.POST.get("email")
        e=request.POST.get("password")
        f=request.POST.get("cpassword")
        reg(name=a,address=b,mobile=c,email=d,password=e,conformpassword=f).save()
        print("User Registered....")
        return render(request,'userlogin.html')
    else:
        return render(request,'userreg.html')

def userlogin(request):
    if request.method=="POST":
        email=request.POST.get("email")
        password=request.POST.get("password")
        cr=reg.objects.filter(email=email,password=password)
        if cr:
            userd=reg.objects.get(email=email,password=password)
            id=userd.id
            email=userd.email
            name=userd.name
            password=userd.password
            request.session['name']=name
            request.session['email']=email
            print("Login Successfull")
            return render(request,'home.html')
        else:
            return render(request,'userlogin.html')
    else:
            return render(request,'userlogin.html')


    
def shop(request):
    return render(request,'shop.html')


def adlogin(request):
    if request.method=='POST':
        name = request.POST.get('name')
        password = request.POST.get('password')
        u='admin'
        p='admin'
        if name==u:
            if password==p:
                return render(request,"adhome.html")
            else:
                return render(request,"adlogin.html")
        else:
            return render(request,"adlogin.html") 
    else:
        return render(request,'adlogin.html')

def adproduct(request):
    if request.method=='POST':
        a=request.POST.get('fname')
        b=request.POST.get('description')
        c=request.POST.get('breed')
        d=request.POST.get('status')
        e=request.POST.get('price')
        f=request.FILES['image']
        fishpro(fname=a,description=b,breed=c,status=d,price=e,image=f).save()
        return render(request,'index.html')
    else:
        return render(request,'adproduct.html')


def listpro(request):
    data=fishpro.objects.all()
    return render(request,'listpro.html',{'x':data})

def list(request):
    a=fishpro.objects.all()
    return render(request,'list.html',{'data':a})



def cart(request,id):
    dt=fishpro.objects.get(id=id)
    a=dt.fname
    b=dt.description
    d=dt.price
    e=dt.image

    email=request.session['email']
    print(email)
    cr=reg.objects.get(email=email)

    name=cr.name
    mobile=cr.mobile

    return render(request,'add_to_cart.html',{'fishname':a,'description':b,'price':d,'image':e,'name':name,'mobile':mobile})

def add_to_cart(request):
    if request.method=='POST':
        a=request.POST.get('fname')
        b=request.POST.get('description')
        c=request.POST.get('price')
        d=request.POST.get('image')

        e= request.session['email']
        cr= reg.objects.get(email=e)

        f=cr.name
        g=cr.mobile
        addcart(fname=a,description=b,price=c,image=d,name=f,mobile=g).save()
        return render(request,'home.html')
    else:
        return render(request,'add_to_cart.html')
    

def cartlist(request):
    name=request.session['name']
    cr=addcart.objects.filter(name=name)
    return render(request,'cartlist.html',{'x':cr})

def delete(request,id):
    cr=addcart.objects.get(id=id)
    cr.delete()
    return render(request,'index.html')

def delete1(request,id):
    cr=addcart.objects.get(id=id)
    cr.delete()
    return render(request,'index.html')


# payment view

def payment(request):
    nm=request.session['name']
    cr=addcart.objects.filter(name=nm)
    totalprice = 0
    
    for i in cr:
     pay(fname=i.fname, price=i.price, name=i.name, mobile=i.mobile).save()
     totalprice += int(i.price)
     i.delete()
    
    totalprice = int(totalprice*100)
    amount=int(totalprice)
    #amount=200
    print('amount is',str(amount))
    currency = 'INR'
    #amount = 20000  # Rs. 200

    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                       currency=currency,
                                                       payment_capture='0'))
 
    # order id of newly created order.
    razorpay_order_id = razorpay_order['id']
    callback_url = 'paymenthandler/'
 
    # we need to pass these details to frontend.
    context = {}
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url
 
    return render(request, 'payment.html', context=context)
 
@csrf_exempt
def paymenthandler(request):
 
    # only accept POST request.
    if request.method == "POST":
        try:
           
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
 
            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(
                params_dict)
            if result is not None:
                amount = 20000  # Rs. 200
                try:
 
                    # capture the payemt
                    razorpay_client.payment.capture(payment_id, amount)
 
                    # render success page on successful caputre of payment
                    return render(request, 'pay_success.html')
                except:
 
                    # if there is an error while capturing payment.
                    return render(request, 'pay_failed.html')
            else:
 
                # if signature verification fails.
                return render(request, 'pay_failed.html')
        except:
 
            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
       # if other than POST request is made.
        return HttpResponseBadRequest()

