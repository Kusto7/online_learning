from django.core.management import BaseCommand

from education.models import Payment
from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        Pay_1 = Payment.objects.create(
            user=User.objects.get(email='admin@gmail.com'),
            course=1,
            amount=10500,
            method='Наличные'

        )
        Pay_1.save()

        Pay_2 = Payment.objects.create(
            user=User.objects.get(email='admin21@gmail.com'),
            course=2,
            amount=9000,
            method='Перевод'

        )
        Pay_2.save()
