from rest_framework import serializers
from .models import AboutUs, News, Help, Offer, Contacts, Advantages, MainPageIcon, CallBack, HelpIcon


class CallBackSerializer(serializers.ModelSerializer):

    class Meta:
        model = CallBack
        fields = ('name', 'phone_number', 'reason')


class ContactsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contacts
        fields = '__all__'


class AdvantagesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Advantages
        fields = '__all__'


class MainPageIconSerializer(serializers.ModelSerializer):

    class Meta:
        model = MainPageIcon
        fields = '__all__'


class AboutSerializer(serializers.ModelSerializer):

    class Meta:
        model = AboutUs
        fields = '__all__'


class NewsSerializer(serializers.ModelSerializer):

    class Meta:
        model = News
        fields = '__all__'


class OfferSerializer(serializers.ModelSerializer):

    class Meta:
        model = Offer
        fields = '__all__'


class HelpIconSerializer(serializers.ModelSerializer):

    class Meta:
        model = HelpIcon
        fields = ['icon']


class HelpSerializer(serializers.ModelSerializer):
    helpicon = HelpIconSerializer()

    class Meta:
        model = Help
        fields = ['question', 'answer', 'helpicon']
