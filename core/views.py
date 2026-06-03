from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


@login_required
def panel(request):
    """Vista heredada.

    El panel interno dejó de ser el centro de navegación. La experiencia principal
    de SIGEFAR Suite se concentra en el ecosistema modular visual y en el admin.
    """
    return redirect("home")


# Alias temporal para compatibilidad con versiones previas.
dashboard = panel
