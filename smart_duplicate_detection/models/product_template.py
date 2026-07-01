from odoo import api, models
from .duplicate_mixin import DuplicateDetectionMixin


class ProductTemplate(DuplicateDetectionMixin, models.Model):
    _inherit = "product.template"

    @api.onchange("barcode", "default_code")
    def _onchange_duplicate_product(self):
        self.ensure_one()

        ignore_archived = self._get_config_param(
            "smart_duplicate_detection.ignore_archived_records",
            False,
        )
        warning_only = self._get_config_param(
            "smart_duplicate_detection.warning_only_mode",
            True,
        )
        active_test = not ignore_archived

        checks = [
            (
                "barcode",
                "smart_duplicate_detection.enable_barcode_check",
                self.barcode,
                "Barcode",
                # NOTE: barcode lives on product.product (variants).
                # We check product.template here for the single-variant
                # common case. Multi-variant barcode checking requires
                # querying product.product — planned for v2.
                "product.template",
            ),
            (
                "default_code",
                "smart_duplicate_detection.enable_internal_ref_check",
                self.default_code,
                "Internal Reference",
                "product.template",
            ),
        ]

        for field_name, config_key, value, label, model_name in checks:
            enabled = self._get_config_param(config_key, True)
            if not enabled or not value:
                continue

            duplicate = self._find_duplicate(
                model_name=model_name,
                field_name=field_name,
                value=value,
                current_id=self.id,
                active_test=active_test,
            )

            if duplicate:
                msg = (
                    f"A product with the same {label} already exists: "
                    f"{duplicate.display_name}"
                )
                if warning_only:
                    return self._warning_message(
                        "Duplicate Product Detected", msg
                    )
                else:
                    from odoo.exceptions import ValidationError
                    raise ValidationError(msg)
