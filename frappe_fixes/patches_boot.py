from email.header import Header

import frappe


def apply():
    try:
        import frappe.email.receive as receive_module
    except ImportError:
        frappe.logger().warning("frappe_fixes: cannot import frappe.email.receive")
        return

    inbound_mail_cls = getattr(receive_module, "InboundMail", None)
    if inbound_mail_cls is None:
        frappe.logger().warning("frappe_fixes: InboundMail class not found, patch not applied")
        return

    original_decode_email = inbound_mail_cls.__dict__.get("decode_email")
    if original_decode_email is None:
        frappe.logger().warning("frappe_fixes: decode_email not found on InboundMail, patch not applied")
        return

    original_func = original_decode_email.__func__ if hasattr(original_decode_email, "__func__") else original_decode_email

    def patched_decode_email(email=None):
        if isinstance(email, Header):
            email = str(email)
        return original_func(email)

    inbound_mail_cls.decode_email = staticmethod(patched_decode_email)
    frappe.logger().info("frappe_fixes: decode_email patch applied")
