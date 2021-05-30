from rest_framework.response import Response
from rest_framework.decorators import api_view

from .serializers import OrderSerializer
from Product.models import Product

@api_view(['POST', ])
def orderView(request, productKey):
    orderedProduct = Product.objects.filter(id=productKey)[0]
    sellerOfProduct = orderedProduct.seller
    serializer = OrderSerializer(data=request.data, context={'request': request, 'orderedProduct': orderedProduct, 'sellerOfProduct': sellerOfProduct})
    data = {}
    
    if serializer.is_valid():
        order = serializer.save()
        data['response'] = "Order Successful"
    else:
        data = serializer.errors
    
    return Response(data)