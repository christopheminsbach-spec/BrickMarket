from catalog.models import Product


# ============================================================
# CONFIGURATION DU PANIER
# ============================================================

# 7,90 € en centimes
SHIPPING_FEES = 790

# Livraison gratuite à partir de 75 €
FREE_SHIPPING_THRESHOLD = 7500

# Clé utilisée pour stocker le panier dans la session Django
CART_SESSION_KEY = "cart"


class Cart:
    """
    Gestion du panier d'achat.

    Structure de la session :

    {
        "cart": {
            "slug-du-produit": {
                "quantity": 2
            }
        }
    }
    """

    def __init__(self, request):
        """
        Initialise le panier à partir de la session Django.
        """

        self.session = request.session

        cart = self.session.get(CART_SESSION_KEY)

        if not isinstance(cart, dict):
            cart = {}

        self.cart = cart

        # S'assurer que la session contient bien le panier
        self.session[CART_SESSION_KEY] = self.cart

    # ========================================================
    # AJOUTER
    # ========================================================

    def add(self, product, quantity=1):
        """
        Ajoute une quantité au panier.

        Exemple :

        Panier :
            produit × 1

        add(product, 1)

        Résultat :
            produit × 2
        """

        try:
            quantity = int(quantity)
        except (TypeError, ValueError):
            quantity = 1

        if quantity <= 0:
            return

        slug = product.slug

        if slug in self.cart:

            current_quantity = self.cart[slug].get(
                "quantity",
                0
            )

            self.cart[slug]["quantity"] = (
                current_quantity + quantity
            )

        else:

            self.cart[slug] = {
                "quantity": quantity
            }

        self._save()

    # ========================================================
    # SUPPRIMER UN PRODUIT
    # ========================================================

    def remove(self, product):
        """
        Supprime complètement un produit du panier.
        """

        self.cart.pop(product.slug, None)

        self._save()

    # ========================================================
    # MODIFIER LA QUANTITÉ
    # ========================================================

    def set_quantity(self, product, quantity):
        """
        Définit précisément la quantité d'un produit.

        quantity = 0
            → produit supprimé

        quantity = 1
            → une unité

        quantity = 2
            → deux unités
        """

        try:
            quantity = int(quantity)
        except (TypeError, ValueError):
            quantity = 1

        if quantity <= 0:
            self.remove(product)
            return

        self.cart[product.slug] = {
            "quantity": quantity
        }

        self._save()

    # ========================================================
    # VIDER LE PANIER
    # ========================================================

    def empty(self):
        """
        Vide complètement le panier.
        """

        self.cart = {}

        self._save()

    # ========================================================
    # SAUVEGARDE SESSION
    # ========================================================

    def _save(self):
        """
        Sauvegarde le panier dans la session Django.
        """

        self.session[CART_SESSION_KEY] = self.cart
        self.session.modified = True

    # ========================================================
    # NOMBRE TOTAL D'ARTICLES
    # ========================================================

    def __len__(self):
        """
        Retourne le nombre total d'articles.

        Exemple :

            LEGO A × 2
            LEGO B × 3

        Résultat :

            5
        """

        total = 0

        for line in self.cart.values():

            try:
                quantity = int(
                    line.get("quantity", 0)
                )
            except (TypeError, ValueError):
                quantity = 0

            total += max(quantity, 0)

        return total

    # ========================================================
    # PARCOURIR LE PANIER
    # ========================================================

    def __iter__(self):
        """
        Permet de faire :

            for item in cart:
                ...

        Chaque élément contient :

            product
            quantity
            total_price_in_cents
        """

        if not self.cart:
            return

        products = Product.objects.filter(
            slug__in=self.cart.keys()
        )

        for product in products:

            line = self.cart.get(
                product.slug,
                {}
            )

            try:
                quantity = int(
                    line.get("quantity", 0)
                )
            except (TypeError, ValueError):
                quantity = 0

            if quantity <= 0:
                continue

            yield {
                "product": product,
                "quantity": quantity,
                "total_price_in_cents": (
                    product.price * quantity
                ),
            }

    # ========================================================
    # SOUS-TOTAL
    # ========================================================

    def subtotal(self):
        """
        Calcule le sous-total hors livraison.
        """

        return sum(
            item["total_price_in_cents"]
            for item in self
        )

    # ========================================================
    # FRAIS DE LIVRAISON
    # ========================================================

    def shipping_fees(self):
        """
        Calcule les frais de livraison.

        Panier vide :
            0 €

        À partir de 75 € :
            livraison gratuite

        Sinon :
            7,90 €
        """

        if not self.cart:
            return 0

        if self.subtotal() >= FREE_SHIPPING_THRESHOLD:
            return 0

        return SHIPPING_FEES

    # ========================================================
    # TOTAL
    # ========================================================

    def total(self):
        """
        Calcule :

            sous-total + livraison
        """

        return (
            self.subtotal()
            + self.shipping_fees()
        )

    # ========================================================
    # LIVRAISON GRATUITE
    # ========================================================

    def is_shipping_free(self):
        """
        Retourne True si la livraison est gratuite.
        """

        return self.shipping_fees() == 0