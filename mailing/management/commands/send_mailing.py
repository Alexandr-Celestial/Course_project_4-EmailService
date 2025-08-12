from django.core.management import BaseCommand
from django.test.client import RequestFactory
from mailing.models import Mailing
from mailing.views import sending_mailing


class Command(BaseCommand):
    help = 'Отправляет выбранную рассылку.'

    def add_arguments(self, parser):
        parser.add_argument('mailing_id', type=int, help='PK рассылки')

    def handle(self, *args, **options):
        mailing_id = options['mailing_id']
        mailing = Mailing.objects.get(pk=mailing_id)
        factory = RequestFactory()
        request = factory.get('/')
        response = sending_mailing(request, mailing.pk)
        self.stdout.write(f'Рассылка "{mailing.message.theme}" успешно запущена.')