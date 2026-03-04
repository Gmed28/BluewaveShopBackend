from decimal import Decimal
from django.apps import apps
from django.db import transaction
from django.db import models


MUCKIE_EXAMPLES = [
    ("Muckie Glitchwave Hoodie", "Oversize Hoodie im Glitch-Print (limitiert).",
     "Signature-Piece: Neon-Akzente, Typo, Glitch-Pattern.", 7, Decimal("54.90")),
    ("Muckie Neon-Koi Sneakers", "Sneaker mit Neon-Paneling & Koi-Illustration.",
     "Reflektierende Details, Mesh, auffälliger Neon-Koi.", 12, Decimal("79.95")),
    ("Muckie Holo-Mug (Thermo)", "Farbwechsel-Becher mit Holo-Schimmer.",
     "Reagiert auf Wärme: dezent → Holo-Overdrive. 350ml.", 25, Decimal("16.50")),
    ("Muckie RGB Jelly Desk Lamp", "RGB-Lampe mit Jelly-Diffusor (dimmbar).",
     "Warm/Neutral/RGB, flexibler Arm, perfektes Setup-Licht.", 4, Decimal("34.90")),
    ("Muckie Stickerbomb Pack (50x)", "50 Sticker: Glitch, Mascots, UI-Icons.",
     "Laptop, Notizbuch, Bottle – überall wo’s zu clean ist.", 40, Decimal("9.90")),
]


def _resolve_field(model, candidates, required=True):
    fields = {f.name for f in model._meta.get_fields()}
    for c in candidates:
        if c in fields:
            return c
    if required:
        raise RuntimeError(f"Keines dieser Felder existiert in {model.__name__}: {candidates}")
    return None


def seed_muckie_products_post_migrate(sender, **kwargs):
    # Signal-Handler
    seed_muckie_products()


def seed_muckie_products():
    Product = apps.get_model("pinguinAPI", "Product")

    # schon Daten da? -> nichts tun
    if Product.objects.exists():
        return

    # Feldnamen automatisch finden (weil dein Model wohl nicht 'name' heißt)
    f_name = _resolve_field(Product, ["name", "product_name", "title"])
    f_short = _resolve_field(Product, ["short_description", "shortDescription", "short_desc", "kurzbeschreibung"])
    f_desc = _resolve_field(Product, ["product_description", "productDescription", "description", "long_description"])
    f_stock = _resolve_field(Product, ["stock", "bestand", "quantity", "qty"])
    f_price = _resolve_field(Product, ["price", "preis", "product_price"])
    f_image = _resolve_field(Product, ["product_image", "image", "img", "picture"], required=False)

    with transaction.atomic():
        for name, short_d, long_d, stock_amount, price in MUCKIE_EXAMPLES:
            kwargs = {
                f_name: name,
                f_short: short_d,
                f_desc: long_d,
                f_price: price,
            }

            # stock: entweder IntegerField ODER Relation (FK/OneToOne)
            stock_field = Product._meta.get_field(f_stock)
            if isinstance(stock_field, (models.ForeignKey, models.OneToOneField)):
                StockModel = stock_field.remote_field.model

                # StockModel hat evtl. 'amount' oder 'stock' oder 'quantity'
                stock_amount_field = _resolve_field(StockModel, ["amount", "stock", "quantity", "qty"])
                stock_obj = StockModel.objects.create(**{stock_amount_field: stock_amount})
                kwargs[f_stock] = stock_obj
            else:
                kwargs[f_stock] = stock_amount

            # optionales Image-Feld: wenn vorhanden, leer setzen (falls erlaubt)
            if f_image:
                img_field = Product._meta.get_field(f_image)
                if isinstance(img_field, (models.FileField, models.ImageField)):
                    kwargs[f_image] = ""  # safe, wenn blank=True
                elif img_field.null:
                    kwargs[f_image] = None
                else:
                    kwargs[f_image] = ""  # fallback

            Product.objects.create(**kwargs)