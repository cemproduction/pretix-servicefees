"""
Tests for per-product fee "included" mode: fee appears in cart/invoice and
position prices are reduced by the fee amount so the total stays correct.
"""
from decimal import Decimal
from unittest.mock import MagicMock, patch

import pytest

from pretix_servicefees.signals import get_fees


@pytest.mark.django_db
@patch("pretix_servicefees.signals.ItemServicefeesSettings")
def test_get_fees_include_mode_adds_fee_line_and_reduces_position_price(mock_settings_cls):
    """With FEE_MODE_INCLUDE, get_fees returns a per-product OrderFee and mutates position price."""
    mock_settings_cls.objects.filter.return_value.select_related.return_value = []

    event = MagicMock()
    event.currency = "EUR"
    event.settings = MagicMock()
    _settings = {
        "service_fee_skip_free": True,
        "service_fee_skip_addons": True,
        "service_fee_skip_non_admission": False,
        "service_fee_product_amount": Decimal("1.00"),
        "service_fee_product_percent": Decimal("0.00"),
        "service_fee_product_mode": "include",
        "service_fee_tax_rule": "default",
    }

    event.settings.get = lambda k, as_type=None, default=None: _settings.get(k, default)
    event.cached_default_tax_rule = None

    # One position: price 10.00, fee 1.00 -> after reduction price should be 9.00
    pos = MagicMock()
    pos.item_id = 1
    pos.addon_to_id = None
    pos.price = Decimal("10.00")
    pos.gross_price_before_rounding = Decimal("10.00")
    pos.count = 1
    pos.quantity = 1
    pos.item = MagicMock()
    pos.item.admission = True

    invoice_address = None
    total = Decimal("10.00")

    fees = get_fees(event, total, invoice_address, positions=[pos])

    # Should have one per-product fee of 1.00
    assert len(fees) == 1
    assert fees[0].internal_type == "servicefees_product"
    assert fees[0].value == Decimal("1.00")

    # Position price should be reduced by the fee (10 - 1 = 9)
    assert pos.price == Decimal("9.00")
    assert pos.gross_price_before_rounding == Decimal("9.00")
