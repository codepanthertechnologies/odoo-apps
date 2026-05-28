import re

from odoo import api, models


class DuplicateDetectionMixin(models.AbstractModel):
    _name = "duplicate.detection.mixin"
    _description = "Duplicate Detection Mixin"

    @api.model
    def _normalize_email(self, value):
        if not value:
            return False

        return value.strip().lower()

    @api.model
    def _normalize_phone(self, value):
        if not value:
            return False

        return re.sub(r"\D", "", value)

    @api.model
    def _get_config_param(self, key, default=False):
        value = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param(key)
        )

        if value is None:
            return default

        return str(value).strip().lower() in (
            "1",
            "true",
            "yes",
        )

    @api.model
    def _build_duplicate_domain(
        self,
        field_name,
        value,
        current_id=None,
    ):
        domain = [
            (field_name, "=", value),
        ]

        if current_id:
            domain.append(("id", "!=", current_id))

        return domain

    @api.model
    def _find_duplicate(
        self,
        model_name,
        field_name,
        value,
        current_id=None,
        active_test=True,
    ):
        if not value:
            return False

        model = self.env[model_name].with_context(
            active_test=active_test
        )

        domain = self._build_duplicate_domain(
            field_name=field_name,
            value=value,
            current_id=current_id,
        )

        return model.search(domain, limit=1)

    @api.model
    def _warning_message(self, title, message):
        return {
            "warning": {
                "title": title,
                "message": message,
            }
        }