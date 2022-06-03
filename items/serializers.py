from rest_framework import serializers
from rest_framework.exceptions import ValidationError


from .models import Collection, Item, ItemImageColor, ItemCart, Order, SearchHelper


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
    '''serializer for item image and item color with full url image'''
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


class ItemCreateSerializer(serializers.ModelSerializer):
    """serializer for create item"""
    itemimage = ImageItemSerializer(many=True, read_only=True)

    class Meta:
        model = Item
        fields = ('id', 'title', 'item_id',
                  'basic_price', 'price', 'discount',
                  'description', 'size_range',
                  'amount_in',
                  'compound', 'material', 'is_in_cart', 'itemimage', 'collection', 'is_in_favourite'
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
            'is_in_favourite',
        )
        read_only_fields = ('id',)


class ItemsFavouriteSerializer(serializers.ModelSerializer):
    """serializer for select one item to favourite"""
    class Meta:
        model = Item
        exclude = ('date', 'is_novelty', 'is_in_cart', 'is_bestseller')
        read_only_fields = (
            'id',
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
            'discount',
        )


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
            'order',
        )

        read_only_fields = ('id',)


class BasketSerializer(serializers.ModelSerializer):
    """serializer for add amount item in basket"""

    class Meta:
        model = ItemCart
        fields = (
            'id',
            'item',
            'amount',
            'order',

        )

        read_only_fields = ('id', 'amount',)


class BasketListSerializer(serializers.ModelSerializer):
    """serializer for list items in basket"""
    item = ItemsListSerializer()

    class Meta:
        model = ItemCart
        fields = (
            'id',
            'item',
            'amount',
            'order',
        )

        read_only_fields = ('id', 'amount', 'order',)


class OrderSerializer(serializers.ModelSerializer):
    """serializer for create order"""
    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        return Order.objects.create(**validated_data)

    def validate(self, attrs):
        if attrs['agreement'] == False:
            raise ValidationError('нужно согласие с публичной офертой')
        return attrs


class SearchHelperSerializer(serializers.ModelSerializer):

    class Meta:
        model = SearchHelper
        fields = '__all__'
