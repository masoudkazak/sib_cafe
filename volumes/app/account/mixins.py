from django.contrib.auth.mixins import AccessMixin


class SuperuserRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class IsOwnerOrSuperuser(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        
        if self.kwargs["username"] == request.user.username:
            return super().dispatch(request, *args, **kwargs)
        else:
            return self.handle_no_permission()
        