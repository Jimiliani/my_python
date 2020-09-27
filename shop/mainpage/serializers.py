from rest_framework import serializers
from .models import Item, Accessory, Shoe, Underwear, Outwear


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'


class OutwearSerializer(serializers.ModelSerializer):
    class Meta:
        model = Outwear
        fields = '__all__'


class UnderwearSerializer(serializers.ModelSerializer):
    class Meta:
        model = Underwear
        fields = '__all__'


class ShoesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shoe
        fields = '__all__'


class AccessoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accessory
        fields = '__all__'


class OutwearMiniSerializer(serializers.ModelSerializer):
    count = serializers.SerializerMethodField('get_count')

    def get_count(self, obj):
        required_size = self.context['size']
        return obj.get_count_in_stock(required_size)

    class Meta:
        model = Outwear
        fields = ('name', 'price', 'image', 'count')


class UnderwearMiniSerializer(serializers.ModelSerializer):
    count = serializers.SerializerMethodField('get_count')

    def get_count(self, obj):
        required_size = self.context['size']
        return obj.get_count_in_stock(required_size)

    class Meta:
        model = Underwear
        fields = ('name', 'price', 'image', 'count')


class ShoesMiniSerializer(serializers.ModelSerializer):
    count = serializers.SerializerMethodField('get_count')

    def get_count(self, obj):
        required_size = self.context['size']
        return obj.get_count_in_stock(required_size)

    class Meta:
        model = Shoe
        fields = ('name', 'price', 'image', 'count')


class AccessoriesMiniSerializer(serializers.ModelSerializer):
    count = serializers.SerializerMethodField('get_count')

    def get_count(self, obj):
        required_size = self.context['size']
        return obj.get_count_in_stock(required_size)

    class Meta:
        model = Accessory
        fields = ('name', 'price', 'image', 'count')
