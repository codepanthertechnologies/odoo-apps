from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    enable_email_check = fields.Boolean(
        string="Enable Email Duplicate Check",
        config_parameter=(
            "smart_duplicate_detection.enable_email_check"
        ),
    )

    enable_phone_check = fields.Boolean(
        string="Enable Phone Duplicate Check",
        config_parameter=(
            "smart_duplicate_detection.enable_phone_check"
        ),
    )

    enable_barcode_check = fields.Boolean(
        string="Enable Barcode Duplicate Check",
        config_parameter=(
            "smart_duplicate_detection.enable_barcode_check"
        ),
    )

    enable_internal_ref_check = fields.Boolean(
        string="Enable Internal Reference Check",
        config_parameter=(
            "smart_duplicate_detection.enable_internal_ref_check"
        ),
    )

    ignore_archived_records = fields.Boolean(
        string="Ignore Archived Records",
        config_parameter=(
            "smart_duplicate_detection.ignore_archived_records"
        ),
    )

    warning_only_mode = fields.Boolean(
        string="Warning Only Mode",
        config_parameter=(
            "smart_duplicate_detection.warning_only_mode"
        ),
    )