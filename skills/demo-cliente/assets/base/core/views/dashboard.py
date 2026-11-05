from django.shortcuts import render


def home(request):
    # Le lead remplace ce corps : KPI, graphiques et listes tirés des modules (core.data.*).
    return render(request, "core/dashboard.html", {})
