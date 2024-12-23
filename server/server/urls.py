from django.contrib import admin
from django.urls import path, include
from events.urls import router

urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api/v1/auth/', include('authentication.urls'))
]
