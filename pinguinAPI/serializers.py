from rest_framework import serializers
from .models import Product, Stock


class ProductSerializer(serializers.ModelSerializer):
    stock = serializers.SerializerMethodField()

    stock_in = serializers.IntegerField(write_only=True, required=False, min_value=0)
 

    class Meta:
        model = Product
        fields = [
            "product_id",
              "product_name",
                "short_description",
                  "product_description",
                    "stock",
                      "price",
                        "product_image",
                        "stock_in",
                          "stock"  # nur für Input, nicht in der Ausgabe
                        ]
    def get_stock(self, obj):
        return obj.stock.amount if obj.stock else None   

    def create(self, validated_data):
        """
        Create: stock kommt als int rein, wir erstellen Stock-Objekt und verknüpfen es.
        """
        stock_value = validated_data.pop("stock_in", 0)
        stock_obj = Stock.objects.create(amount=stock_value)
        return Product.objects.create(stock=stock_obj, **validated_data)

    def update(self, instance, validated_data):
        """
        Update: erlaubt PUT/PATCH über denselben Serializer.
        """
        stock_value = validated_data.pop("stock_in", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if stock_value is not None:
            if instance.stock is None:
                instance.stock = Stock.objects.create(amount=stock_value)
            else:
                instance.stock.amount = stock_value
            instance.stock.save()

        instance.save()
        return instance