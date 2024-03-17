from itertools import chain

from django.db.models import Case, When, Value, IntegerField
from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import User, Group
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics, views, status
from rest_framework import permissions
from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.response import Response

from core.extensions import CustomResponseViewSet, CustomRetrieveViewSet, CustomRetrieveUpdateViewSet
from core.filters import NewsFilter
from core.models import News, Employe, Profile, Wallet, Cart, ShopCategory, ShopItems
from core.response import CustomResponse
from core.serializes import NewsSerializer, EmployesSerializer, WalletSerializer, ShopSerializer, ShopItemsSerializer, \
    ProfileSerializer


class NewsViewSet(CustomResponseViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = NewsFilter
    permission_classes = [permissions.IsAuthenticated]


class EmployesViewSet(CustomResponseViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Employe.objects.all()
    serializer_class = EmployesSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Employe.objects.all()
        user = self.request.user
        if user is not None and user.is_authenticated:
            profile_employe_id = user.profile.employe.id
            # Добавьте поле 'sort_order' с помощью annotate
            queryset = queryset.annotate(
                sort_order=Case(
                    When(id=profile_employe_id, then=Value(0)),
                    default=Value(1),
                    output_field=IntegerField(),
                )
            )
            # Сортируйте по 'sort_order' и затем по имени
            queryset = queryset.order_by('sort_order', 'name')
        return queryset

class ShopViewSet(CustomResponseViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = ShopCategory.objects.all()
    serializer_class = ShopSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['post'])
    def buy(self, request):
        item_id = request.data.get('item_id')
        if not item_id:
            return CustomResponse(status=status.HTTP_400_BAD_REQUEST)

        try:
            item = ShopItems.objects.get(id=item_id)
        except ShopItems.DoesNotExist:
            return CustomResponse(status=status.HTTP_404_NOT_FOUND)

        profile = Profile.objects.get(user=request.user)
        wallet = Wallet.objects.get(profile=profile)
        cart, _ = Cart.objects.get_or_create(profile=profile)

        if cart.items.filter(id=item_id).exists():
            cart.items.remove(item)
            wallet.wallet += item.coast
            wallet.save()
            serializer = ShopItemsSerializer(item, context={'request': request})
            return CustomResponse(serializer.data, status=status.HTTP_200_OK)

        if wallet.wallet < item.coast:
            return CustomResponse( status=status.HTTP_400_BAD_REQUEST)

        cart.items.add(item)
        wallet.wallet -= item.coast
        wallet.save()

        serializer = ShopItemsSerializer(item, context={'request': request})
        return CustomResponse(serializer.data, status=status.HTTP_200_OK)


class WalletView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        profile = Profile.objects.get(user=request.user)
        wallet = Wallet.objects.get(profile=profile)
        serializer = WalletSerializer(wallet)
        return CustomResponse(serializer.data)


class UserProfileView(CustomRetrieveUpdateViewSet):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.profile