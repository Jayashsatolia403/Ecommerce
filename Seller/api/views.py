from Order.models import Order
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token

from .serializers import RegistrationSerializer, AddProductSerializer

from rest_framework.generics import ListAPIView

from Seller.models import Seller

@api_view(['POST',])
def registration_view(request):
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            seller = serializer.save()
            data['response'] = "Registration Successful"
            data['first_name'] = seller.first_name
            data['last_name'] = seller.last_name
            data['email'] = seller.email
            data['phone'] = seller.phone
            token = Token.objects.get(user=seller).key
            data['token'] = token
        else:
            data = serializer.errors
        return Response(data)

@api_view(['POST',])
def addProductView(request):
    if request.method == 'POST':
        serializer = AddProductSerializer(data=request.data, context={'request': request})
        data = {}
        if serializer.is_valid():
            product = serializer.save()
            data['response'] = "Product Added"
            data['title'] = product.title
            data['seller'] = product.seller
        else:
            data = serializer.errors

        return Response(data)


@api_view(['GET',])
def sellerAdmin(request):
    adminSeller = request.user.seller
    orders = Order.objects.filter(seller = adminSeller)

    data = {}
    print(orders)
    data['orders'] = orders

    return Response(data)





"""
def seller_admin(request):
    if request.user.is_seller:
        seller = request.user.seller
        if request.user.is_verified == True:
            products = seller.products.all()
            orders = seller.orders.all()

            for order in orders:
                order.seller_amount = 0
                order.seller_paid_amount = 0
                order.fully_paid = True

                for item in order.items.all():
                    if item.seller == request.user.seller:
                        if item.seller_paid:
                            order.seller_paid_amount += item.get_total_price()
                        else:
                            order.seller_amount += item.get_total_price()
                            order.fully_paid = False
            
            return render(request, 'seller/seller_admin.html', {'seller':seller, 'products':products, 'orders':orders})
        else:
            return render(request, 'seller/seller_admin_fail.html')
    else:
        return redirect('login_failed')

"""