from django.shortcuts import render

from .sigefar_submodules import SUBMODULES
from .views import MODULES


def get_module(module_slug):
    selected_module = next((module for module in MODULES if module["slug"] == module_slug), None)
    if selected_module is None:
        selected_module = next(module for module in MODULES if module["slug"] == "qms")
    return selected_module


def submodule_detail(request, module_slug, submodule_slug):
    module = get_module(module_slug)
    submodules = SUBMODULES.get(module["slug"], [])
    submodule = next((item for item in submodules if item["slug"] == submodule_slug), None)

    if submodule is None and submodules:
        submodule = submodules[0]

    return render(
        request,
        "core/submodule_detail.html",
        {
            "module": module,
            "submodule": submodule,
            "submodules": submodules,
        },
    )
