import datetime

from django.contrib import messages
from django.core.paginator import Paginator
from django.utils import datetime_safe
from django.views.generic import DetailView, ListView, UpdateView, CreateView

from apps.executivetracking.models import CheckPoint, Zone
from apps.user.models import Executive, Role, User
# Create your views here.
from apps.viewset import ModelSelectorMixin


class FieldForceSelect(
    # PermissionMixin,
    ListView
):
    template_name = 'executivetracking/field-force-tracking.html'
    access_to = Role.BRANCH_MANAGER

    def get_queryset(self):
        qs = Executive.objects.all()
        has_account = hasattr(self.request.user, 'account')
        if has_account and int(self.request.user.user_role) > Role.ADMIN:
            qs = qs.filter(branch=self.request.user.account.branch)
        if self.request.GET.get('place'):
            qs = qs.filter(place__iexact=self.request.GET.get('place'))
        return qs

    def get_context_data(self, **kwargs):
        kwargs = super(FieldForceSelect, self).get_context_data(**kwargs)
        date = datetime_safe.date.today()
        kwargs['selected_date'] = date.strftime("%d-%m-%Y")
        return kwargs


class FieldForceTracking(
    # PermissionMixin,
    DetailView
):
    template_name = 'executivetracking/field-force-tracking.html'
    access_to = Role.BRANCH_MANAGER

    def get_queryset(self):
        qs = Executive.objects.all()
        has_account = hasattr(self.request.user, 'account')
        if has_account and int(self.request.user.user_role) > Role.ADMIN:
            qs = qs.filter(branch=self.request.user.account.branch)
        # print(qs)
        return qs

    def get_context_data(self, **kwargs):
        kwargs = super(FieldForceTracking, self).get_context_data(**kwargs)
        self.object = self.get_object(self.get_queryset())
        date = self.request.GET.get('date')
        if not date:
            date = datetime_safe.date.today()
        else:
            try:
                date = datetime_safe.datetime.strptime(date, "%d-%m-%Y").date()
            except:
                date = datetime_safe.date.today()
                messages.warning(self.request, "Invalid Date format")
        check_in = CheckPoint.objects.filter(
            **{'check_in_at__range': (
                datetime.datetime.combine(date, datetime.time.min),
                datetime.datetime.combine(date, datetime.time.max)
            )},
            executive=self.object).select_related('store').order_by('check_in_at')

        kwargs['checkin_set'] = check_in
        # kwargs['checkin_set'].sort(key=lambda check: check.check_in_at)

        kwargs['first_device_id'] = kwargs['checkin_set'][0].device_id if len(kwargs['checkin_set']) else None

        kwargs['check_list'] = self.get_queryset()
        kwargs['object_list'] = self.get_queryset()
        kwargs['selected_date'] = date.strftime("%d-%m-%Y")
        kwargs['selected_date_obj'] = date
        return kwargs


class LeadListView(ModelSelectorMixin, ListView):
    template_name = 'executivetracking/lead-list.html'
    access_to = Role.BRANCH_MANAGER
    model = User
    object = None

    def get_object(self, queryset=None):
        """
        Return the object the view is displaying.

        Require `self.queryset` and a `pk` or `slug` argument in the URLconf.
        Subclasses can override this to return any object.
        """
        # Next, try looking up by primary key.
        pk = self.kwargs.get('pk')
        if pk is not None:
            queryset = queryset.filter(pk=pk)

        self.object = queryset.first()
        return self.object

    def get_queryset(self):
        qs = Executive.objects.all()
        has_account = hasattr(self.request.user, 'account')
        if has_account and int(self.request.user.user_role) > Role.ADMIN:
            qs = qs.filter(branch=self.request.user.account.branch)
        return qs

    def get_context_data(self, **kwargs):
        kwargs = super(LeadListView, self).get_context_data(**kwargs)
        qs = User.objects.all().filter(executive=self.kwargs.get('pk')).order_by('-id')
        page_number = self.request.GET.get('page')
        page_size = self.request.GET.get('page_size', 30)
        paginator = Paginator(qs, page_size)
        page_obj = paginator.get_page(page_number)
        kwargs['page_obj'] = page_obj
        kwargs['object'] = self.get_object(Executive.objects.all())
        return kwargs


class DistrictList(ModelSelectorMixin, ListView):
    template_name = 'executivetracking/district_list.html'
    model = Zone
    app_name = ''
    access_to = Role.BRANCH_MANAGER


class DistrictCreateView(ModelSelectorMixin, CreateView):
    template_name = 'executivetracking/district_form.html'
    model = Zone
    app_name = ''
    access_to = Role.BRANCH_MANAGER
    fields = ("name",)


class DistrictUpdateView(ModelSelectorMixin, UpdateView):
    template_name = 'executivetracking/district_form.html'
    model = Zone
    app_name = ''
    access_to = Role.BRANCH_MANAGER
    fields = ("name",)
