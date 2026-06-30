{
    "name": "Smart Duplicate Detection",
    "summary": "Realtime soft duplicate detection for contacts and products.",
    "description": """
Smart Duplicate Detection
=========================

Detect duplicate contacts and products using realtime warnings.

Features:
---------
* Contact duplicate detection
    - Email
    - Mobile
    - Phone

* Product duplicate detection
    - Barcode
    - Internal Reference

* Configurable checks
* Warning-only mode
* Lightweight ORM queries
* Production-ready architecture
    """,
    "version": "16.0.1.0.0",
    "category": "Tools",
    "license": "LGPL-3",
    "author": "Code Panther Technologies",
    "website": "https://codepanther.online",
    "images": [
        "static/description/banner.png",
    ],
    "depends": [
        "base",
        "contacts",
        "product",
    ],
    "data": [
        "views/res_partner_views.xml",
        "views/product_template_views.xml",
        "views/res_config_settings_views.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
}
