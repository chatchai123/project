from collections import defaultdict
from datetime import datetime,timedelta
from django.db.models import Case, IntegerField, Value, When
import requests
from django.http import HttpResponse
from django.shortcuts import redirect, render
from app.forms import *
#from linebot import LineBotApi
#from linebot.models import TextSendMessage
from app.models import *
from django.contrib.auth.models import User,auth
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from app.models import *
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect, HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate,logout,login as auth_login
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db import transaction

def getdate(x=None,th=None):
    '''
    get_month = thai_month_dict[current_date.month]
    formatted_date = f"{current_date.year}-{get_month}-{current_date.day}"
    date = datetime.strptime(formatted_date, '%Y-%m-%d').date()
    '''
    #เพื่อ เอาวันที่แบบตัวหนังสือ ปี-เดือน-วัน
    if x:
        current_date = x
        print(current_date,'xxxxxxxxxx')
        return f'{current_date.year}-{current_date.month}-{current_date.day}'
    

    
    #เพื่อ เอาวันที่แบบตัวหนังสือ แบบไทย 4 ธันวาคม 2023
    else:
        if th:
            date = th
            current_date = datetime.strptime(date, '%Y-%m-%d').date()
            print(current_date,'yyyyyyyyyyyyyy')
    
        else:
            current_date = datetime.now()
            print(current_date,'ppppppppppppppppp')
            return f'{current_date.year}-{current_date.month}-{current_date.day}'

        thai_month_dict = {
        1:"มกราคม",
        2:"กุมภาพันธ์",
        3:"มีนาคม",
        4:"เมษายน",
        5:"พฤษภาคม",
        6:"มิถุนายน",
        7:"กรกฎาคม",
        8:"สิงหาคม",
        9:"กันยายน",
        10:"ตุลาคม",
        11:"พฤศจิกายน",
        12:"ธันวาคม",}
        get_month = thai_month_dict[current_date.month]
        return f'{current_date.day} {get_month} {current_date.year}'

#------------------------------------------------------------------

# Create your views here.

def home(req):
    food = Food.objects.all()
    context ={
        'food':food,
    }
    return render(req,'app/home.html',context)
def create(req):
    form = FoodForm()
    if req.method =='POST':
        form = FoodForm(req.POST,req.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {
        'form':form
    }
    return render(req,'app/create.html',context)

def search(req):
    if req.method =='POST':
        text = req.POST['text-search']
        if text:
            food = Food.objects.filter(name__contains=text)
            if food:
                return render(req,'app/search.html',{'food':food})
            else:
                return render(req,'app/search.html',{'text':'ไม่พบเมนูอาหารที่ท่านค้นหา'}) 
        else:
            return render(req,'app/search.html',{'text':'กรุณาเพิ่มเมนูอาหารที่ท่านต้องการค้นหา'}) 

        
    else:
        return render(req,'app/search.html',{'text':'กรุณาเพิ่มเมนูอาหารที่ท่านต้องการค้นหา'}) 

def select_date(req):
    if req.method =='POST':
            form_date = DateForm(req.POST)

            if form_date.is_valid():
                date = form_date.cleaned_data['date_field']
                print(date)
                get_date = getdate(date)
                print('get_date:',get_date)
                currect_date = getdate(datetime.now().date())
                print('currect_date:',currect_date)
                #ทำการเปรียบเทียบ ถ้าวันที่ ที่ส่งมาเป็นเมื่อวานหรือมากกว่านั้น ให้ รีเทิร์น history.html ไป แต่ ถ้าเป็นปัจจุบันก็รีเทิร์น managefood.html
                # currect_date > get_date = เมื่อวาน
                if currect_date > get_date:

                    food_history = Historysale.objects.filter(date_field=get_date)
                    foods = []
                    for history in food_history:
                        if history.food:
                            foods.append(history.food)
                    print(foods)
                    form_date = DateForm()
                    thai_date = getdate(None,get_date)
                    print(thai_date)
                    context ={
                        'date':get_date,
                        'thai_date':thai_date,
                        'food':foods,
                        'form':form_date,
                    }
                    return render(req,'app/historysales.html',context)
                # currect_date < get_date = เมื่อวาน
                elif currect_date < get_date:
                    food_history = Historysale.objects.filter(date_field=get_date)
                    foods = []
                    for history in food_history:
                        if history.food:
                            foods.append(history.food)
                    print(foods)
                    form_date = DateForm()
                    thai_date = getdate(None,get_date)
                    print(thai_date)
                    context ={
                        'date':get_date,
                        'thai_date':thai_date,
                        'food':foods,
                        'form':form_date,
                    }
                    return render(req,'app/historysales.html',context)
                # present
                else:
                   print('44444444444444')
                   return redirect('/managefood/')
    else:
            food = Food.objects.all()
            form_date = DateForm()
            get_date = getdate()
            thai_date = getdate(None,get_date)


    context ={
        'date':get_date,
        'thai_date':thai_date,
        'food':food,
        'form':form_date,
    }
    return render(req,'app/managefood.html',context)

def clearfood(req):
    if req.method=='POST':
        #Food.objects.exclude(options='notchoose').update(options='notchoose')
        food = Food.objects.all()
        for f in food:
            if f.options != 'notchoose':
                print('setsetset')
                print(f)
                f.options = 'notchoose'
                f.save()
        return redirect('managefood')
    else:
        return redirect('managefood')
def updatefood(req,id):
    if req.method=='GET':
        food = Food.objects.get(pk=id)
        form = FoodForm(instance=food)
    else:
        food = Food.objects.get(pk=id)
        form = FoodForm(req.POST,req.FILES,instance=food)
        if form.is_valid():
            form.save()
            return redirect('managefood')
    context ={
        'food':food,
        'form':form,
    }
    return render(req,'app/updatefood.html',context)

def reviewfood(req,id):
    food = Food.objects.get(pk=id)
    print(food)
    if req.method =='GET':
        form = FeviewFood(instance=food)
        print(food.id)
        print(form.instance.id)
    else:
        form = ReviewFood(req.POST,req.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            review.food = food
            review.save()
            return redirect('home')
        
    context = {
        'form':form,
        'food':food,
    }
    return render(req,'app/review.html',context)


def managefood(req,date=None):

    if req.method =='POST':
        food_ids = req.POST.getlist('food_id')
        print(food_ids)
        options = req.POST.getlist('options')
        print(options)
        if len(food_ids) == len(options):
            for id, option in zip(food_ids, options):
                food_item = Food.objects.get(pk=id)
                print(food_item,f'pass {option}')


                #ถ้า option is notchoose if notchoose delete out database
                if option == 'notchoose':
                    found = Historysale.objects.filter(food_id=food_item.id , date_field = date )
                    print(found)
                    if found.exists():
                        food_item.options = option
                        food_item.save()
                        found.delete()
                        print('ลบสำเร็จ')
                    else:
                        print('111111111')

                #if option is onsale if onsale save to database
                if option == 'onsale':
                    if Historysale.objects.filter(id=food_item.id , date_field = date ).exists():
                        if food_item.options != option:
                            food_item.options = option
                            food_item.save()
                            print('เปลี่ยนแปลงข้อมูลสำเร็จ')
                        else:
                            pass
                    else:
                        food_item.options = option
                        food_item.save()
                        history_sale= Historysale.objects.create(
                        food=food_item,
                        date_field= date)
                        print('เซฟข้อมูลงฐานข้อมูลได้')

                #if option is soldout same onsale

                elif option == 'soldout':
                    if Historysale.objects.filter(id=food_item.id , date_field = date ).exists():
                        if food_item.options != option:
                            food_item.options = option
                            food_item.save()
                            print('เปลี่ยนแปลงข้อมูลสำเร็จ')

                        else:
                            pass
                    else:
                        food_item.options = option
                        food_item.save()
                        history_sale= Historysale.objects.create(
                        food=food_item,
                        date_field= date)
                        print('เซฟข้อมูลงฐานข้อมูลได้')

        return redirect('managefood')
    else:
        food = Food.objects.all()
        form_date = DateForm()
        get_date = getdate()
        thai_date = getdate(None,get_date)

                

        context ={
            'date':get_date,
            'thai_date':thai_date,
            'food':food,
            'form':form_date,
        }
        return render(req,'app/managefood.html',context)


def admin1(request):
    return render(request, 'admin/admin1.html', {'user': request.user})


@login_required
def edit_profile(request):
    user_profile = request.user.userprofile

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            day = request.POST.get('day')
            month = request.POST.get('month')
            year = request.POST.get('year')
            birth_date_str = f"{year}-{month}-{day}"
            birth_date = datetime.strptime(birth_date_str, "%Y-%m-%d").date()
            user_profile.birth_date = birth_date
            user_profile.save()
            messages.success(request, 'บันทึกข้อมูลเรียบร้อยแล้ว')
            return redirect('profile')
        else:
            messages.error(request, 'กรุณากรอกข้อมูลที่ถูกต้อง')
    else:
        form = UserProfileForm(instance=user_profile)
    return render(request, 'app/edit_profile.html', {'form': form})

def upload_profile_image(request):
    if request.method == 'POST':
        profile_image = request.FILES.get('profile_image')
        if profile_image:
            request.user.userprofile.profile_image = profile_image
            request.user.userprofile.save()
            messages.success(request, 'อัพโหลดโปรไฟล์เรียบร้อยแล้ว')
        else:
            messages.error(request, 'กรุณาเลือกรูปภาพ')
    return redirect('profile')

@login_required
def profile(request):
    return render(request, 'app/profile.html', {'user': request.user})


def Me(request):
    return render(request, 'app/me.html', {'user': request.user})

def home(req):
    food = Food.objects.all()
    context ={
        'food':food,
    }
    return render(req,'app/home.html',context)

def registerXlogin(req):
    return render(req,'app/login.html')


def signout(request):
    logout(request)
    return redirect('home')

def register(req):
    if req.method == "POST":
        username = req.POST['username']
        fname = req.POST['fname']
        lname = req.POST['lname']
        email = req.POST['email']
        pass1 = req.POST['pass1']

        if User.objects.filter(username=username).exists():
            messages.error(req, "Username is already taken. Please choose a different username.")
            return render(req, "app/register.html")

        try:
            myuser = User.objects.create_user(username, email, pass1)
            myuser.first_name = fname
            myuser.last_name = lname
            myuser.save()

            UserProfile.objects.create(user=myuser, first_name=fname, last_name=lname, email=email, pass1=pass1)
            messages.success(req, "สร้างบัญชีเรียบร้อย ")
            return redirect('login')

        except IntegrityError:
            messages.error(req, "An error occurred while creating the user. Please try again.")
            return render(req, "app/register.html")

    return render(req, "app/register.html")


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('pass1')
        user = authenticate(username=username, password=password)

        if user is not None:
            auth_login(request, user)
            messages.success(request, "เข้าสู่ระบบสำเร็จ")

            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'message': 'เข้าสู่ระบบสำเร็จ'})
            else:
                return redirect('home')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'message': 'ข้อมูลเข้าสู่ระบบไม่ถูกต้อง'})
            else:
                messages.error(request, "ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง")
                return redirect('login')

    return render(request, 'app/login.html')

def payment(req):
    return render(req,'app/payment.html')



@login_required
def cart(req):
    try:
        user_profile = UserProfile.objects.get(user=req.user)
        cart, created = Cart.objects.get_or_create(cart=user_profile)
        
        cart_detail = Food.objects.filter(carts=cart)
        count = sum(detail.amount for detail in cart_detail)
        
        context = {'count': count, 'cart': cart_detail}
        return render(req, 'productweb/cart.html', context)
    except UserProfile.DoesNotExist:
        pass

def contag(req):
    return render(req,'productweb/contag.html')

@login_required
def order(request):
    if request.method == 'POST':
        user_profile = request.user.userprofile  
        name = request.POST.get('name')
        category = request.POST.get('category')
        material = request.POST.get('material')
        message = request.POST.get('message')
        attachment = request.FILES.get('attachment')
        order = Food.objects.create(
            user_profile=user_profile,
            name=name,
            category=category,
            material=material,
            message=message,
            attachment=attachment
        )
        try:
            with transaction.atomic():
                cart = Cart.objects.select_for_update().get(cart=user_profile)
                cart_items = Detailcart.objects.filter(carts=cart)
                cart_items.delete()
                messages.success(request, 'Your order has been placed successfully!')
        except Cart.DoesNotExist:
            pass
        return redirect('preorder') 

    return render(request, 'productweb/order.html')


def user_management_view(request):
    user_profiles = UserProfile.objects.all()
    return render(request, 'admin/management.html', {'user_profiles': user_profiles})

@login_required


def order2(request):
    return render(request, 'productweb/order2.html')
def order3(request):
    return render(request, 'productweb/order3.html')
def order4(request):
    return render(request, 'productweb/order4.html')
def order5(request):
    return render(request, 'productweb/order5.html')
def order6(request):
    return render(request, 'productweb/order6.html')

@login_required
def preorder(request, order_id=None):
    if order_id:
        # If order_id is provided, redirect to track_order view
        return redirect('track_order', order_id=order_id)
    else:
        # Fetch all orders for the current user
        current_user = request.user
        orders = Order.objects.filter(user_profile__user=current_user).order_by('-created_at')
        return render(request, 'productweb/preorder.html', {'orders': orders})

def delete_product(request, product_id):
    cart_item = get_object_or_404(Detailcart, id=product_id)
    if request.method == 'POST':
        cart_item.delete()
        return redirect('cart') 
    return render(request, 'productweb/delete_product.html', {'product': cart_item})

def products(request):
    all_products = Food.objects.all()
    context = {'products': all_products}
    return render(request, 'productweb/product.html', context)


def product(request, item_id):
    item_instance = get_object_or_404(Food, id=item_id)
    return render(request, 'productweb/product_detail.html', {'item': item_instance})

def add_product(request):
    if request.method == 'POST':
        item_form = FoodForm(request.POST)
        image_form = FoodForm(request.POST, request.FILES)

        if item_form.is_valid() and image_form.is_valid():
            item = item_form.save()
            image = image_form.save(commit=False)
            image.item = item
            image.save()

            return redirect('products') 
    else:
        item_form = FoodForm()
        image_form = FoodForm()

    return render(request, 'productweb/add_product.html', {'item_form': item_form, 'image_form': image_form})


def add_cart(req, id):
    products = Food.objects.filter(item=id)
    
    try:
        user_profile = UserProfile.objects.get(user=req.user)
        cart, created = Cart.objects.get_or_create(cart=user_profile)
        product_instance = products.first()
        
        cart_detail = Detailcart.objects.create(
            itemImages=product_instance,
            carts=cart,
            amount=1,
        )
        cart_detail.save()
        return HttpResponseRedirect(reverse('cart'))
    except UserProfile.DoesNotExist:
        pass