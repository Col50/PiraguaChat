from django.urls import path
from .views.langchain_agent_view import LangchainAgentView
from .views.whats_app_webhook_view import WhatsAppWebhookView
from .views.ocr_view import WhatsAppOCRView

urlpatterns = [
    path("agent/", LangchainAgentView.as_view(), name="langchain-agent"),
    path("whatsapp/webhook/", WhatsAppWebhookView.as_view(), name="whatsapp-webhook"),
    path("whatsapp/ocr/", WhatsAppOCRView.as_view(), name="whatsapp-webhook-ocr"),
]
