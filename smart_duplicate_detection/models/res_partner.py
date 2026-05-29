from odoo import api, models
from .duplicate_mixin import DuplicateDetectionMixin


class ResPartner(DuplicateDetectionMixin, models.Model):
    _inherit = "res.partner"

    @api.onchange("email", "mobile", "phone")
    def _onchange_duplicate_contact(self):
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

        # --- Email ---
        if self._get_config_param(
            "smart_duplicate_detection.enable_email_check", True
        ) and self.email:
            dup = self._find_duplicate_email(
                model_name="res.partner",
                field_name="email",
                raw_value=self.email,
                current_id=self.id,
                active_test=active_test,
            )
            if dup:
                msg = (
                    f"A contact with the same Email already exists: "
                    f"{dup.display_name}"
                )
                if warning_only:
                    return self._warning_message(
                        "Duplicate Contact Detected", msg
                    )
                else:
                    from odoo.exceptions import ValidationError
                    raise ValidationError(msg)

        # --- Mobile ---
        if self._get_config_param(
            "smart_duplicate_detection.enable_mobile_check", True
        ) and self.mobile:
            dup = self._find_duplicate_phone(
                model_name="res.partner",
                field_name="mobile",
                raw_value=self.mobile,
                current_id=self.id,
                active_test=active_test,
            )
            if dup:
                msg = (
                    f"A contact with the same Mobile already exists: "
                    f"{dup.display_name}"
                )
                if warning_only:
                    return self._warning_message(
                        "Duplicate Contact Detected", msg
                    )
                else:
                    from odoo.exceptions import ValidationError
                    raise ValidationError(msg)

        # --- Phone ---
        if self._get_config_param(
            "smart_duplicate_detection.enable_phone_check", True
        ) and self.phone:
            dup = self._find_duplicate_phone(
                model_name="res.partner",
                field_name="phone",
                raw_value=self.phone,
                current_id=self.id,
                active_test=active_test,
            )
            if dup:
                msg = (
                    f"A contact with the same Phone already exists: "
                    f"{dup.display_name}"
                )
                if warning_only:
                    return self._warning_message(
                        "Duplicate Contact Detected", msg
                    )
                else:
                    from odoo.exceptions import ValidationError
                    raise ValidationError(msg)