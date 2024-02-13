from datetime import date, datetime
from django.db import models
from PIL import Image
from django.contrib.auth.models import User
from django.utils import timezone



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
    

