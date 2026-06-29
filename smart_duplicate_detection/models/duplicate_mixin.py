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
        """Strip all non-digit characters for comparison only.
        Do NOT use the result as a DB query value — phones are stored raw."""
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
        return str(value).strip().lower() in ("1", "true", "yes")

    @api.model
    def _find_duplicate_phone(
        self,
        model_name,
        field_name,
        raw_value,
        current_id=None,
        active_test=True,
    ):
        """Find a duplicate by comparing normalized phone digits.

        Odoo stores phone numbers as the user typed them (e.g. '+91-98765 43210').
        A direct DB equality query with a normalized value will always miss.
        We fetch candidates that share the same digit-only suffix and compare
        normalized values in Python instead.
        """
        if not raw_value:
            return False

        normalized = self._normalize_phone(raw_value)
        if not normalized:
            return False

        # Use the last 7 digits as a loose DB filter to keep the result set small.
        suffix = normalized[-7:] if len(normalized) >= 7 else normalized

        model = self.env[model_name].with_context(active_test=active_test)
        domain = [(field_name, "like", suffix)]
        if current_id:
            domain.append(("id", "!=", current_id))

        candidates = model.search(domain, limit=50)
        for rec in candidates:
            stored_raw = getattr(rec, field_name, False)
            if self._normalize_phone(stored_raw) == normalized:
                return rec
        return False

    @api.model
    def _find_duplicate_email(
        self,
        model_name,
        field_name,
        raw_value,
        current_id=None,
        active_test=True,
    ):
        """Find a duplicate by case-insensitive email comparison."""
        if not raw_value:
            return False

        normalized = self._normalize_email(raw_value)
        if not normalized:
            return False

        model = self.env[model_name].with_context(active_test=active_test)
        # '=ilike' is case-insensitive equality in Odoo ORM
        domain = [(field_name, "=ilike", normalized)]
        if current_id:
            domain.append(("id", "!=", current_id))

        return model.search(domain, limit=1)

    @api.model
    def _find_duplicate(
        self,
        model_name,
        field_name,
        value,
        current_id=None,
        active_test=True,
    ):
        """Generic exact-match duplicate finder (for barcode, internal ref, etc.)."""
        if not value:
            return False

        model = self.env[model_name].with_context(active_test=active_test)
        domain = [(field_name, "=", value)]
        if current_id:
            domain.append(("id", "!=", current_id))

        return model.search(domain, limit=1)

    @api.model
    def _warning_message(self, title, message):
        return {
            "warning": {
                "title": title,
                "message": message,
            }
        }