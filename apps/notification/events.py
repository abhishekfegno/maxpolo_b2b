from lib.events import EventHandler
from .models import Notification


class NotificationEvent(EventHandler):
    def event_for_banners(self, instance):
        # return None
        from apps.user.models import Dealer
        user_id = [i for i in Dealer.objects.all()]
        title = "Advertisements have created"
        description = "New Advertisements have been created"
        title_list = [i for i in len(user_id) * title.split('.') if not i == '']
        description_list = [i for i in len(user_id) * description.split('.') if not i == '']
        notifications = [Notification(title=t, description=d, user=u) for t, d, u in
                         zip(title_list, description_list, user_id)]
        # import pdb;pdb.set_trace()

        return Notification.objects.bulk_create(notifications)

    def event_for_complaints(self, instance):
        # return None
        # import pdb;pdb.set_trace()
        title = f"Dear {instance.created_by},we have received your complaint"
        description = f"Your have created a complaint {instance.ticket_id}, we will check it and resolve as soon as possible"
        return Notification.objects.create(title=title, description=description, user=instance.created_by)

    def event_for_orders(self, instance, message):
        # return None
        title = f"Dear {instance.dealer}!! Your order {instance.id_as_text} has been placed"
        description = "You have created a order, we will verify and notify you the order confirmation.Thank You !!"
        return Notification.objects.create(title=title, description=description, user=instance.dealer)

    def event_for_pdfs(self, instance):
        # return None
        from apps.user.models import Dealer
        user_id = [i for i in Dealer.objects.all()]
        title = "New Products have been launched."
        description = "New Products have been launched,Check the new products."
        title_list = [i for i in len(user_id)*title.split('.') if not i == '']
        description_list = [i for i in len(user_id)*description.split('.') if not i == '']
        notifications = [Notification(title=t, description=d, user=u) for t, d, u in zip(title_list, description_list, user_id)]
        # import pdb;pdb.set_trace()

        return Notification.objects.bulk_create(notifications)
