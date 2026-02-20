from django.db import models
from wagtail import blocks
from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField
from wagtail.models import Page, TranslatableMixin
from wagtail.images.blocks import ImageChooserBlock
from wagtail.snippets.models import register_snippet
from wagtail.snippets.blocks import SnippetChooserBlock
from django.shortcuts import render
from django.core.paginator import Paginator
from wagtail.search import index
from wagtail.images import get_image_model_string



@register_snippet
class Author(models.Model):
    name = models.CharField(max_length=255)
    photo = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    panels = [
        FieldPanel("name"),
        FieldPanel("photo"),
    ]

    def __str__(self):
        return self.name


class ImageBlock(blocks.StructBlock):
    image = ImageChooserBlock()
    caption = blocks.CharBlock(required=False)

    class Meta:
        icon = "image"


class StoryBlock(blocks.StreamBlock):
    heading = blocks.CharBlock()
    paragraph = blocks.RichTextBlock()
    image = ImageBlock()
    advert = SnippetChooserBlock("home.Advert")


@register_snippet
class NewsCategory(TranslatableMixin, models.Model):
    name = models.CharField(max_length=255)

    panels = [
        FieldPanel("name"),
    ]

    def __str__(self):
        return self.name


class NewsPage(Page):
    publication_date = models.DateField(null=True, blank=True)
    author = models.ForeignKey(
        Author,  # change app name if needed
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="news_posts",
    )
    image = models.ForeignKey(
        "wagtailimages.Image", on_delete=models.SET_NULL, null=True
    )
    body = StreamField(StoryBlock())
    category = models.ForeignKey(
        NewsCategory, on_delete=models.SET_NULL, null=True, related_name="blog_posts"
    )

    content_panels = Page.content_panels + [
        FieldPanel("publication_date"),
        FieldPanel("author"),
        FieldPanel("image"),
        FieldPanel("body"),
        FieldPanel("category"),
    ]

    search_fields = Page.search_fields + [
        index.SearchField("title"),
        index.SearchField("body"),
    ]

    parent_page_types = ["news.NewsIndexPage"]


class NewsIndexPage(Page):
    advert = models.ForeignKey(
        "home.Advert",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    content_panels = Page.content_panels + [
        FieldPanel("advert"),
    ]
    max_count = 1
    parent_page_types = ["home.Home"]

    def get_context(self, request):
        context = super().get_context(request)

        news_qs = NewsPage.objects.descendant_of(self).live().public()

        search_query = request.GET.get("q")
        if search_query:
            news_qs = news_qs.search(search_query)  # relevance order
        else:
            news_qs = news_qs.order_by("-publication_date")

        paginator = Paginator(news_qs, 2)
        page_number = request.GET.get("page")

        context["news"] = paginator.get_page(page_number)
        context["search_query"] = search_query

        return context


