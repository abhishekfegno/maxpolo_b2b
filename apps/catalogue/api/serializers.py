from rest_framework import serializers

from apps.catalogue.models import Product, PDF, Category


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductPDFSerializer(serializers.ModelSerializer):
    class Meta:
        model = PDF
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    def get_children(self, instance):
        return self.__class__(
            instance.get_children(),
            many=True,
            context={'request': self.context['request']}
        ).data or None

    class Meta:
        model = Category
        fields = ('name', 'children')
