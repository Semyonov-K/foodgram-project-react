from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.views import APIView

from recipes.models import Favorite, Ingredient, Recipe, RecipeIngredient, Tag
from .filters import IngredientFilter, RecipeFilter
from .serializers import (FavoriteSerializer, IngredientSerializer,
                          RecipePostUpdateSerializer, RecipeSerializer,
                          ShoppingCartSerializer, TagSerializer)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filterset_class = IngredientFilter


class FavoriteViewSet(APIView):
    serializer_class = FavoriteSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        recipe_id = self.kwargs.get('recipe_id')
        recipe = get_object_or_404(Recipe, id=recipe_id)
        if Favorite.objects.filter(
                user=request.user,
                recipe_id=recipe_id
        ).exists():
            return Response(
                {'error': 'Рецепт уже добавлен в избранное'},
                status=status.HTTP_400_BAD_REQUEST
            )
        Favorite.objects.create(
            user=request.user,
            recipe_id=recipe_id
        )
        return Response(
            FavoriteSerializer(recipe, context={'request': request}).data,
            status=status.HTTP_201_CREATED
        )
    

    def delete(self, request, *args, **kwargs):
        recipe_id = self.kwargs.get('recipe_id')
        recipe = get_object_or_404(Recipe, id=recipe_id)
        favorite = Favorite.objects.filter(
            user=request.user,
            recipe_id=recipe_id
        )
        if favorite.exists():
            favorite.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {'error': 'Вы не подписаны на пользователя'},
            status=status.HTTP_400_BAD_REQUEST
        )


class ShoppingCartViewSet(FavoriteViewSet):
    serializer_class = ShoppingCartSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeSerializer
        return RecipePostUpdateSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=False,
            permission_classes=[IsAuthenticated],
            methods=['GET']
            )
    def download_shopping_cart(self, request):
        ingredients = RecipeIngredient.objects.filter(
            recipe__carts__user=request.user).values(
            'ingredient__name', 'ingredient__measurement_unit'
        ).order_by('ingredient__name').annotate(ingredient_total=Sum('amount'))
        content = ''
        for ingredient in ingredients:
            content += (
                f'∙ {ingredient["ingredient__name"]} '
                f'({ingredient["ingredient__measurement_unit"]}) '
                f'- {ingredient["ingredient_total"]}\n'
            )
        filename = "shopping_cart.txt"
        response = HttpResponse(
            content, content_type='text/plain', charset='utf-8'
        )
        response['Content-Disposition'] = (
            'attachment; filename={0}'.format(filename)
        )
        return response
