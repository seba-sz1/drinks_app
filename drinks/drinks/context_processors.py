def base_template_context(request):
    is_homepage = request.path == '/'
    return {'is_homepage': is_homepage}

