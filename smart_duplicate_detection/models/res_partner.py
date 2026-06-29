from odoo import api, models
from odoo.exceptions import ValidationError
from .duplicate_mixin import DuplicateDetectionMixin


class ResPartner(DuplicateDetectionMixin, models.Model):
    _inherit = "res.partner"

    @api.onchange("email", "mobile", "phone")
    def _onchange_duplicate_contact(self):
        """Live UI warning only — does not block saving."""
        self.ensure_one()
        ignore_archived = self._get_config_param(
            "smart_duplicate_detection.ignore_archived_records", False
        )
        active_test = not ignore_archived

        if (
            self._get_config_param("smart_duplicate_detection.enable_email_check", True)
            and self.email
        ):
            dup = self._find_duplicate_email(
                model_name="res.partner",
                field_name="email",
                raw_value=self.email,
                current_id=self.id,
                active_test=active_test,
            )
            if dup:
                return self._warning_message(
                    "Duplicate Contact Detected",
                    f"A contact with the same Email already exists: {dup.display_name}",
                )

        if (
            self._get_config_param("smart_duplicate_detection.enable_mobile_check", True)
            and self.mobile
        ):
            dup = self._find_duplicate_phone(
                model_name="res.partner",
                field_name="mobile",
                raw_value=self.mobile,
                current_id=self.id,
                active_test=active_test,
            )
            if dup:
                return self._warning_message(
                    "Duplicate Contact Detected",
                    f"A contact with the same Mobile already exists: {dup.display_name}",
                )

        if (
            self._get_config_param("smart_duplicate_detection.enable_phone_check", True)
            and self.phone
        ):
            dup = self._find_duplicate_phone(
                model_name="res.partner",
                field_name="phone",
                raw_value=self.phone,
                current_id=self.id,
                active_test=active_test,
            )
            if dup:
                return self._warning_message(
                    "Duplicate Contact Detected",
                    f"A contact with the same Phone already exists: {dup.display_name}",
                )

    @api.constrains("email", "mobile", "phone")
    def _constrains_duplicate_contact(self):
        """Hard block at save time — this actually prevents saving."""
        ignore_archived = self._get_config_param(
            "smart_duplicate_detection.ignore_archived_records", False
        )
        warning_only = self._get_config_param(
            "smart_duplicate_detection.warning_only_mode", True
        )

        # If warning_only mode is ON, skip the hard block
        if warning_only:
            return

        active_test = not ignore_archived

        for record in self:
            if (
                self._get_config_param("smart_duplicate_detection.enable_email_check", True)
                and record.email
            ):
                dup = self._find_duplicate_email(
                    model_name="res.partner",
                    field_name="email",
                    raw_value=record.email,
                    current_id=record.id,
                    active_test=active_test,
                )
                if dup:
                    raise ValidationError(
                        f"A contact with the same Email already exists: {dup.display_name}"
                    )

            if (
                self._get_config_param("smart_duplicate_detection.enable_mobile_check", True)
                and record.mobile
            ):
                dup = self._find_duplicate_phone(
                    model_name="res.partner",
                    field_name="mobile",
                    raw_value=record.mobile,
                    current_id=record.id,
                    active_test=active_test,
                )
                if dup:
                    raise ValidationError(
                        f"A contact with the same Mobile already exists: {dup.display_name}"
                    )

            if (
                self._get_config_param("smart_duplicate_detection.enable_phone_check", True)
                and record.phone
            ):
                dup = self._find_duplicate_phone(
                    model_name="res.partner",
                    field_name="phone",
                    raw_value=record.phone,
                    current_id=record.id,
                    active_test=active_test,
                )
                if dup:
                    raise ValidationError(
                        f"A contact with the same Phone already exists: {dup.display_name}"
                    )