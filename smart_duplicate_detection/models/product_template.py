from odoo import api, models


class ProductTemplate(models.Model):
    _inherit = [
        "product.template",
        "duplicate.detection.mixin",
    ]

    @api.onchange("barcode", "default_code")
    def _onchange_duplicate_product(self):
        self.ensure_one()

        ignore_archived = self._get_config_param(
            "smart_duplicate_detection.ignore_archived_records",
            False,
        )

        checks = [
            (
                "barcode",
                "smart_duplicate_detection.enable_barcode_check",
                self.barcode,
                "Barcode",
            ),
            (
                "default_code",
                "smart_duplicate_detection.enable_internal_ref_check",
                self.default_code,
                "Internal Reference",
            ),
        ]

        for field_name, config_key, value, label in checks:
            enabled = self._get_config_param(config_key, True)

            if not enabled or not value:
                continue

            duplicate = self._find_duplicate(
                model_name="product.template",
                field_name=field_name,
                value=value,
                current_id=self.id,
                active_test=not ignore_archived,
            )

            if duplicate:
                return self._warning_message(
                    title="Duplicate Product Detected",
                    message=(
                        f"A product with the same {label} "
                        f"already exists: {duplicate.display_name}"
                    ),
                )