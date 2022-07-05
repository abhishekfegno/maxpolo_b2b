from rest_framework import serializers

from apps.catalogue.models import Product, PDF, Category


class ProductSerializer(serializers.ModelSerializer):
    brand = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()

    def get_category(self, instance):
        return instance.category.name

    def get_brand(self, instance):
        return instance.brand.name

    class Meta:
        model = Product
        fields = ('id', 'name', 'product_code', 'brand', 'category')


class ProductPDFSerializer(serializers.ModelSerializer):
    class Meta:
        model = PDF
        fields = ('id', "title", "image", 'file')


class CategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    def get_children(self, instance):
        if instance.pdf.all().exists:
            return ProductPDFSerializer(instance.pdf.all(), many=True).data
        return self.__class__(
            instance.get_children(),
            many=True,
            context={'request': self.context['request']}
        ).data or None

    class Meta:
        model = Category
        fields = ('id', 'name', 'children')
