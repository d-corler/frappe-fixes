# Frappe fixes

## Email

`builtins.AttributeError: 'Header' object has no attribute 'decode'`

Edit `InboundMail.decode_email` (frappe/email/receive.py) to fix this issue.

## To install

    bench get-app https://github.com/d-corler/frappe-fixes
    bench --site erp.local install-app frappe_fixes
    bench --site erp.local migrate
