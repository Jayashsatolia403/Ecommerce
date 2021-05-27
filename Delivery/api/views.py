from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token

from .serializers import RegistrationSerializer

@api_view(['POST',])
def registration_view(request):
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        print(request.data)
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
        else:
            data = serializer.errors
        return Response(data)

