from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from tickets.models import Ticket


class Command(BaseCommand):
    help = "Checks for Open tickets that have been unaccepted for too long, and flags them as overdue."

    def handle(self, *args, **kwargs):
        overdue_minutes = 10
        cutoff_time = timezone.now() - timedelta(minutes=overdue_minutes)

        overdue_tickets = Ticket.objects.filter(
            status=Ticket.Status.OPEN,
            created_at__lt=cutoff_time,
        )

        if not overdue_tickets.exists():
            self.stdout.write(self.style.SUCCESS("No overdue tickets found."))
            return

        self.stdout.write(self.style.WARNING(f"Found {overdue_tickets.count()} overdue ticket(s):"))
        for ticket in overdue_tickets:
            self.stdout.write(
                f"  - Ticket #{ticket.id} ('{ticket.subject}') has been Open since {ticket.created_at}"
            )