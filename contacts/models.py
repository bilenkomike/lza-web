from wagtail.snippets.models import register_snippet
from django.db import models
from wagtail.models import Page, TranslatableMixin
from wagtail.admin.panels import FieldPanel
from django.shortcuts import render
from django import forms
from .utils import t



@register_snippet
class IncidentReportSubmission(models.Model):
    what_happened = models.TextField()
    where_happened = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)


@register_snippet
class ContactSubmission(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    organisation = models.CharField(max_length=255, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)



class IncidentReportForm(forms.Form):
    what_happened = forms.CharField(widget=forms.Textarea)
    where_happened = forms.CharField()
    name = forms.CharField()
    phone = forms.CharField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["what_happened"].widget.attrs.update({
            "placeholder": t("incident_what_happened", "What happened?"),
            "class": "textarea",
        })
        self.fields["where_happened"].widget.attrs.update({
            "placeholder": t("incident_where_happened", "Where did it happen?"),
            "class": "input",
        })
        self.fields["name"].widget.attrs.update({
            "placeholder": t("incident_name", "Your name"),
            "class": "input",
        })
        self.fields["phone"].widget.attrs.update({
            "placeholder": t("incident_phone", "Your phone number"),
            "class": "input",
        })


class ContactForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    organisation = forms.CharField(required=False)
    message = forms.CharField(widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["first_name"].widget.attrs.update({
            "placeholder": t("contact_first_name", "Name"),
            "class": "input",
        })
        self.fields["last_name"].widget.attrs.update({
            "placeholder": t("contact_last_name", "Surname"),
            "class": "input",
        })
        self.fields["email"].widget.attrs.update({
            "placeholder": t("contact_email", "Email"),
            "class": "input",
        })
        self.fields["organisation"].widget.attrs.update({
            "placeholder": t("contact_organisation", "Organisation (optional)"),
            "class": "input",
        })
        self.fields["message"].widget.attrs.update({
            "placeholder": t("contact_message", "Message"),
            "class": "textarea",
        })


@register_snippet
class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email



class IncidentReportPage(Page, TranslatableMixin):
    introduction = models.TextField(blank=True)
    success_message = models.TextField(blank=True, default="Thank you. Information sent.")

    content_panels = Page.content_panels + [
        FieldPanel("introduction"),
        FieldPanel("success_message"),
    ]

    parent_page_types = ["home.Home"]
    subpage_types = []

    def serve(self, request):

        if request.method == "POST":
            form = IncidentReportForm(request.POST)
            if form.is_valid():
                IncidentReportSubmission.objects.create(**form.cleaned_data)
                return render(request, self.template, {
                    "page": self,
                    "form": IncidentReportForm(),
                    "success": True,
                })
        else:
            form = IncidentReportForm()

        return render(request, self.template, {
            "page": self,
            "form": form,
        })


class ContactPage(Page, TranslatableMixin):
    introduction = models.TextField(blank=True)
    success_message = models.TextField(blank=True, default="Thank you. Message sent.")

    content_panels = Page.content_panels + [
        FieldPanel("introduction"),
        FieldPanel("success_message"),
    ]

    parent_page_types = ["home.Home"]
    subpage_types = []

    def serve(self, request):

        if request.method == "POST":
            form = ContactForm(request.POST)
            if form.is_valid():
                ContactSubmission.objects.create(**form.cleaned_data)
                return render(request, self.template, {
                    "page": self,
                    "form": ContactForm(),
                    "success": True,
                })
        else:
            form = ContactForm()

        return render(request, self.template, {
            "page": self,
            "form": form,
        })
