from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from catalog.models import Product, Category

from .cart import Cart


# =========================================================
# PANIER — AJOUTER
# =========================================================

def add(request):
    """
    Ajoute un produit au panier.
    """

    if request.method != "POST":
        return redirect("cart:view")

    product_slug = request.POST.get("slug", "")

    product = get_object_or_404(
        Product,
        slug=product_slug,
        status=Product.Status.AVAILABLE,
    )

    quantity = request.POST.get("quantity", "1")

    try:
        quantity = int(quantity)
    except (TypeError, ValueError):
        quantity = 1

    quantity = max(1, min(quantity, 99))

    cart = Cart(request)

    cart.add(
        product,
        quantity,
    )

    messages.success(
        request,
        f"{product.name} a été ajouté au panier."
    )

    return redirect("cart:view")


# =========================================================
# PANIER — MODIFIER QUANTITÉ
# =========================================================

def set_quantity(request):
    """
    Modifie la quantité d'un produit dans le panier.
    """

    if request.method != "POST":
        return redirect("cart:view")

    product_slug = request.POST.get("slug", "")

    if not product_slug:
        return redirect("cart:view")

    product = get_object_or_404(
        Product,
        slug=product_slug,
        status=Product.Status.AVAILABLE,
    )

    quantity = request.POST.get("quantity", "1")

    try:
        quantity = int(quantity)
    except (TypeError, ValueError):
        quantity = 1

    # Sécurité : entre 0 et 99
    quantity = max(0, min(quantity, 99))

    cart = Cart(request)

    cart.set_quantity(
        product,
        quantity,
    )

    if quantity == 0:
        messages.success(
            request,
            f"{product.name} a été retiré du panier."
        )
    else:
        messages.success(
            request,
            "Quantité modifiée."
        )

    return redirect("cart:view")


# =========================================================
# PANIER — AFFICHER
# =========================================================

def view_cart(request):
    """
    Affiche le panier.
    """

    cart = Cart(request)

    return render(
        request,
        "cart/view.html",
        {
            "cart": cart,
        },
    )


# =========================================================
# COLLECTION
# =========================================================

def product_catalogue(request):
    """
    Affiche tous les produits disponibles.
    """

    products = (
        Product.objects
        .filter(
            status=Product.Status.AVAILABLE
        )
        .select_related("category")
        .order_by("-id")
    )

    return render(
        request,
        "catalog/product_list.html",
        {
            "products": products,
        },
    )


# =========================================================
# PAGE PRODUIT
# =========================================================

def product_detail(request, slug):
    """
    Affiche la fiche détaillée d'un produit.
    """

    product = get_object_or_404(
        Product.objects.select_related("category"),
        slug=slug,
        status=Product.Status.AVAILABLE,
    )

    return render(
        request,
        "catalog/product.html",
        {
            "product": product,
        },
    )


# =========================================================
# NOUVEAUTÉS
# =========================================================

def nouveautes(request):
    """
    Affiche les produits les plus récents.
    """

    products = (
        Product.objects
        .filter(
            status=Product.Status.AVAILABLE
        )
        .select_related("category")
        .order_by("-id")
    )

    return render(
        request,
        "catalog/nouveautes.html",
        {
            "products": products,
        },
    )


# =========================================================
# JOURNAL
# =========================================================

def journal(request):
    """
    Affiche la page Journal de BrickMarket.
    """

    return render(
        request,
        "catalog/journal.html",
    )