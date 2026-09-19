import frappe


def fix_sent_or_received(doc, method):
    """
    Frappe's IMAP receive pipeline hardcodes sent_or_received='Received'
    for every fetched message, regardless of the source IMAP folder
    (see frappe/email/receive.py). This means messages pulled from the
    'Sent' folder are mislabeled as 'Received'.

    This hook runs before a Communication is inserted and flips
    sent_or_received to 'Sent' when the sender matches the email
    account's own address, since that reliably indicates a message
    the account owner sent (regardless of which folder it came from).
    """
    if doc.communication_medium != "Email":
        return

    if not doc.sender or not doc.email_account:
        return

    account_email = frappe.db.get_value("Email Account", doc.email_account, "email_id")
    if account_email and doc.sender.strip().lower() == account_email.strip().lower():
        doc.sent_or_received = "Sent"
