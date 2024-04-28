from django.db import models
from django.utils.translation import gettext_lazy as _

from ckeditor.fields import RichTextField

from services.abstract_models import TimeStampedModel
from services.custom_fields import CustomSlugField


class Category(TimeStampedModel):
    slug = CustomSlugField(
        verbose_name=_("Slug"),
        source_field="title",
        symbol_mapping="default",
        unique=True,
        editable=True,
    )
    
    title = models.CharField(
        max_length=300, verbose_name="Kateqoriyanın adı"
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Məhsul kateqoriyası")
        verbose_name_plural = _("Məhsul kateqoriyaları")


class Product(TimeStampedModel):
    slug = CustomSlugField(
        verbose_name=_("Slug"),
        source_field="title",
        symbol_mapping="default",
        unique=True,
        editable=True,
    )

    title = models.CharField(
        verbose_name=_("Başlıq"),
        max_length=300
    )

    price = models.FloatField(
        default=0,
        verbose_name="Məhsulun qiyməti"
    )

    category = models.PositiveIntegerField(
        verbose_name="Məhsulun Kateqoriyası"
    )

    text = RichTextField(
        verbose_name="Məhsul haqqında mətn"
    )

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = _("Məhsul")
        verbose_name_plural = _("Məhsullar")
