from django.db import models
from django.db.models import UniqueConstraint


class Product(models.Model):
    name = models.CharField("Название", max_length=150)
    amount_of_cooking = models.PositiveIntegerField(
        default=0,
        blank=True,
        null=True,
        verbose_name="Колличество приготовленных блюд",
    )

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"

    def __str__(self):
        return self.name


class Recipe(models.Model):
    products = models.ManyToManyField(
        Product,
        through="RecipeProduct",
        through_fields=("recipes", "products"),
        related_name="recipes",
        verbose_name="продукт",
    )
    name = models.CharField("Название", max_length=150)
    measurement_unit = models.CharField(
        "Единица измерения", max_length=1, default="г", editable=False
    )

    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"

    def __str__(self):
        return self.name


class RecipeProduct(models.Model):
    recipes = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="recipes_products",
        verbose_name="Рецепт",
    )
    products = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="recipes_products",
        verbose_name="Продукт",
    )
    weight = models.PositiveSmallIntegerField(verbose_name="Вес")

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["recipes", "products"],
                name="unique_recipes_products",
            )
        ]
        verbose_name = "Рецепт и Продукт"
        verbose_name_plural = "Рецепты и Продукты"
