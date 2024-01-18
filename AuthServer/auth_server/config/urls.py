"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import grpc

from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from concurrent.futures import ThreadPoolExecutor


from ._credentials import SERVER_CERTIFICATE_KEY, SERVER_CERTIFICATE
from modules.main.handlers import grpc_handlers as auth_grpc_handler
from modules.main.interceptors import AuthServerInterceptor



_PORT = 50051
_SERVER_ADDR_TEMPLATE = "localhost:%d"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

def grpc_handlers(server):
    interceptors = AuthServerInterceptor()
    server = grpc.server(
        ThreadPoolExecutor(max_workers=1),
        interceptors=[interceptors]
    )
    
    # Loading credentials
    server_credentials = grpc.ssl_server_credentials(
        (
            (
                SERVER_CERTIFICATE_KEY,
                SERVER_CERTIFICATE,
            ),
        )
    )
    
    auth_grpc_handler(server)

    server.add_secure_port(_SERVER_ADDR_TEMPLATE % _PORT, server_credentials)
    server.start()
    server.wait_for_termination()

