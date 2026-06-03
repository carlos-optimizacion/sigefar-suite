from django.shortcuts import render

from .sigefar_catalog import VISIBLE_MODULES, PRINCIPLES, FLOW_STEPS, SUBMODULES


def get_visible_module(slug):
    module = next((item for item in VISIBLE_MODULES if item["slug"] == slug), None)
    if module is None:
        module = next(item for item in VISIBLE_MODULES if item["slug"] == "regulatorio")
    return module


def public_home(request):
    return render(
        request,
        "core/dashboard_public.html",
        {
            "modules": VISIBLE_MODULES,
            "principles": PRINCIPLES,
            "flow_steps": FLOW_STEPS,
        },
    )


def public_module_detail(request, slug):
    module = get_visible_module(slug)
    related_modules = [item for item in VISIBLE_MODULES if item["slug"] != module["slug"]]
    return render(
        request,
        "core/module_public_detail.html",
        {
            "module": module,
            "related_modules": related_modules,
            "submodules": SUBMODULES.get(module["slug"], []),
        },
    )


def public_submodule_index(request, module_slug):
    module = get_visible_module(module_slug)
    return render(
        request,
        "core/submodule_index.html",
        {
            "module": module,
            "submodules": SUBMODULES.get(module["slug"], []),
        },
    )


def public_submodule_detail(request, module_slug, submodule_slug):
    module = get_visible_module(module_slug)
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
