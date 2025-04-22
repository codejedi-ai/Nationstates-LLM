from django.shortcuts import render, redirect
from django.apps import apps


def index(request):
    """Process images uploaded by users"""

    app_name = "GreatDictatorAI"
    context = {
        'app_name': app_name,
    }
    return render(request, 'base.html' , context = context)