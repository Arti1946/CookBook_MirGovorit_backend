from django.http import HttpResponse

from django.shortcuts import render, get_object_or_404

from .models import RecipeProduct, Recipe, Product


def add_product_to_recipe(request, recipe_id, product_id, weight):
    """Добавляет к указанному рецепту указанный продукт с указанным весом."""
    if request.method == "GET":
        recipe = get_object_or_404(Recipe, id=recipe_id)
        product = get_object_or_404(Product, id=product_id)
        if RecipeProduct.objects.filter(
            recipes=recipe_id, products=product_id
        ).exists():
            recipe_with_product = RecipeProduct.objects.get(
                recipes=recipe, products=product
            )
            recipe_with_product.weight = weight
            recipe_with_product.save()
            return HttpResponse(
                f"successfully changed weight of product {product.name} in recipe {recipe.name}"
            )
        else:
            RecipeProduct.objects.create(
                recipes=recipe, products=product, weight=weight
            )
            return HttpResponse(
                f"Successfully added product {product.name} to recipe {recipe.name}",
                status=200,
            )
    return HttpResponse("Not allowed method", status=405)


def cook_recipe(request, recipe_id):
    """Увеличивает на единицу количество приготовленных блюд для каждого продукта, входящего в указанный рецепт."""
    if request.method == "GET":
        products_id = RecipeProduct.objects.filter(
            recipes=recipe_id
        ).values_list("products")
        products = Product.objects.filter(id__in=products_id)
        for product in products:
            product.amount_of_cooking += 1
            product.save()
        return HttpResponse(
            "Successfully changed amount of cooking for products in recipe",
            status=200,
        )
    return HttpResponse("Not allowed method", status=405)


def show_recipes_without_product(request, product_id):
    """Возвращает HTML страницу, на которой размещена таблица.
    В таблице отображены id и названия всех рецептов, в которых указанный продукт отсутствует,
    или присутствует в количестве меньше 10 грамм.
    """
    if request.method == "GET":
        recipes_id = RecipeProduct.objects.filter(
            products=product_id, weight__lt=10
        ).values_list("recipes")
        recipes = set(Recipe.objects.filter(id__in=recipes_id))
        recipes_without_product = RecipeProduct.objects.filter(
            products=product_id
        ).values_list("recipes")
        recipes.update(Recipe.objects.exclude(id__in=recipes_without_product))
        context = {"recipes": recipes}
        return render(request, "index.html", context)
    return HttpResponse("Not allowed method", status=405)
