from django.urls import path

from . import views


app_name = "cart"


urlpatterns = [

    # =====================================================
    # PANIER
    # =====================================================

    path(
        "",
        views.view_cart,
        name="view",
    ),

    path(
        "add/",
        views.add,
        name="add",
    ),

    path(
        "set_quantity/",
        views.set_quantity,
        name="set_quantity",
    ),

    # =====================================================
    # COLLECTION
    # =====================================================

    path(
        "products/",
        views.product_catalogue,
        name="product_catalogue",
    ),

    # =====================================================
    # PRODUIT
    # =====================================================

    path(
        "products/<slug:slug>/",
        views.product_detail,
        name="product_detail",
    ),

    # =====================================================
    # NOUVEAUTÉS
    # =====================================================

    path(
        "nouveautes/",
        views.nouveautes,
        name="nouveautes",
    ),

    # =====================================================
    # JOURNAL
    # =====================================================

    path(
        "journal/",
        views.journal,
        name="journal",
    ),
]