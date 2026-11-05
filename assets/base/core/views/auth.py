from django.shortcuts import redirect, render

from core.data.common import USERS


def login(request):
    if request.method == "POST":
        request.session["user"] = request.POST.get("profil", next(iter(USERS)))
        return redirect("dashboard")
    return render(request, "core/login.html", {"profiles": list(USERS.values())})


def logout(request):
    request.session.flush()
    return redirect("login")
