from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting
from wagtail.snippets.models import register_snippet
from wagtail.models import Page, TranslatableMixin
from news.models import NewsPage



@register_setting
class GlobalSiteSettings(BaseSiteSetting):
    site_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=50)
    about = models.TextField(
        max_length=400,
        default="",
    )
    organization_name = models.CharField(
        max_length=255,
        default="",
    )
    country = models.CharField(
        max_length=150,
        default="",
    )
    city = models.CharField(
        max_length=150,
        default="",
    )
    address = models.CharField(
        max_length=255,
        default="",
    )
    postal_code = models.CharField(
        max_length=20,
        default="",
    )

    panels = [
        FieldPanel('site_name'),
        FieldPanel('email'),
        FieldPanel('phone'),
        FieldPanel('about'),
        FieldPanel("organization_name"),
        FieldPanel("country"),
        FieldPanel("city"),
        FieldPanel("address"),
        FieldPanel("postal_code"),
    ]


@register_snippet
class Advert(models.Model):
    name = models.CharField(max_length=255)
    image = models.ForeignKey(
        'wagtailimages.Image',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='+'
    )
    url = models.URLField()

    panels = [
        FieldPanel('name'),
        FieldPanel('image'),
        FieldPanel('url'),
    ]

    def __str__(self):
        return self.name



class Home(Page):
    page_title = models.CharField(max_length=150)
    advert = models.ForeignKey(
        "home.Advert",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    content_panels = Page.content_panels + [
        FieldPanel("page_title"),
        FieldPanel("advert"),
    ]
    parent_page_types = ["wagtailcore.Page"]

    def get_context(self, request):
        context = super().get_context(request)
        qs = (
            NewsPage.objects
            .live()
            .public()
            .filter(locale=self.locale)
            .order_by("-publication_date")
        )
        context["last_post"] = qs.first()
        context["latest_posts"] = qs[0:7]

        return context