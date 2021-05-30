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

from Order.models import Order



tokenValue = {}

@api_view(['POST',])
def registration_view(request):
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            customer = serializer.save()
            data['response'] = "Registration Successful"
            data['first_name'] = customer.first_name
            data['last_name'] = customer.last_name
            data['email'] = customer.email
            data['phone'] = customer.phone
            data['city'] = customer.city
            token = Token.objects.get(user=customer).key
            data['token'] = token

            # Send Email Verification Link

            current_site = get_current_site(request)
            htmly = get_template(r'C:\Users\Jayash Satolia\OneDrive\Desktop\Ecomproject\Backend\Customer\templates\Users\ActivateAccount.html')

            ans = {
                    'user':customer,
                    'uid': urlsafe_base64_encode(force_bytes(customer.pk)),
                    'token': account_activation_token.make_token(customer)
                }

            tokenValue[str(ans['uid'])] =  str(ans['token'])

            html_content = htmly.render(ans)

            subject, from_email, to = 'Welcome!', 'jayashsatolia@gmail.com', customer.email

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
        customer = Customer.objects.get(pk=uid)

    except(TypeError, ValueError, OverflowError, Customer.DoesNotExist):
        customer = None

    if customer is not None and tokenValue[str(uidb64)] == str(token):
        customer.is_verified = True
        customer.save()
        return HttpResponse('Thanks for Confirmation! You can now login to your Account.')
    else:
        return HttpResponse('Activation link is invalid!')


@api_view(['GET', ])
def profile(request):
    customer = request.user.customer

    orders = Order.objects.filter(customer=customer)

    data = {}
    data['orders'] = [order for order in orders]