from rest_framework.permissions import BasePermission


# пользователь редактирует свой профиль
class IsProfileUser(BasePermission):
    message = "Вы не можете редактировать чужой профиль"

    def has_permission(self, request, view):
        return request.user == view.get_object()


# # пользователь относится к группе модераторов
# class IsModerator(BasePermission):
#     message = "Вы не состоите в группе модераторов"
#
#     def has_permission(self, request, view):
#         return request.user.groups.filter(name='moderator').exists()


# # пользователь не относится к группе модераторов
# class IsNotModerator(BasePermission):
#     def has_permission(self, request, view):
#         return not request.user.groups.filter(name='moderator').exists()


# class IsOwner(BasePermission):
#     def has_object_permission(self, request, view, obj):
#         if request.user == obj.owner:
#             return True
#         return False


# class IsModerator(BasePermission):
#     def has_permission(self, request, view):
#         if request.user.role == UserRole.MODERATOR:
#             return True
#         return False
