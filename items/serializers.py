from colorfield.serializers import ColorField
from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import CurrentUserDefault

from .models import Collection, Item, ItemImageColor, ItemCart, Order, OrderItem, UserFavouriteItems


class CollectionGetSerializer(serializers.ModelSerializer):
    """serializer for get collection"""
    image_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Collection
        fields = (
            'id',
            'name',
            'image_url',
        )

    def get_image_url(self, obj):
        try:
            request = self.context.get('context')
            image_url = obj.image.path
            print(self.context.get('context'))
            return request.build_absolute_uri(image_url)
        except AttributeError:
            return None
        except ValueError:
            return None


class CollectionCreateSerializer(serializers.ModelSerializer):
    """serializer for create collection"""
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
    """serializer for item image and item color with full url image"""
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
        except AttributeError:
            return None
        except ValueError:
            return None


class ItemsListSerializer(serializers.ModelSerializer):
    """serializer for list item"""
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
    """serializer for detail item"""
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
            'is_in_favourite',
        )


class BasketCreateSerializer(serializers.ModelSerializer):
    """serializer for create new basket"""

    class Meta:
        model = ItemCart
        fields = (
            'id',
            'item',
            'amount',
            'image',
        )

        read_only_fields = ('id', )


class BasketSerializer(serializers.ModelSerializer):
    """serializer for add amount item in basket"""

    class Meta:
        model = ItemCart
        fields = (
            'id',
            'item',
            'amount',
            'image',

        )

        read_only_fields = ('id', 'amount',)

    def get_image_url(self, obj):
        try:
            request = self.context.get('context')
            image_url = obj.image.path
            print(self.context.get('context'))
            return request.build_absolute_uri(image_url)
        except AttributeError:
            return None
        except ValueError:
            return None

    def create(self, validated_data):
        return ItemCart.objects.create(**validated_data)


class ItemBasketSerializer(serializers.ModelSerializer):
    """item serializer for get in ordered list"""
    class Meta:
        model = Item
        fields = ('title', 'size_range', 'price', 'basic_price')


class BasketListSerializer(serializers.ModelSerializer):
    """serializer for list items in basket"""
    item = ItemBasketSerializer()
    image = ImageItemSerializer()

    class Meta:
        model = ItemCart
        fields = (
            'id',
            'item',
            'image',
            'amount',

        )

        read_only_fields = ('id', 'amount')


class OrderSerializer(serializers.ModelSerializer):
    """serializer for create order"""
    class Meta:
        model = Order
        exclude = ('order_status',)
        read_only_fields = (''
                            'id',
                            'item_quantity',
                            'line_quantity',
                            'price_before_discount',
                            'price_after_discount',
                            'sum_of_discount'
                            )

    def create(self, validated_data):
        return Order.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.lastname = validated_data.get('lastname', instance.lastname)
        instance.email = validated_data.get('email', instance.email)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.created_at = validated_data.get('created_at', instance.created_at)
        instance.country = validated_data.get('country', instance.country)
        instance.city = validated_data.get('city', instance.city)
        instance.agreement = validated_data.get('agreement', instance.agreement)

    def validate(self, attrs):
        if attrs['agreement'] == False:
            raise ValidationError('необходимо согласие с публичной офертой, нажмите на галочку')
        return attrs


class OrderListSerializer(serializers.ModelSerializer):
    """serializer for list order"""
    class Meta:
        model = Order
        fields = ('id', 'name', 'lastname', 'phone_number', 'country', 'city', 'order_status')


class ItemForOrderSerializer(serializers.ModelSerializer):
    """item serializer for order item"""

    class Meta:
        model = Item
        fields = ('title', 'size_range', 'price', 'basic_price')


class ImageOrderSerializer(serializers.ModelSerializer):
    """image color serializer for order item"""

    image = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ItemImageColor
        fields = ('image', 'custom_color')

    def get_image(self, obj):
        try:
            request = self.context.get('context')
            image_url = obj.image.path
            print(self.context.get('context'))
            return request.build_absolute_uri(image_url)
        except AttributeError:
            return None
        except ValueError:
            return None


class OrderItemSerializer(serializers.ModelSerializer):
    """order item serializer for order"""
    item = ItemForOrderSerializer()
    image = ImageOrderSerializer()

    class Meta:
        model = OrderItem
        fields = ('item', 'image')


class OrderDetailSerializer(serializers.ModelSerializer):
    """order serializer for get detail order"""
    orderitem = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        exclude = ('agreement', )


class UserFavouriteItemSerializer(serializers.ModelSerializer):
    item = ItemsListSerializer()

    class Meta:
        model = UserFavouriteItems
        fields = ('id', 'item', 'user')


class UserFavouriteCreateSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = UserFavouriteItems
        fields = ('id', 'item', 'user')

    def get_user(self, obj):
        user = self.context['context'].user.id
        return user

    @transaction.atomic
    def create(self, validated_data):
        request = self.context.get('context', None)
        if request:
            user = request.user
        else:
            raise serializers.ValidationError({'user': ('Пользователь не авторизовался')})

        validated_data['user'] = user
        print(validated_data)
        favourite = UserFavouriteItems.objects.create(
            **validated_data
        )
        return favourite

