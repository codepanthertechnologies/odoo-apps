from odoo import api, models


class ResPartner(models.Model):
    _inherit = [
        "res.partner",
        "duplicate.detection.mixin",
    ]

    @api.onchange("email", "mobile", "phone")
    def _onchange_duplicate_contact(self):
        self.ensure_one()

        ignore_archived = self._get_config_param(
            "smart_duplicate_detection.ignore_archived_records",
            False,
        )

        email = getattr(self, "email", False)
        mobile = getattr(self, "mobile", False)
        phone = getattr(self, "phone", False)

        checks = [
            (
                "email",
                "smart_duplicate_detection.enable_email_check",
                self._normalize_email(email),
                "Email",
            ),
            (
                "mobile",
                "smart_duplicate_detection.enable_mobile_check",
                self._normalize_phone(mobile),
                "Mobile",
            ),
            (
                "phone",
                "smart_duplicate_detection.enable_phone_check",
                self._normalize_phone(phone),
                "Phone",
            ),
        ]

        for field_name, config_key, value, label in checks:
            enabled = self._get_config_param(config_key, True)

            if not enabled or not value:
                continue

            duplicate = self._find_duplicate(
                model_name="res.partner",
                field_name=field_name,
                value=value,
                current_id=self.id,
                active_test=not ignore_archived,
            )

            if duplicate:
                return self._warning_message(
                    title="Duplicate Contact Detected",
                    message=(
                        f"A contact with the same {label} "
                        f"already exists: {duplicate.display_name}"
                    ),
                )