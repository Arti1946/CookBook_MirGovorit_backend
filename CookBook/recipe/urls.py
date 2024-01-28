from django.urls import path

from . import views

app_name = "recipe"

urlpatterns = [
    path(
        "show_recipes/<product_id>/",
        views.show_recipes_without_product,
        name="show_recipes",
    ),
    path(
        "add_product/<recipe_id>/<product_id>/<weight>/",
        views.add_product_to_recipe,
    ),
    path("cook_recipe/<recipe_id>/", views.cook_recipe),
]
