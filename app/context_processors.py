from wagtail.models import Page, Site, Locale

def navigation_pages(request):
    site = Site.find_for_request(request) or Site.objects.first()
    root = site.root_page.specific

    # Default pages by slug

    news_page = root.get_children().filter(slug="news").first()
    about_page = root.get_children().filter(slug="about-us").first()
    contact_page = root.get_children().filter(slug="contacts").first()
    incident_report_page = root.get_children().filter(slug="incident-report").first()

    # Get the current locale object from language code
    lang_code = getattr(request, "LANGUAGE_CODE", "en")
    try:
        locale = Locale.objects.get(language_code=lang_code)
    except Locale.DoesNotExist:
        locale = Locale.objects.get(language_code="en")

    # Resolve translations for the current locale
    home_page = root.get_translation_or_none(locale) or root

    if news_page:
        news_page = news_page.get_translation_or_none(locale) or news_page
    if about_page:
        about_page = about_page.get_translation_or_none(locale) or about_page
    if contact_page:
        contact_page = contact_page.get_translation_or_none(locale) or contact_page
    if incident_report_page:
        incident_report_page = incident_report_page.get_translation_or_none(locale) or incident_report_page

    return {
        "home_page": home_page,
        "news_page": news_page,
        "about_page": about_page,
        "contact_page": contact_page,
        "incident_report_page": incident_report_page,
    }
