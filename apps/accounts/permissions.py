from rest_framework import permissions


class AllowGuests(permissions.BasePermission):
    """
    Разрешает доступ как аутентифицированным пользователям, так и гостям
    """
    def has_permission(self, request, view):
        # Если пользователь - гость (имеет guest_id), считаем его аутентифицированным
        return bool(request.user and (
            request.user.is_authenticated or 
            hasattr(request.user, 'guest_id')
        ))
