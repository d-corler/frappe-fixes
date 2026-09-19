__version__ = "0.0.3"

from email.header import Header


def _find_owner_class(cls, method_name):
    """Walk the MRO to find which class in the hierarchy actually defines method_name."""
    for klass in cls.__mro__:
        if method_name in klass.__dict__:
            return klass
    return None


def _patch_decode_email():
    """
    Fixes AttributeError: 'Header' object has no attribute 'decode'
    in decode_email (frappe/email/receive.py), which occurs when a header
    (To/From/Cc) contains a badly encoded address (invalid RFC 2047 encoding).

    decode_email is defined on the base `Email` class, not on `InboundMail`
    itself, so we walk the MRO to find and patch the real owner class. This
    also covers subclasses such as Helpdesk's CustomInboundMail, since they
    inherit from InboundMail/Email and don't override decode_email.
    """
    try:
        import frappe.email.receive as receive_module
    except ImportError:
        return

    inbound_mail_cls = getattr(receive_module, "InboundMail", None)
    if inbound_mail_cls is None:
        return

    owner_cls = _find_owner_class(inbound_mail_cls, "decode_email")
    if owner_cls is None:
        return

    original = owner_cls.__dict__["decode_email"]
    original_func = original.__func__ if hasattr(original, "__func__") else original

    def patched_decode_email(email=None):
        if isinstance(email, Header):
            email = str(email)
        return original_func(email)

    owner_cls.decode_email = staticmethod(patched_decode_email)


_patch_decode_email()
