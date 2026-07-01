from odoo import api, models
from odoo.exceptions import ValidationError
from .duplicate_mixin import DuplicateDetectionMixin


class ResPartner(DuplicateDetectionMixin, models.Model):
    _inherit = "res.partner"

    def _duplicate_checks(self):
        return [
            ("enable_email_check", "email", "Email", self._find_duplicate_email),
            ("enable_mobile_check", "mobile", "Mobile", self._find_duplicate_phone),
            ("enable_phone_check", "phone", "Phone", self._find_duplicate_phone),
        ]

    def _get_duplicate_message(self, flag, field_name, label, finder):
        raw_value = self[field_name]
        if not raw_value:
            return None
        if not self._get_config_param(
            f"smart_duplicate_detection.{flag}", True
        ):
            return None
        ignore_archived = self._get_config_param(
            "smart_duplicate_detection.ignore_archived_records", False
        )
        dup = finder(
            model_name="res.partner",
            field_name=field_name,
            raw_value=raw_value,
            current_id=self.id,
            active_test=not ignore_archived,
        )
        if not dup:
            return None
        return (
            f"A contact with the same {label} already exists: "
            f"{dup.display_name}"
        )

    @api.onchange("email", "mobile", "phone")
    def _onchange_duplicate_contact(self):
        """UI-only hint. Never blocks saving on its own."""
        self.ensure_one()
        for flag, field_name, label, finder in self._duplicate_checks():
            msg = self._get_duplicate_message(flag, field_name, label, finder)
            if msg:
                return self._warning_message(
                    "Duplicate Contact Detected", msg
                )

    @api.constrains("email", "mobile", "phone")
    def _check_duplicate_contact(self):
        """Real constraint: runs on create/write and actually blocks save
        when warning-only mode is disabled."""
        for record in self:
            warning_only = record._get_config_param(
                "smart_duplicate_detection.warning_only_mode", True
            )
            if warning_only:
                continue
            for flag, field_name, label, finder in record._duplicate_checks():
                msg = record._get_duplicate_message(
                    flag, field_name, label, finder
                )
                if msg:
                    raise ValidationError(msg)
                    