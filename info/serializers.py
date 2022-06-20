from rest_framework import serializers
from .models import AboutUs, News, Help, Offer, Contacts, Advantages, MainPageIcon, CallBack,\
    HelpIcon, HeaderFooterPic


class HeaderFooterPicSerializer(serializers.ModelSerializer):
    """serialilzer for callback"""

    class Meta:
        model = HeaderFooterPic
        fields = '__all__'


class CallBackSerializer(serializers.ModelSerializer):
    """serialilzer for callback"""

    class Meta:
        model = CallBack
        fields = ('name', 'phone_number',)


class ContactsSerializer(serializers.ModelSerializer):
    """serializer for footer"""

    class Meta:
        model = Contacts
        fields = '__all__'


class AdvantagesSerializer(serializers.ModelSerializer):
    """serialzier for company's advantages"""

    class Meta:
        model = Advantages
        fields = '__all__'


class MainPageIconSerializer(serializers.ModelSerializer):
    """serializer for main page slider"""

    class Meta:
        model = MainPageIcon
        fields = '__all__'


class AboutSerializer(serializers.ModelSerializer):
    """serializer for info about company"""

    class Meta:
        model = AboutUs
        fields = '__all__'


class NewsSerializer(serializers.ModelSerializer):
    """serializer for news"""
    class Meta:
        model = News
        fields = '__all__'


class OfferSerializer(serializers.ModelSerializer):
    """serializer for public offer"""

    class Meta:
        model = Offer
        fields = '__all__'


class HelpSerializer(serializers.ModelSerializer):
    """serializer for help"""
    icon = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Help
        fields = ['question', 'answer', 'icon']

    def get_icon(self, obj):
        try:
            request = self.context.get('context')
            icon_url = obj.icon
            return request.build_absolute_uri(icon_url)
        except ValueError:
            return None
