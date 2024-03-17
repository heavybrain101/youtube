from django.contrib.auth.models import User, Group
from django.template.context_processors import request
from rest_framework import serializers

from core.models import News, Employe, Wallet, ShopCategory, ShopItems, Profile, Cart


class EmployesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Employe
        fields = ['id', 'name']


class ShopItemsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ShopItems
        fields = ['id', 'name', 'coast']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get('request')
        profile = Profile.objects.get(user=request.user)
        is_buy = Cart.objects.filter(profile=profile, items=instance).exists()
        representation['isBuy'] = is_buy
        return representation

class ShopSerializer(serializers.HyperlinkedModelSerializer):
    items = ShopItemsSerializer(many=True, read_only=True, context={'request': request})

    class Meta:
        model = ShopCategory
        fields = ['id', 'name', 'items']


class NewsSerializer(serializers.HyperlinkedModelSerializer):
    employe = EmployesSerializer()

    class Meta:
        model = News
        fields = ['id', 'text', 'title', 'image', 'employe']


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['id', 'wallet']

class ProfileSerializer(serializers.ModelSerializer):
    employe = serializers.PrimaryKeyRelatedField(queryset=Employe.objects.all())
    email = serializers.EmailField(source='user.email')  # Добавьте это поле
    class Meta:
        model = Profile
        fields = ['id', 'name', 'phone', 'employe', 'image', 'office', 'email']

    def update(self, instance, validated_data):
        # Обновите email пользователя, если он предоставлен
        user_data = validated_data.pop('user', None)
        if user_data:
            instance.user.email = user_data.get('email', instance.user.email)
            instance.user.save()

        instance = super().update(instance, validated_data)

        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get('request')
        if request and (request.method == 'GET' or request.method == 'PUT'):
            representation['employe'] = EmployesSerializer(instance.employe).data
        return representation
