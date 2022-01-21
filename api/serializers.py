import datetime

from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.validators import UniqueValidator


from .models import *



__all__ = ['TokenObtainSerializer', 'RegisterSerializer', 'UserSerializer','ShopSerializer', 'BookingSerializer', 'WalletSerializer' ]

class TokenObtainSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(TokenObtainSerializer, cls).get_token(user)

        # Add custom claims
        token['username'] = user.username
        return token
    
    

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    role = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name', 'role')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }
        
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        
        obj = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )

        
        obj.set_password(validated_data['password'])
        api_user = APIUser.objects.create(user=obj, role='customer')
        obj.save()
        api_user.save()

        return obj

class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    role = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ('id','username', 'password', 'password2', 'email', 'first_name', 'last_name', 'role')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }
        
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        
        obj = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )

        
        obj.set_password(validated_data['password'])
        api_user = APIUser.objects.create(user=obj, role='shop')
        obj.save()
        api_user.save()

        return obj


class ShopSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Shop
        fields = "__all__"
        

class BookingSerializer(serializers.ModelSerializer):
    shop = serializers.PrimaryKeyRelatedField(queryset=Shop.objects.all(), many=True, required=False)
    class Meta:
        model = Booking
        fields = ['id','customer','shop','date_time']
        
    def create(self, validated_data):
        shops = self.context['request'].data['id']
        total_amount = 0.0
        obj = []
        if len(shops) > 0:
            for i in shops:
                try:
                    shop = Shop.objects.get(id=int(i))
                    obj.append(shop)
                    total_amount += shop.price
                except Exception as e:
                    raise serializers.ValidationError(str(e))
            try:
                user_w = Wallet.objects.get(user=self.context['request'].user.id)
            except:
                raise serializers.ValidationError("You Have not added money to your wallet, kindly First Add Money to Wallet")
            if float(total_amount) > float(user_w.balance):
                raise serializers.ValidationError("You Do Not Have Sufficient Account Balance")
            else:
                user_w.balance = float(user_w.balance) - float(total_amount)
                dic = {}
                dic[str(datetime.date.today())] = "You have spent {} INR on Shopping at {}. Your Account Balance is {}".format(float(total_amount),str(shops),float(user_w.balance))
                user_w.statement.append(dic)
                user_w.save()
    
            booking = Booking.objects.create(customer=self.context['request'].user, total_price=total_amount)
            booking.shop.set(obj)
            booking.save()
            
            return booking
        
        else:
            return "Nothing TO create"
                


class WalletSerializer(serializers.ModelSerializer):
    
    
    class Meta:
        model = Wallet
        fields = "__all__"
        
            
            