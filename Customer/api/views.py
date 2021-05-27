from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token

from .serializers import RegistrationSerializer

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
        else:
            data = serializer.errors
        return Response(data)