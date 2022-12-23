from rest_framework import permissions
from rest_framework.views import Request, View

class IsAdminToGet(permissions.BasePermission):
    def has_permission(self, request: Request, view: View) -> bool:   
       
        if request.method == "GET":
            return request.user.is_superuser

        return True
        
class IsAdminOrOwner(permissions.BasePermission):
    def has_permission(self, request: Request, view: View) -> bool:   
       
        param_id = view.kwargs['pk']
        if request.method == "GET" or request.method == "PATCH":
            if param_id is request.user.id:
                return True

        return request.user.is_superuser