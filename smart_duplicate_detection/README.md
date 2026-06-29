# Smart Duplicate Detection

Realtime duplicate detection for Contacts and Products in Odoo 16.

## Features

### Contact Duplicate Detection

- Email
- Mobile
- Phone

### Product Duplicate Detection

- Barcode
- Internal Reference (`default_code`)

## Key Highlights

- Realtime soft warnings via `@api.onchange`
- No blocking by default (configurable)
- Lightweight ORM queries
- Case-insensitive email matching
- Self-exclusion — ignores the current record
- Ignores empty field values
- Fully configurable per-check settings
- Production-ready architecture

## Odoo Version

This module targets **Odoo 16**.

> For Odoo 17/18, a separate `17.0.x.y.z` branch is available.

## Configuration

Go to:

```
Settings → Smart Duplicate Detection
```

### Available Options

| Setting | Description |
|---|---|
| Email Check | Warn when a contact with the same email already exists |
| Mobile Check | Warn when a contact with the same mobile already exists |
| Phone Check | Warn when a contact with the same phone already exists |
| Barcode Check | Warn when a product with the same barcode already exists |
| Internal Reference Check | Warn when a product with the same internal reference already exists |
| Ignore Archived Records | Skip archived contacts/products during duplicate checks |
| Warning Only Mode | Show a soft warning only (does not block saving). Disable to raise a hard `ValidationError`. |

## Installation

1. Copy the `smart_duplicate_detection` folder into your Odoo 16 `addons` directory.
2. Restart the Odoo server.
3. Go to **Apps**, search for **Smart Duplicate Detection**, and install.

## Dependencies

- `base`
- `contacts`
- `product`

## Author

**Code Panther Technologies**

Website: https://codepanther.netlify.app