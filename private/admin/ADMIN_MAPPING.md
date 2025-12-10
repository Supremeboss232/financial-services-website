Admin Folder Mapping

This document maps admin templates to their responsibilities and describes the linking/navigation strategy used across `private/admin`.

Templates & Purpose
- `base.html`: Global admin layout. Provides sidebar navigation, `page_title`, `back_button`, `content` blocks.
- `admin_dashboard.html`: Overview of users, accounts, and activity.
- `admin_profile.html`: Admin personal profile and info.
- `admin_settings.html`: Admin settings dashboard (links to system/email/payment/maintenance).
- `admin_system_settings.html`: Configure core system settings.
- `admin_email_settings.html`: Email server/configuration.
- `admin_payment_settings.html`: Payment gateway, fees, limits.
- `admin_maintenance_mode.html`: Enable/disable site maintenance.

User management
- `admin_users.html`: List of all users.
- `admin_user_details.html`: Individual user info and profile. (Now extends `base.html`.)
- `admin_user_accounts.html`: View/manage user accounts.
- `admin_user_assets.html`: User assets, investments, wallets.
- `admin_user_investments.html`: View/manage user investments.
- `admin_user_loans.html`: User loan management.
- `admin_user_cards.html`: Manage user cards.
- `admin_user_wallets.html`: Wallet balances and transactions.

KYC management
- `admin_kyc.html`: KYC dashboard overview.
- `admin_kyc_list.html`: List of KYC requests.
- `admin_kyc_review.html`: Review submitted KYC. (Now extends `base.html`.)
- `admin_kyc_details.html`: Individual KYC details.
- `admin_kyc_settings.html`: Configure KYC rules/workflow.

Transactions & funds
- `admin_transactions.html`: All transaction history.
- `admin_transaction_details.html`: Individual transaction. (Now extends `base.html`.)
- `admin_pending_deposits.html`: Pending deposits.
- `admin_pending_withdrawals.html`: Pending withdrawals.
- `admin_submissions.html`: User-submitted requests/forms.
- `admin_fund_user.html`: Fund a user account manually.
- `admin_adjust_balance.html`: Adjust user balances (credits/debits).

Reports & content
- `admin_reports.html`: Financial and system reports.
- `admin_content.html`: Manage site content/pages.

Security & monitoring
- `admin_logs.html`: System logs.
- `admin_activity_monitor.html`: Track user/admin activity.
- `admin_security_center.html`: Security settings, alerts.
- `admin_notifications.html`: Notifications to admins/users.

Admin roles & management
- `admin_roles.html`: Manage roles (admin, moderator, etc.).
- `admin_manage_admins.html`: Create/remove other admins.

Linking Strategy (enforced in `base.html`)
- Sidebar: A consistent sidebar is included in `base.html`. It uses relative links only (e.g. `admin_dashboard.html`, `admin_users.html`).
- Internal linking: All links between admin pages must be relative and point to files inside `private/admin`.
  - Example: `<a href="admin_users.html">Users</a>`
- Child pages: Detailed/child pages should provide a "Back" button to the parent page using the `back_button` block. Example at top of child templates:

```jinja
{% extends "private/admin/base.html" %}
{% block page_title %}User Details{% endblock %}
{% block back_button %}
<a href="admin_users.html" class="btn btn-secondary mb-3">&larr; Back to Users</a>
{% endblock %}
{% block content %}
  ...
{% endblock %}
```

Active Navigation
- To show an active nav item, set a small variable in the child template near the top:

```jinja
{% set nav_active = 'Users' %}
```

Then implement any JS/CSS detection or add conditional classes in `base.html` if desired.

Converting Existing Templates
- Prefer converting full standalone admin pages to extend `base.html` (see examples above). This keeps layout consistent and avoids duplicated header/footer.
- The repository already contains a mixture of standalone pages and Jinja templates; start by converting high-traffic pages (`users`, `kyc`, `transactions`, `settings`) then the rest.

Next Steps
- Optionally convert remaining admin templates to extend `base.html` and add `nav_active` where needed.
- Implement server-side logic to set `nav_active` automatically (optional).

If you want, I can:
- Convert all remaining admin pages to extend `base.html` in one pass.
- Add `nav_active` support to mark the current section active.
- Add an include fragment for breadcrumbs or micro-actions.

