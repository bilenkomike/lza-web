from django.db import models
from wagtail.models import Page, Orderable
from wagtail.fields import StreamField, RichTextField
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.snippets.models import register_snippet
from django.forms import CheckboxSelectMultiple
from modelcluster.fields import ParentalKey


class ImageBlock(blocks.StructBlock):
    image = ImageChooserBlock()
    caption = blocks.CharBlock(required=False)

    class Meta:
        icon = "image"


class AboutSectionBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=True, max_length=255)
    subtext = blocks.CharBlock(required=False, max_length=255)
    text = blocks.RichTextBlock(required=True)
    image = ImageBlock()
    image_placement = blocks.ChoiceBlock(
        choices=[("left", "Left"), ("right", "Right")],
        default="left"
    )

    class Meta:
        template = "about/section_block.html"
        icon = "image"
        label = "About Section"


@register_snippet
class TeamMember(models.Model):
    name = models.CharField(max_length=255)
    position = models.CharField(max_length=255, blank=True)
    company_name = models.CharField(max_length=50)
    image = models.ForeignKey(
        "wagtailimages.Image", on_delete=models.SET_NULL, null=True
    )

    panels = [
        FieldPanel("name"),
        FieldPanel("position"),
        FieldPanel("company_name"),
        FieldPanel("image"),
    ]

    def __str__(self):
        return self.name


class AboutPageTeamMember(Orderable):
    page = ParentalKey("about.AboutPage", related_name="team_members")
    name = models.CharField(max_length=255)
    position = models.CharField(max_length=255, blank=True)
    image = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
    )
    company_name = models.CharField(max_length=50)


class AboutPage(Page):
    top_description = RichTextField(blank=True)
    sections = StreamField(
        [("section", AboutSectionBlock())],
        blank=True,
    )
    team_title = models.CharField(
        max_length=150,
    )

    content_panels = Page.content_panels + [
        FieldPanel("top_description"),
        FieldPanel("sections"),
        FieldPanel("team_title"),
        InlinePanel("team_members", label="Team Members"),
    ]

    max_count = 1
    parent_page_types = ["home.Home"]