from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework_jwt.settings import api_settings


#@receiver(post_save, sender=settings.AUTH_USER_MODEL)
#def get_token(self, sender):
    #jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    #jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
    #payload = jwt_payload_handler(sender)
    #token = jwt_encode_handler(payload)
    #return token



