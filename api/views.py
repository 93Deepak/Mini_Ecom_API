from django.contrib.auth.models import User

from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, views, mixins
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import *
from .models import *
import datetime
import json

__all__ =['MyObtainTokenPairView', 'RegisterView', 'ShopView', 'BookingView', 'WalletView', 'AdminView']

def user(request):
    try:
        obj= APIUser.objects.get(user=request.user)
    except:
        obj = None
    if obj:
        if obj.role == 'customer':
            return 'customer'
        if obj.role == 'shop':
            return 'shop'
        else:
            return 'admin'
    else:
        return None
        
class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = TokenObtainSerializer
    
    
    
class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    


class AdminView(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAdminUser]
         
    def create(self,request):
        data = request.data
        serializer = UserSerializer(data=data, context={'request':request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ShopView(ModelViewSet):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    # def get_permissions(self):
        
    #     if self.action == 'create':
    #         permission_classes = [IsAdminUser]
    #     else:
    #         permission_classes = [IsAuthenticated]
            
    #     return [permission() for permission in permission_classes]
    
    def list(self, request):
        if user(request) is None:
            return Response({"Error":"Make sure You are Not Making Any Mistake"})
        if user(request) == 'shop':
            try:
                obj = Shop.objects.filter(Shop=request.user)
                serializer = ShopSerializer(obj, many=True)
                
                return Response(serializer.data)
            
            except:
                return Response({"Empty":"You Have Not Created any services. Create One First to view"})
        if user(request) == 'customer':
            obj = Shop.objects.all()
            serializer = ShopSerializer(obj, many=True)
            
            return Response(serializer.data)
        else:
            return Response({"Not Allowed - GET":"You Do Not Have Permissions to Perform this task"})
            
    def create(self, request):
        if user(request) == 'shop':
            data = request.data
            data._mutable = True
            data['Shop'] = request.user.id
            serializer = ShopSerializer(data=data, context={'request':request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        else:
            return Response({'Not Allowed - POST':"You Do Not Have Permissions to Perform this task"})
        
    
    
class BookingView(ModelViewSet):
    serializer_class = BookingSerializer
    # authentication_classes = [TokenAuthentication]
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        if user(self.request) == 'customer':
            try:
                queryset = Booking.objects.get(customer = self.request.user.id)
            except:
                queryset = None
        elif user(self.request) == 'shop':
            try:
                queryset = Booking.objects.get(shop = self.request.user.id)
            except:
                queryset = None
        else:
            
            queryset = None
        
        return queryset
    
    def create(self,request):
        if user(request) == 'customer':
            data = request.data
            data['customer'] = request.user.id
            
            serializer = BookingSerializer(data=data, context={'request':request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        
        else:
            
            return Response({'Error':"You Do Not Have Permission TO perform This Action"})
        
            
    
    
class WalletView(ModelViewSet):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    # authentication_classes = [TokenAuthentication]
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    
    def list(self,request):
        try:
            queryset = Wallet.objects.get(user=request.user.id)
        except:
            queryset = None
            
        if queryset:
            serializer = WalletSerializer(queryset)
            
            return Response(serializer.data)
        else:
            return Response({'Error':'You Have Not Added any amount to wallet yet, please add once so you can see it'})
        
    
    def create(self, request):
        if user(request) == 'customer':
            data = self.request.data
            data._mutable = True
            data['user'] = request.user.id
            
            try:
                obj = Wallet.objects.get(user=data['user'])
            except:
                obj = None
                
            if obj:
                obj.balance = obj.balance + float(data['amount'])
                dic = {}
                dic[str(datetime.date.today())] = "Credited {} INR for {} . Your Account Balance is {} INR ".format(float(data['amount']),data['reason'], float(obj.balance))
                obj.statement.append(dic)
                obj.save()
                serializer = WalletSerializer(obj)
                return Response(serializer.data)
            else:
                data['balance'] = data['amount']
                dic = {}
                dic[str(datetime.date.today())] = "Credited {} INR for {} . Your account Balance is {} INR".format(float(data['amount']), data['reason'], float(data['amount']))
                data['statement'] = json.dumps(dic)
                serializer = WalletSerializer(data=data, context={'request':request})
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.data)
        else:
            return Response({"Error":"You Are Not Allowed to Perform this Action."})