from django.shortcuts import render

from .sigefar_submodules import SUBMODULES
from .views import MODULES


def get_module(module_slug):
    selected_module = next((module for module in MODULES if module["slug"] == module_slug), None)
    if selected_module is None:
        selected_module = next(module for module in MODULES if module["slug"] == "qms")
    return selected_module


def module_detail_with_submodules(request, slug):
    module = get_module(slug)
    related_modules = [item for item in MODULES if item["slug"] != module["slug"]]
    return render(
        request,
        "core/module_detail.html",
        {
            "module": module,
            "related_modules": related_modules,
            "submodules": SUBMODULES.get(module["slug"], []),
        },
    )


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
