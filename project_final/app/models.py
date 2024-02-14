from datetime import date, datetime
from django.db import models
from PIL import Image
from django.contrib.auth.models import User
from django.utils import timezone


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='images_profile', null=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    pass1 = models.CharField(max_length=100, null=True, blank=True)
    
    def __str__(self):
        return self.user.username
# Create your models here.
#class Member(models.Model):
class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email =models.EmailField(blank=True,null=True)
    phone_number = models.CharField(max_length=100)
    pass1 = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(max_length=20, choices=(
        ('Male', 'ผู้ชาย'),
        ('Female', 'ผู้หญิง'),
        ('Other', 'อื่นๆ'),

    ), default='11-20') 
    def __str__(self) -> str:
        return f'{self.user_name} '


class Food(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField(default=0)
    unit = models.CharField(max_length=100,default='บาทต่อถุง')
    score = models.FloatField(default=0,blank=True,null=True)
    quantity_review = models.IntegerField(default=0,blank=True,null=True)
    image = models.ImageField(upload_to='media/image/',blank=True,null=True)
    options = models.CharField(max_length=20, choices=(
        ('notchoose', 'ไม่ได้เลือก'),
        ('onsale', 'วางขาย'),
        ('soldout', 'ขายหมดแล้ว'),
    ), default='notchoose') 


    def __str__(self) -> str:
        return f'เมนู {self.name} ราคา {self.price} บาท status : {self.options}'
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            img = Image.open(self.image.path)
            if img.height >300 or img.width >300:
                output_size = (300,300)
                img.thumbnail(output_size)
                img.save(self.image.path)
            
        
    
class Historysale(models.Model):
    date_field = models.DateField()
    food = models.ForeignKey(Food,on_delete=models.DO_NOTHING,null=True,blank=True)

    def __str__(self) -> str:
        return f'{self.date_field} {self.food}'
    
class Reviewfood(models.Model):
    food = models.ForeignKey(Food,on_delete=models.CASCADE)
    owner = models.ForeignKey(Member,on_delete=models.CASCADE,null=True)
    review = models.TextField(max_length=500,blank=True,null=True)
    created = models.DateTimeField(default=timezone.now)
    rating = models.IntegerField(choices=(
        (1, '1 ดาว'),
        (2, '2 ดาว'),
        (3, '3 ดาว'),
        (4, '4 ดาว'),
        (5, '5 ดาว'),

    ), default=5) 

    def __str__(self) -> str:
        return f'{self.food.name} rating : {self.rating}'
    

class Cart(models.Model):
    cart = models.ForeignKey(UserProfile, on_delete=models.CASCADE)


class Detailcart(models.Model):
    itemImages = models.ImageField(upload_to='media/image/',blank=True,null=True)
    carts = models.ForeignKey(Cart, on_delete=models.CASCADE)
    amount = models.IntegerField()

class Order(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=2, choices=[('A0', 'A0'), ('A1', 'A1'), ('A2', 'A2'), ('A3', 'A3'), ('A4', 'A4')])
    material = models.CharField(max_length=50, choices=[('Vinyl', 'ป้ายไวนิลธงญี่ปุ่น'), ('Acrylic', 'ป้ายไวนิลโครงไม้/โครงเหล็ก'), ('Metal', 'ป้ายกล่องไฟไวนิล'), ('Wood', 'สติกเกอร์อิงค์เจ็ท'), ('Foamboard', 'แคนวาสอิงค์เจ็ท')])
    message = models.TextField()
    attachment = models.FileField(upload_to='order_attachments', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=[('รอดำเนินการ', 'รอดำเนินการ'), ('กำลังดำเนินการ', 'กำลังดำเนินการ'), ('จัดส่งแล้ว', 'จัดส่งแล้ว'), ('จัดส่งเรียบร้อย', 'จัดส่งเรียบร้อย')])


    def __str__(self):
        return f"Order {self.id}: {self.name} ({self.get_status_display()})"
