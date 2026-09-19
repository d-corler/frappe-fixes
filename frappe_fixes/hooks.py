app_name = "frappe_fixes"
app_title = "Frappe Fixes"
app_publisher = "Accro-plongee"
app_description = "Fix for decode_email (Header without .decode) during IMAP sync, and sent/received mislabeling"
app_email = "contact@accro-plongee.fr"
app_license = "mit"

doc_events = {
    "Communication": {
        "before_insert": "frappe_fixes.communication_fix.fix_sent_or_received"
    }
}
