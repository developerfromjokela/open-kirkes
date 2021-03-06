#  Copyright (c) 2020 openKirkes, developed by Developer From Jokela

from django.core.management.base import BaseCommand

from openKirkesAuth.models import ApiUserToken
from openKirkesConnector.fcm_client import FCMClient


class Command(BaseCommand):
    help = 'Pushes refresh request to devices'

    def handle(self, *args, **options):
        fcm_client = FCMClient()
        users_pushed = 0
        for user in ApiUserToken.objects.all():
            push_token = user.push_key
            if push_token is not None:
                if push_token:
                    push_result = fcm_client.sendPush(push_token, {
                        "data_refresh": True,
                        "user": user.token
                    })
                    if not push_result.is_error():
                        if push_result.is_sent():
                            users_pushed += 1
                    else:
                        self.stdout.write(self.style.WARNING('Failed to push: "%s"' % str(push_result.get_exception())))
        self.stdout.write(self.style.SUCCESS('Successfully pushed "%s" user(s)' % str(users_pushed)))
