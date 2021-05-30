from Order.models import Order
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token

from django.http.response import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token

from .serializers import RegistrationSerializer
from Seller.models import Seller

from django.core.mail import EmailMultiAlternatives
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import account_activation_token
from django.utils.encoding import force_bytes, force_text
from django.template.loader import get_template
from django.contrib.sites.shortcuts import get_current_site


from .serializers import RegistrationSerializer, AddProductSerializer


tokenValue = {}

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
            # Send Email Verification Link

            current_site = get_current_site(request)
            htmly = get_template(r'C:\Users\Jayash Satolia\OneDrive\Desktop\Ecomproject\Backend\Seller\templates\Users\ActivateAccount.html')

            ans = {
                    'user':seller,
                    'uid': urlsafe_base64_encode(force_bytes(seller.pk)),
                    'token': account_activation_token.make_token(seller)
                }

            tokenValue[str(ans['uid'])] =  str(ans['token'])

            html_content = htmly.render(ans)

            subject, from_email, to = 'Welcome!', 'jayashsatolia@gmail.com', seller.email

            msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
        else:
            data = serializer.errors
        return Response(data)



def activate(request, uidb64, token):
    print(tokenValue)
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        seller = Seller.objects.get(pk=uid)

    except(TypeError, ValueError, OverflowError, Seller.DoesNotExist):
        seller = None

    if seller is not None and tokenValue[str(uidb64)] == str(token):
        seller.is_verified = True
        seller.save()
        return HttpResponse('Thanks for Confirmation! You can now login to your Account.')
    else:
        return HttpResponse('Activation link is invalid!')

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
    data['orderId'] = [order.id for order in orders]
    data['address'] = [order.address for order in orders]
    data['phone'] = [order.phone for order in orders]
    data['zipcode'] = [order.zipcode for order in orders]
    data['longitude'] = [order.longitude for order in orders]
    data['latitude'] = [order.latitude for order in orders]
    data['date'] = [order.created_at for order in orders]

    return Response(data)