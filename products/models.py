from django.db import models
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    parent = models.ForeignKey("self", verbose_name=_("parent"), blank=True, null=True, on_delete=models.CASCADE)
    title = models.CharField(verbose_name=_("title"), max_length=50)
    description = models.TextField(_("description"), blank=True)
    avatar = models.ImageField(_("avatar"), blank=True, upload_to='products/')
    is_enable = models.BooleanField(_("is_enable"), default=True)
    created = models.DateTimeField(_("created category"), auto_now_add=True)
    updated = models.DateTimeField(_("updated category"), auto_now=True)

    class Meta:
        db_table = "categories"
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")


class Product(models.Model):
    title = models.CharField(verbose_name=_("title"), max_length=50)
    description = models.TextField(_("description"), blank=True)
    avatar = models.ImageField(_("avatar"), blank=True, upload_to='categories/')
    is_enable = models.BooleanField(_("is_enable"), default=True)
    created = models.DateTimeField(_("created product"), auto_now_add=True)
    updated = models.DateTimeField(_("updated product"), auto_now=True)
    categories = models.ManyToManyField('Category', verbose_name=_("categories"), blank=True)

    class Meta:
        db_table = "products"
        verbose_name = _("Product")
        verbose_name_plural = _("Products")


class File(models.Model):
    product = models.ForeignKey('Product', verbose_name=_("product"), on_delete=models.CASCADE)
    title = models.CharField(verbose_name=_("title"), max_length=50)
    description = models.TextField(_("description"), blank=True)
    file = models.FileField(_("file"), blank=True, upload_to='files/%Y/%m/%d/')
    is_enable = models.BooleanField(_("is_enable"), default=True)
    created = models.DateTimeField(_("created category"), auto_now_add=True)
    updated = models.DateTimeField(_("updated category"), auto_now=True)

    class Meta:
        db_table = "files"
        verbose_name = _("File")
        verbose_name_plural = _("Files")
