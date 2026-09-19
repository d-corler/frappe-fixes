__version__ = "0.0.2"

from email.header import Header


def _patch_decode_email():
    """
    Fixes AttributeError: 'Header' object has no attribute 'decode'
    in InboundMail.decode_email (frappe/email/receive.py), which occurs
    when a header (To/From/Cc) contains a badly encoded address (invalid
    RFC 2047 encoding).
    """
    try:
        import frappe.email.receive as receive_module
    except ImportError:
        return

    inbound_mail_cls = getattr(receive_module, "InboundMail", None)
    if inbound_mail_cls is None:
        return

    original = inbound_mail_cls.__dict__.get("decode_email")
    if original is None:
        return

    original_func = original.__func__ if hasattr(original, "__func__") else original

    def patched_decode_email(email=None):
        if isinstance(email, Header):
            email = str(email)
        return original_func(email)

    inbound_mail_cls.decode_email = staticmethod(patched_decode_email)


_patch_decode_email()
