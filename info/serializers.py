from rest_framework import serializers
from .models import AboutUs, News, Help, Offer, Contacts, Advantages, MainPageIcon


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


class HelpSerializer(serializers.ModelSerializer):

    class Meta:
        model = Help
        fields = '__all__'


class OfferSerializer(serializers.ModelSerializer):

    class Meta:
        model = Offer
        fields = '__all__'