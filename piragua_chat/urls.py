from django.urls import path
from .views.views import LangchainAgentView

urlpatterns = [
    path("agent/", LangchainAgentView.as_view(), name="langchain-agent"),
]
