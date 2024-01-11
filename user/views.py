from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .froms import UserRegistrationForm, UserLoginForm
from django.contrib.auth import login,authenticate, logout
from django.contrib.auth.decorators import login_required,user_passes_test
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import random
from  django.contrib import  messages
from string import ascii_letters
import itertools
from .models import Transaction, User
import string
from django.conf import settings
from .utils import initialize_transaction, verify_transaction, verify_by_reference
# Create your views here.

def generate_code():
    size = random.randint(10, 15)
    result = ''.join(random.choices("123456789", k=size))
    for  i in itertools.count(1):
        if result not in User.objects.filter(qr_id=result).values_list('qr_id',flat=True):
            break
        generate_code()

    return result


def create_ref():
    size = random.randint(11, 15)
    result = ''.join(random.choices("123456789" + string.ascii_letters, k=size))
    for  i in itertools.count(1):
        if result not in User.objects.filter(qr_id=result).values_list('qr_id',flat=True):
            break
        generate_code()

    return result




def home_page(request):
    html_template='user/index.html'

    return render(request, html_template, {})


def register(request):
    if not request.user.is_authenticated:
        if request.method=='POST':
            form=UserRegistrationForm(request.POST)
            if form.is_valid():
                form.save()
                new_user= authenticate(email=form.cleaned_data['email'],password=form.cleaned_data['password1'])
                login(request,new_user)
                return redirect('index')
        else:
            form=UserRegistrationForm()  
    else:
        return redirect('index') 

    return render(request,'user/register.html',{'form':form})


def web_login(request):
    if not request.user.is_authenticated:
        if request.method=='POST':
            form=UserLoginForm(request.POST)
            if form.is_valid():
                new_user= authenticate(email=form.cleaned_data['email'],password=form.cleaned_data['password'])
                login(request,new_user)
                return redirect('index')
        else:
            form=UserRegistrationForm()  
    else:
        return redirect('index') 

    return render(request,'user/login.html',{'form':form})


def web_logout(request):
    logout(request)
    
    messages.success(request, "You have logged out successfully")
    return redirect('index')


@require_POST
@csrf_exempt
def payment_webhook(request):
    secret_hash = settings.HASH_ENC
    signature = request.headers.get("verifi-hash")
    if signature == None or (signature != secret_hash):
        # This request isn't from Flutterwave; discard
        return HttpResponse(status=401)
    payload = request.body
    verified= verify_transaction(payload['data'['id']])

    try:
        if verified["status"]== "success":
            user_mail= verified["data"]["tx_ref"].split("-")[-1]
            user= User.objects.get(email= user_mail)
            trans= Transaction.objects.get(payer= user, reference=verified["data"]["tx_ref"])
            if trans.completed==False:
                user.balance += int(verified["data"]["amount"])
                trans.completed == True
                trans.save()
                user.save()
                return HttpResponse(status=200)
    except:
        return HttpResponse(status=401)
    # It's a good idea to log all received events.
    print(payload)
    # Do something (that doesn't take too long) with the payload
    return HttpResponse(status=200)


@csrf_exempt
def callback_endpoint(request):
    ref= request.GET.get('tx_ref', None)
    if not ref:
        return HttpResponse(status=401)
    
    verified= verify_by_reference(ref)
    try:
        if verified["status"]== "success":
            user_mail= verified["data"]["tx_ref"].split("-")[-1]
            user= User.objects.get(email= user_mail)
            trans= Transaction.objects.get(payer= user, reference=verified["data"]["tx_ref"])
            if trans.completed==False:
                user.balance += int(verified["data"]["amount"])
                trans.completed == True
                trans.save()
                user.save()
                return redirect('web_profile')
    except:
        return redirect('web_profile')
    # It's a good idea to log all received events.
    print(verified)
    # Do something (that doesn't take too long) with the payload
    return redirect('web_profile')

# https://swiftstand.net/?status=completed&tx_ref=trans-hq2haicMTpckg-ade%40gmail.com&transaction_id=4844832

@login_required
def web_profile(request):
    html_template='user/profile.html'
    paystack_key= settings.PUBLIC_KEY

    if request.method=='POST':
        if int(request.POST['amount']) > 80000 or int(request.POST['amount']) < 100:
            messages.warning(request, 'you can only fund between the range of 100 - 80,000')
            return redirect('web_profile')
        pay_ref= create_ref()
        trans_ref = f"trans-{pay_ref}-{request.user.email}"
        new_transaction = Transaction.objects.create(payer=request.user,amount=int(request.POST['amount']), description="Flutterwave Gateway", reference=trans_ref, add=True, completed= False)
        new_transaction.branch_name = "Self Funding"
        new_transaction.is_branch = False
        new_transaction.save()

        red_url= f"{settings.MY_SITE}/arole/callback/"
        pay_load= {
                "public_key": paystack_key, 
                "tx_ref": trans_ref,
                "amount": request.POST['amount'],
                "currency": "NGN",
                "payment_options": "banktransfer, card",
                "redirect_url": "" +  red_url,
                # "webhook_url": #settings.MY_SITE + f"/arole/pay/webhook/",
                # "meta": {
                #     "consumer_id": 23,
                #     "consumer_mac": "92a3-912ba-1192a",
                # },
                "customer": {
                    "email": request.user.email,
                    "name": request.user.fullname,
                },
                "customizations": {
                    "title": "Arole E-wallet funding",
                    # logo: "https://www.logolynx.com/images/logolynx/22/2239ca38f5505fbfce7e55bbc0604386.jpeg",
                },
            }
        
        print("LOAD : ", pay_load)
        trans_info= initialize_transaction(pay_load)
        try:
            checkout_url= trans_info['data']['link']
            return HttpResponseRedirect(checkout_url)
        except:
            messages.error(request, f"Unabble to fund: {request.POST['amount']}")

    return render(request, html_template, {'pay_key': paystack_key})


@login_required
def display_qr(request):
    html_template='user/display_qr.html'

    if request.user.qr_id:
        data = dict(
            exists = True,
            new_code = generate_code(),
            code = request.user.qr_id,
            pay_code= request.user.pay_code,
            flaggy = "1"
        )
    else:
        print("Now : ", request.user.pay_code)
        data = dict(
            exists = False,
            new_code = generate_code(),
            code = None,
            pay_code= request.user.pay_code,
            flaggy = "0"
        )

    return render(request, html_template, data)


@login_required
def web_save_qr(request):
    body= request.POST
    code = body["new_code"]
    pay =  body["website"]

    user = User.objects.get(pk = request.user.pk)

    if user.qr_id:
        msg= "You have generated a new QR-CODE successfully, the previous one has been terminated"
    else:
        msg= "You now have a new qr code show it any of our branch to be scanned so you can pay"
    user.qr_id = code
    user.pay_code = pay
    user.save()

    messages.success(request, msg)
    return redirect("web_profile")
