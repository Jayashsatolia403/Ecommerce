from Delivery.models import Delivery
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token

from .serializers import RegistrationSerializer
from Order.models import Order
from Customer.models import Customer

from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import account_activation_token, delivery_token
from django.shortcuts import render, redirect


from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token

from django.http.response import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token

from .serializers import RegistrationSerializer
from Customer.models import Customer

from django.core.mail import EmailMultiAlternatives
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import account_activation_token
from django.utils.encoding import force_bytes, force_text
from django.template.loader import get_template
from django.contrib.sites.shortcuts import get_current_site



tokenValue = {}
delivery_token_value = {}


@api_view(['POST',])
def registration_view(request):
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            delivery = serializer.save()
            data['response'] = "Registration Successful"
            data['first_name'] = delivery.first_name
            data['last_name'] = delivery.last_name
            data['email'] = delivery.email
            data['phone'] = delivery.phone
            token = Token.objects.get(user=delivery).key
            data['token'] = token
        
            # Send Email Verification Link

            current_site = get_current_site(request)
            htmly = get_template(r'C:\Users\Jayash Satolia\OneDrive\Desktop\Ecomproject\Backend\Delivery\templates\Users\ActivateAccount.html')

            print(" >>> ", delivery.pk)
            ans = {
                    'user':delivery,
                    'uid': urlsafe_base64_encode(force_bytes(delivery.pk)),
                    'token': account_activation_token.make_token(delivery)
                }

            tokenValue[str(ans['uid'])] =  str(ans['token'])

            html_content = htmly.render(ans)

            subject, from_email, to = 'Welcome!', 'jayashsatolia@gmail.com', delivery.email

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
        delivery = Delivery.objects.get(pk=uid)

    except(TypeError, ValueError, OverflowError, Delivery.DoesNotExist):
        delivery = None

    if delivery is not None and tokenValue[str(uidb64)] == str(token):
        delivery.is_verified = True
        delivery.save()
        return HttpResponse('Thanks for Confirmation! You can now login to your Account.')
    else:
        return HttpResponse('Activation link is invalid!')

@api_view(['GET',])
def deliveryAdmin(request):
    adminDelivery = request.user.delivery
    orders = Order.objects.filter(delivery = adminDelivery)

    data = {}
    data['orderId'] = [order.id for order in orders]
    data['address'] = [order.address for order in orders]
    data['phone'] = [order.phone for order in orders]
    data['zipcode'] = [order.zipcode for order in orders]
    data['longitude'] = [order.longitude for order in orders]
    data['latitude'] = [order.latitude for order in orders]
    data['date'] = [order.created_at for order in orders]
    data['seller'] = [order.seller.email for order in orders]

    return Response(data)

@api_view(['GET', ])
def confirmDelivery(request, orderID):
    global delivery_token_value
    delivery = request.user.delivery
    order = Order.objects.filter(delivery = delivery, id = orderID)[0]


    if not order:
        return Response("You are not authorised!")
    
    print(order.customer)
    
    customer = order.customer
    email = customer.email
    current_order_id = str(orderID)

    delivery_ans = {
            'customer':customer,
            'delivery_uid': urlsafe_base64_encode(force_bytes(customer.pk)),
            'delivery_token': delivery_token.make_token(customer),
            'order_id': current_order_id
        }

    htmly = get_template(r'C:\Users\Jayash Satolia\OneDrive\Desktop\Ecomproject\Backend\Delivery\templates\Users\verifyDelivery.html')

    delivery_token_value[str(delivery_ans['delivery_uid']) + str(delivery_ans['order_id'])] = str(delivery_ans['delivery_token'])

    print(delivery_token_value)

    html_content = htmly.render(delivery_ans)

    subject, from_email, to = 'Welcome!', 'jayashsatolia403@gmail.com', email

    msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

    return HttpResponse("Yo")


def verifyConfirmDelivery(request, delivery_uidb64, delivery_token, current_order_id):
    global delivery_token_value
    if str(delivery_uidb64) + str(current_order_id) in delivery_token_value:
        if delivery_token_value[str(delivery_uidb64) + str(current_order_id)] == str(delivery_token):
            order = Order.objects.filter(id=current_order_id)[0]
            order.is_delivered = True
            order.save()
            return HttpResponse('Thanks For Verification. Take your Order!')
        else:
            return HttpResponse('Activation link is invalid!')
    else:
        return HttpResponse('Invalid')