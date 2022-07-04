from lib.events import EventHandler
from .models import Notification


class NotificationEvent(EventHandler):
    def event_for_banners(self, instance):
        return None
        from apps.user.models import Dealer
        user_id = [i for i in Dealer.objects.all()]
        title = "Advertisements have created"
        description = "New Advertisements have been created"
        title_list = [i for i in len(user_id)*title]
        description_list = [i for i in len(user_id)*description]
        return Notification.objects.bulk_create(title=title_list, description=description_list, user=user_id)

    def event_for_complaints(self, instance):
        return None
        # import pdb;pdb.set_trace()
        title = "Your have created a complaint"
        description = "Your have created a complaint, we will check it and resolve as soon as possible"
        return Notification.objects.create(title=title, description=description, user=instance.created_by)

    def event_for_orders(self, instance):
        return None
        title = "ThankYou !! Your order has been placed"
        description = "Thank You have created a order, we will verify and notify you"
        return Notification.objects.create(title=title, description=description, user=instance.dealer)

    def event_for_pdfs(self, instance):
        return None
        from apps.user.models import Dealer
        user_id = [i for i in Dealer.objects.all()]
        title = "New Products have been launched"
        description = "New Products have been launched,Check the new products"
        title_list = [i for i in len(user_id)*title]
        description_list = [i for i in len(user_id)*description]
        return Notification.objects.bulk_create(title=title_list, description=description_list, user=user_id)
