from django.shortcuts import render

from .sigefar_catalog import FLOW_STEPS, PRINCIPLES, SUBMODULES, VISIBLE_MODULES


def get_visible_module_v2(slug):
    module = next((item for item in VISIBLE_MODULES if item["slug"] == slug), None)
    if module is None:
        module = next(item for item in VISIBLE_MODULES if item["slug"] == "core")
    return module


def build_visual_submodules(module):
    configured = SUBMODULES.get(module["slug"], [])
    if configured:
        return configured
    visual_items = []
    for index, name in enumerate(module.get("componentes", []), start=1):
        slug = name.lower().replace(" ", "-").replace(",", "").replace("/", "-")
        visual_items.append(
            {
                "slug": slug,
                "nombre": name,
                "descripcion": f"Herramienta funcional para gestionar {name.lower()} dentro de {module['nombre']}.",
                "alcance": f"Mantiene el alcance del módulo {module['codigo']} sin duplicar funciones de Core, Regulatorio, Calidad u otros módulos.",
                "acciones": ["Registrar información", "Consultar trazabilidad", "Adjuntar evidencia", "Controlar estado"],
                "exclusiones": module.get("principios", ["No duplica funciones de otros módulos"]),
                "admin_url": "/admin/",
            }
        )
    return visual_items


def public_home_v2(request):
    return render(
        request,
        "core/dashboard_public_core.html",
        {
            "modules": VISIBLE_MODULES,
            "principles": PRINCIPLES,
            "flow_steps": FLOW_STEPS,
        },
    )


def public_module_detail_v2(request, slug):
    module = get_visible_module_v2(slug)
    related_modules = [item for item in VISIBLE_MODULES if item["slug"] != module["slug"]]
    return render(
        request,
        "core/module_public_detail.html",
        {
            "module": module,
            "related_modules": related_modules,
            "submodules": build_visual_submodules(module),
        },
    )


def public_submodule_index_v2(request, module_slug):
    module = get_visible_module_v2(module_slug)
    return render(request, "core/submodule_index.html", {"module": module, "submodules": build_visual_submodules(module)})


def public_submodule_detail_v2(request, module_slug, submodule_slug):
    module = get_visible_module_v2(module_slug)
    submodules = build_visual_submodules(module)
    submodule = next((item for item in submodules if item["slug"] == submodule_slug), None)
    if submodule is None and submodules:
        submodule = submodules[0]
    return render(request, "core/submodule_detail.html", {"module": module, "submodule": submodule, "submodules": submodules})
