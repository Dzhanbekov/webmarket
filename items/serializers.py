from django.contrib.auth import get_user_model
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault

from .models import Collection, Item, ItemImageColor, ItemCart, Order


class CollectionGetSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Collection
        fields = (
            'id',
            'name',
            'image_url',
        )

    def get_image_url(self, category):
        request = self.context.get('context')
        image_url = category.image.path
        print(self.context.get('context'))
        return request.build_absolute_uri(image_url)


class CollectionCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Collection
        fields = ('id', 'name', 'image')

    def create(self, validated_data):
        return Collection.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.image = validated_data.get('image', instance.image)
        instance.save()
        return instance


class ImageItemSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ItemImageColor
        fields = ('id', 'image_url', 'custom_color')

    def get_image_url(self, obj):
        try:
            request = self.context.get('context')
            image_url = obj.image.path
            print(self.context.get('context'))
            return request.build_absolute_uri(image_url)
        except ValueError:
            return None


# class ItemColorSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = ItemColor
#         fields = '__all__'


class ItemCreateSerializer(serializers.ModelSerializer):
    itemimage = ImageItemSerializer(many=True, read_only=True)

    class Meta:
        model = Item
        fields = ('id', 'title', 'item_id',
                  'basic_price', 'price', 'discount',
                  'description', 'size_range',
                  'amount_in',
                  'compound', 'material', 'is_in_cart', 'itemimage', 'collection'
                  )

    def create(self, validated_data):
        return Item.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.item_id = validated_data.get('item_id', instance.item_id)
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.price = validated_data.get('basic_price', instance.old_price)
        instance.new_price = validated_data.get('price', instance.new_price)
        instance.collection = validated_data.get('collection', instance.collection)
        instance.material = validated_data.get('material', instance.material)
        instance.compound = validated_data.get('compound', instance.compound)
        instance.size_range = validated_data.get('size_range', instance.size_range)
        instance.amount_in = validated_data.get('amount_in', instance.amount_in)
        instance.save()
        return instance


class ItemsListSerializer(serializers.ModelSerializer):
    itemimage = ImageItemSerializer(many=True, read_only=True)
    collection = CollectionGetSerializer()

    class Meta:
        model = Item
        fields = (
            'id',
            'title',
            'basic_price',
            'price',
            'discount',
            'itemimage',
            'collection',
            'size_range',
        )
        read_only_fields = ('id',)


class ItemsDetailSerializer(serializers.ModelSerializer):
    itemimage = ImageItemSerializer(many=True, read_only=True)
    collection = CollectionGetSerializer()

    class Meta:
        model = Item
        fields = (
            'title',
            'item_id',
            'price',
            'basic_price',
            'description',
            'size_range',
            'material',
            'compound',
            'amount_in',
            'itemimage',
            'collection',
        )


class BasketSerializer(serializers.ModelSerializer):

    class Meta:
        model = ItemCart
        fields = (
            'id',
            'item',
            'amount',
            'order',
        )

        read_only_fields = ('id',)
