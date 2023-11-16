from django.core.validators import RegexValidator


class SKUValidator(RegexValidator):
    regex = '^[a-zA-Z0-9\-\_]{6,20}$'
    message = 'SKU must be alphanumeric with 6 to 20 characters'
    code = 'invalid_sku '


validate_sku = SKUValidator()
