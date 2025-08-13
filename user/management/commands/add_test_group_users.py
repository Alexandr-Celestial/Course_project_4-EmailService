from django.core.management import BaseCommand, call_command


class Command(BaseCommand):
    help = 'Добавляет данные из фикстуры в БД'

    def handle(self, *args, **kwargs):
        call_command('loaddata', 'fixture_groups_permissions.json')
        self.stdout.write(self.style.SUCCESS('Данные успешно добавлены'))