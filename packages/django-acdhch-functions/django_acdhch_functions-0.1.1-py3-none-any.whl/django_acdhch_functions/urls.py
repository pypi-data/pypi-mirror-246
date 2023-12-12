from django.urls import path

from . import views

app_name = "django_acdhch_functions"

urlpatterns = [path("imprint2", views.Imprint.as_view(), name="imprint")]
