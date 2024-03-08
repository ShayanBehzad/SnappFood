from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.core.validators import MinValueValidator, RegexValidator
from django.utils.translation import gettext_lazy as _



class UserRoleMixin(models.Model):
    SELLER = 'seller'
    CUSTOMER = 'customer'
    ROLE_CHOICES = [
        (SELLER, 'Seller'),
        (CUSTOMER, 'Customer'),
    ]
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    phone_regex = RegexValidator(
        regex=r'^(0|0098|\+98)9(0[1-5]|[1 3]\d|2[0-2]|98)\d{7}$',
        message="Phone number must be entered in the format: '+989031234567'."
    )
    phone = models.CharField(validators=[phone_regex], max_length=17, blank=True, default='')

    
    class Meta:
        abstract = True

class User(UserRoleMixin, AbstractUser):
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_('The groups this user belongs to.'),
        related_name='custom_user_set',  # Add a related_name argument
        related_query_name='custom_user',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name='custom_user_set',  # Add a related_name argument
        related_query_name='custom_user',
    )