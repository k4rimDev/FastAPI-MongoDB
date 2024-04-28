import uuid
import unicodedata
from django.db import models
from django.core import checks
from django.utils.translation import gettext_lazy as _


class CustomSlugField(models.SlugField):
    """
    Custom Django SlugField with additional features.
    """

    DEFAULT_SYMBOL_MAPPING = (
        # Azerbaijani alphabet
        (" ", "-"),
        ("/", "-"),
        (".", "-"),
        ("(", "-"),
        (")", "-"),
        (",", "-"),
        ("!", ""),
        ("?", ""),
        ("'", "-"),
        ('"', "-"),
        ("ə", "e"),
        ("ı", "i"),
        ("ö", "o"),
        ("ğ", "g"),
        ("ü", "u"),
        ("ş", "s"),
        ("ç", "c"),
        ("%", ""),
        ("$", ""),
        ("=", ""),
        (":", ""),
    )

    def __init__(self, source_field: str = None,  overwrite: bool = False, symbol_mapping: list = None, allow_manual: bool = False, *args, **kwargs):
        """
        Initialize custom slug field with optional parameters.

        :param source_field: The source field to generate the slug from.
        :param overwrite: If True, overwrite the existing slug when saving.
        :param symbol_mapping: Custom symbol mapping for slug generation.
        :param allow_manual: If True, allow manual input for the slug.
        """
        self.source_field = source_field
        self.overwrite = overwrite
        # Set the symbol_mapping based on the provided value or use the default if "default" is specified
        self.symbol_mapping = self.DEFAULT_SYMBOL_MAPPING if symbol_mapping == "default" else symbol_mapping
        self.allow_manual = allow_manual
        super().__init__(*args, **kwargs)

    def slugify(self, title, allow_unicode=False):
        value = title.strip().lower()

        for before, after in self.DEFAULT_SYMBOL_MAPPING:
            value = value.replace(before, after)

        if allow_unicode:
            value = unicodedata.normalize("NFKC", value)
        else:
            value = (
                unicodedata.normalize("NFKD", value)
                .encode("ascii", "ignore")
                .decode("ascii")
            )

        return value

    def pre_save(self, model_instance, add):
        # Generate or overwrite the slug based on source_field, symbol_mapping, and manual input settings
        if (not getattr(model_instance, self.attname) or self.overwrite) and self.source_field and not self.allow_manual:
            source_value = getattr(model_instance, self.source_field)

            if self.symbol_mapping:
                # Replace symbols based on symbol mapping
                source_value = self.replace_symbols(source_value)

            slug_value = self.generate_slug(source_value, model_instance)
            setattr(model_instance, self.attname, slug_value)

        return super().pre_save(model_instance, add)

    def replace_symbols(self, source_value):
        # Replace symbols in the source value with corresponding replacements
        for symbol, replacement in self.symbol_mapping:
            source_value = source_value.replace(symbol, replacement)

        return source_value

    def generate_slug(self, source_value, model_instance):
        # Generate a slug from the source value using the configured allow_unicode setting
        slug_value = self.slugify(source_value, allow_unicode=self.allow_unicode)

        # Generate a unique slug from the source value
        if self.unique:
            unique_slug = slug_value
            counter = 1

            # Create a unique slug with a single database query
            while model_instance.__class__.objects.filter(**{self.attname: unique_slug}).exclude(pk=model_instance.pk).exists():
                unique_slug = f"{slug_value}-{counter}"
                counter += 1

            slug_value = unique_slug

        # If a valid slug is generated, return it; otherwise, fallback to a UUID
        return slug_value or self.slugify(str(uuid.uuid4()))

    def check(self, **kwargs):
        # Perform additional checks and return a list of warnings and errors.
        return [
            *super().check(**kwargs),
            *self._check_allow_manual(),
            *self._check_symbol_mapping(),
        ]

    def _check_allow_manual(self):
        # If the allow_manual property is True and other relevant properties are set, raise a warning
        if self.allow_manual and (self.source_field or self.overwrite or self.symbol_mapping):
            return [
                checks.Warning(
                    "allow_manual is True, so source_field, overwrite, and symbol_mapping are ineffective.",
                    obj=self,
                    id="fields.W001",
                )
            ]
        return []

    def _check_symbol_mapping(self):
        # Check if 'symbol_mapping' is correctly formatted as a list of tuples with two elements each
        if self.symbol_mapping is not None:
            if not all(isinstance(item, tuple) and len(item) == 2 for item in self.symbol_mapping):
                return [
                    checks.Error(
                        "symbol_mapping should contain tuples with exactly two elements for each item.",
                        hint="Each tuple should be in the form (symbol, replacement).",
                        obj=self,
                        id="fields.E001",
                    )
                ]
        return []
