import re


def normalize_nicaragua_whatsapp(raw: str) -> str:
    digits = re.sub(r'\D', '', raw or '')
    if len(digits) == 8:
        return f'505{digits}'
    if len(digits) == 11 and digits.startswith('505'):
        return digits
    raise ValueError('WhatsApp inválido. Usa 8 dígitos o 505 + 8 dígitos.')
