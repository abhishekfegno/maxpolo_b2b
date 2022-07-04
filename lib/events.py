class EventHandler(object):

    def event_for_pdfs(self, **kwargs):
        raise NotImplementedError

    def event_for_banners(self, **kwargs):
        raise NotImplementedError

    def event_for_complaints(self, **kwargs):
        raise NotImplementedError

    def event_for_orders(self, **kwargs):
        raise NotImplementedError
