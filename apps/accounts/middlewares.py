class UserTypeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Добавляем заголовок с типом пользователя
        if hasattr(request, 'user'):
            if hasattr(request.user, 'is_guest') and request.user.is_guest:
                response['X-User-Type'] = 'guest'
            elif request.user.is_authenticated:
                response['X-User-Type'] = 'authenticated'
            else:
                response['X-User-Type'] = 'anonymous'

        return response


class GuestConsentMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if self.needs_consent_banner(request):
            # Добавляем флаг в контекст для фронтенда
            if hasattr(request, 'need_consent'):
                request.need_consent = True

        return response

    def needs_consent_banner(self, request):
        # Проверяем, нужно ли показывать баннер согласия
        if request.path.startswith('/admin/'):
            return False

        # Проверяем cookies/сессию на наличие согласия
        consent_given = request.session.get('guest_consent_given')
        if consent_given:
            return False

        return True
