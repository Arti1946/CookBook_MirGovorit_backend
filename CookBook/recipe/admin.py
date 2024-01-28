from django.contrib import admin

from .models import Recipe, RecipeProduct, Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "amount_of_cooking")
    readonly_fields = ("amount_of_cooking",)
    list_editable = ("name",)
    ordering = ("id",)


@admin.register(RecipeProduct)
class RecipeProductAdmin(admin.ModelAdmin):
    list_display = ("recipes", "products", "weight_of_product")
    list_filter = ("recipes", "products")
    ordering = ("recipes",)

    def get_queryset(self, request):
        query = RecipeProduct.objects.select_related("products", "recipes")
        return query

    @admin.display(description="Вес продукта")
    def weight_of_product(self, recipes_products):
        recipe = Recipe.objects.get(name=recipes_products.recipes)
        return f"{recipes_products.weight}{recipe.measurement_unit}"


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_editable = ("name",)
    ordering = ("id",)
