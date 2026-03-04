from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Product
from .serializers import ProductSerializer


class ProductList(APIView):
    """
    GET /api/products/
    Gibt 5 beliebige Produkte zurück.
    """
    def get(self, request): #Wenn der get request kommt zeigt er die 5 produkte an.
        products = Product.objects.order_by("?")[:5]
        return Response(ProductSerializer(products, many=True).data)


class ProductDetail(APIView):
    """
    GET /api/products/<id>/
    PUT/PATCH /api/products/<id>/
    DELETE /api/products/<id>/
    """
    def get_object(self, product_id: int) -> Product: #Erstmal wird das Produkt aufgerufen
        return Product.objects.get(pk=product_id)

    def get(self, request, product_id: int):
        try:
            product = self.get_object(product_id) # Wenn der get request kommt zeigt er das Produkt mit der id an.
        except Product.DoesNotExist:
            return Response({"detail": "Produkt nicht gefunden."}, status=status.HTTP_404_NOT_FOUND)
        return Response(ProductSerializer(product).data)

    def put(self, request, product_id: int): #Wenn der put request kommt, wird das Produkt mit der id aktualisiert. Alle Felder müssen übergeben werden.
        try:
            product = self.get_object(product_id)
        except Product.DoesNotExist:
            return Response({"detail": "Produkt nicht gefunden."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(product, data=request.data)  # full update
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def patch(self, request, product_id: int): #Wenn der patch request kommt, wird das Produkt mit der id aktualisiert. Es können auch nur einzelne Felder übergeben werden.
        try:
            product = self.get_object(product_id)
        except Product.DoesNotExist:
            return Response({"detail": "Produkt nicht gefunden."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(product, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, product_id: int): #Wenn der delete request kommt, wird das Produkt mit der id gelöscht.
        try:
            product = self.get_object(product_id)
        except Product.DoesNotExist:
            return Response({"detail": "Produkt nicht gefunden."}, status=status.HTTP_404_NOT_FOUND)

        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductCreate(APIView):
    """
    POST /api/products/create/
    Legt ein neues Produkt an.
    """
    def post(self, request): #Wenn der post request kommt, wird ein neues Produkt angelegt. Alle Felder müssen übergeben werden.
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = serializer.save()
        return Response(ProductSerializer(product).data, status=status.HTTP_201_CREATED)

