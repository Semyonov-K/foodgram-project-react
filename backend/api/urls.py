from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import FollowCreateViewSet, FollowViewSet
from .views import (FavoriteViewSet, IngredientViewSet, RecipeViewSet,
                    ShoppingCartViewSet, TagViewSet)

app_name = 'api'

router = DefaultRouter()

router.register('tags', TagViewSet, basename='tags')
router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('recipes', RecipeViewSet, basename='recipes')


urlpatterns = [
    path('users/<int:user_id>/subscribe/', FollowCreateViewSet.as_view(),
         name='follow'),
    path('users/subscriptions/', FollowViewSet.as_view(),
         name='subsciptions'),
    path('recipes/<int:recipe_id>/favorite/',
         FavoriteViewSet.as_view(), name='favorite'),
    path('recipes/<int:recipe_id>/shopping_cart/',
         ShoppingCartViewSet.as_view(), name='shopping_cart'),
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
