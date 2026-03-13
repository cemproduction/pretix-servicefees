from django.db import models
from django.utils.translation import gettext_lazy as _

FEE_MODE_ADD = "add"
FEE_MODE_INCLUDE = "include"
FEE_MODE_CHOICES = [
    (FEE_MODE_ADD, _("Added to the product price")),
    (FEE_MODE_INCLUDE, _("Included in the product price")),
]


class ItemServicefeesSettings(models.Model):
    item = models.OneToOneField(
        "pretixbase.Item", related_name="servicefees_settings", on_delete=models.CASCADE
    )
    exclude = models.BooleanField(
        verbose_name=_(
            "Exclude this product from the calculation of per-ticket and percentual service fees"
        )
    )
    # Per-product fee override (null = use event default)
    fee_amount = models.DecimalField(
        max_digits=13,
        decimal_places=2,
        null=True,
        blank=True,
        default=None,
        verbose_name=_("Fee (amount)"),
    )
    fee_percent = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        null=True,
        blank=True,
        default=None,
        verbose_name=_("Fee (percent)"),
    )
    fee_mode = models.CharField(
        max_length=20,
        choices=FEE_MODE_CHOICES,
        null=True,
        blank=True,
        default=None,
        verbose_name=_("Fee mode"),
    )
