from django.shortcuts import render
from django.http import JsonResponse
from .forms import NewsletterForm

def newsletter_subscribe(request):
    if request.method == "POST":
        form = NewsletterForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse(
                {"success": True, "message": "Subscribed successfully."}
            )
        else:
            return JsonResponse(
                {"success": False, "errors": form.errors},
                status=400,
            )

    return JsonResponse({"success": False}, status=405)