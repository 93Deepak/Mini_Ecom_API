
from django.db import models
from django.contrib.auth.models import User

__all__ = ['Shop','Booking','Wallet','APIUser']



class APIUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20)
    
    
class Shop(models.Model):
    Shop    = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.CharField(max_length=50)
    price   = models.FloatField(default=0.0)
    
    
    
class Booking(models.Model):
    customer    = models.ForeignKey(User, on_delete=models.CASCADE)
    shop        = models.ManyToManyField("api.shop")
    total_price = models.FloatField(default=0.0)
    date_time   = models.DateTimeField(auto_now_add=True)


class Wallet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    balance = models.FloatField(default=0.0)
    statement = models.JSONField(default=[], blank=True)
    
    def get_user_display(self):
        return self.user.name