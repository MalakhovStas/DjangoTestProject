"""Модуль реализации инструментов для обработки команды - python manage.py parse <path>"""

from django.core.management.base import BaseCommand
from django.core.management.color import color_style

from parser.models import LogData
from parser.services import ParserService
from config.exceptions import GenericException


class Command(BaseCommand):
    """Класс описывающий логику при вызове команды - python manage.py parse <path>"""
    help = 'Command to start parsing logs from a remote file'
    output_transaction = True
    requires_migrations_checks = True
    missing_args_message = color_style(True).ERROR(
        'The path to the file is not specified, the command '
        'should be of the form - python manage.py parse <path>'
    )

    def add_arguments(self, parser):
        """Метод добавления аргументов к команде"""
        parser.add_argument(
            "url",
            nargs="+",
            type=str,
            help="Argument for passing the remote path to the log file"
        )

    def handle(self, *args, **options):
        """Метод обрабатывающий команду - python manage.py parse <path>"""
        try:
            result = ParserService(options["url"][0])()
            pre = LogData.objects.count()
            LogData.objects.bulk_create(result.results, ignore_conflicts=True)
            post = LogData.objects.count()
            self.stdout.write(
                self.style.SUCCESS(
                    f"File parsing result:"
                    f"\n\tlogs received: {result.succeeded}"
                    f"\n\tlog parsing errors: {result.errors}"
                    f"\n\tsaved in DB: {post - pre}"
                    f"\n\tuniqueness error, number of unsaved logs: {result.count - (post - pre)}"
                )
            )
        except GenericException as exc:
            self.stderr.write(self.style.ERROR(str(exc)))
