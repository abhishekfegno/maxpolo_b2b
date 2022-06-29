from django.contrib import messages
from django.core.exceptions import PermissionDenied, ValidationError
from django.db import transaction
from django.db.models import QuerySet, Q
from django.forms import ModelForm
from django.http import HttpResponseRedirect, Http404
from django.urls import include, path, reverse_lazy, NoReverseMatch, reverse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django_filters.constants import ALL_FIELDS
from django_filters.views import FilterView

from apps.infrastructure.models import Warehouse
from apps.user.models import Dealer, Executive, Role


class QuerysetFilterMixin:

    def get_queryset(self) -> QuerySet:
        request = self.request
        QS = super().get_queryset()

        if self.request.user.is_superuser or request.user.user_role == request.user.ADMIN or (
                hasattr(self.model, 'bypass_qs_filter') and self.model.bypass_qs_filter):
            return QS
        account = request.user.account
        branch = account and account.branch
        if branch:
            return QS.filter(**{self.model.branch_filter: branch})
        return QS.none()

    @property
    def is_admin(self):
        return self.request.user.is_authenticated and (
                self.request.user.is_superuser or self.request.user.user_role == self.request.user.ADMIN)


class ModelSelectorMixin(QuerysetFilterMixin,
                         # PermissionMixin
                         ):
    model = None
    app_name = None
    access_to = Role.DEFAULT
    redirect_to = 'update'

    def get_success_url(self):
        _app_name = ''
        if self.app_name:
            _app_name += self.app_name + ':'

        if self.request.method == 'POST':
            data = self.request.POST
        else:
            data = self.request.GET
        try:
            if data.get('submit'):
                if 'another' in data.get('submit').lower():
                    return reverse(f'{_app_name}{self.model.reverser}-create', )
                elif 'continue' in data.get('submit').lower():
                    return reverse(f'{_app_name}{self.model.reverser}-update', kwargs={'pk': self.object.pk})
                else:
                    return reverse(f'{_app_name}{self.model.reverser}-list')
            else:
                if self.redirect_to == 'create':
                    return reverse(f'{_app_name}{self.model.reverser}-create', )
                elif self.redirect_to == 'update':
                    return reverse(f'{_app_name}{self.model.reverser}-update', kwargs={'pk': self.object.pk})
        except NoReverseMatch as e:
            pass
        return reverse(f'{_app_name}{self.model.reverser}-list')

    def get_context_data(self, **kwargs):
        def format_title(plural=False):
            field = 'verbose_name' + ((plural and '_plural') or '')
            return " ".join([name[0].upper() + name[1:] for name in getattr(self.model._meta, field).split(' ')])

        _app_name = ''
        if self.app_name:
            _app_name += self.app_name + ':'
        try:
            self.object_list = self.get_queryset()
        except Exception as e:
            self.object_list = self.model.objects.all()

        kwargs['title'] = format_title()
        kwargs['model_class'] = self.model
        kwargs['title_plural'] = format_title(plural=True)
        kwargs['list_url'] = reverse_lazy(f'{_app_name}{self.model.reverser}' + '-list')

        kwargs['create_new_url'] = reverse_lazy(f'{_app_name}{self.model.reverser}' + '-create')
        kwargs['update_url_name'] = f'{_app_name}{self.model.reverser}' + '-update'
        kwargs.update(super().get_context_data(**kwargs))
        return kwargs

    def get_form_class(self):
        branch_required = []

        if not self.is_admin and self.fields and 'branch' in self.fields:
            self.fields = [f for f in self.fields if f != 'branch']
            branch_required.append('branch')
        form: ModelForm = super(ModelSelectorMixin, self).get_form_class()

        outer_self = self
        request = self.request

        class MyForm(form):
            __name__ = form.__name__
            __doc__ = form.__doc__

            def __init__(self, *args, **kwargs):

                # assert (date fields will not be used for any other purpose in any models)
                self.context2 = kwargs.get('context', {})
                if 'context' in kwargs.keys():
                    kwargs.pop('context')

                super(MyForm, self).__init__(*args, **kwargs)
                if hasattr(self, 'fields'):
                    if self.fields.get('mobile'):
                        self.fields['mobile'].initial = "+91 "
                    if not outer_self.is_admin:
                        branch = outer_self.request.branch
                        if self.fields.get('warehouse'):
                            warehouse_kwargs = {Warehouse.branch_filter: branch}
                            self.fields['warehouse'].queryset = Warehouse.objects.filter(**warehouse_kwargs)

                        if self.fields.get('executive'):
                            executive_kwargs = {f'{Executive.branch_filter}': branch}
                            self.fields['executive'].queryset = Executive.objects.filter(**executive_kwargs)

                        if self.fields.get('dealer'):
                            dealer_kwargs = {Dealer.branch_filter: branch}
                            self.fields['dealer'].queryset = Dealer.objects.filter(**dealer_kwargs)

            def clean_mobile(self, ):
                mobile = self.cleaned_data['mobile']
                from apps.user.models import User
                qs = User.objects.filter(username__endswith=mobile.national_number)
                if self.instance and hasattr(self.instance, 'user'):
                    qs = qs.exclude(pk=self.instance.user_id)
                if qs.exists():
                    raise ValidationError(
                        'This mobile number is used by some other user in this system.'
                    )
                return mobile

            def clean(self):
                attrs = self.cleaned_data
                if isinstance(self.instance, Warehouse):
                    if attrs.get('branch'):
                        if Warehouse.objects.filter(branch=attrs.get('branch')).exists():
                            from django.core.exceptions import ValidationError
                            raise ValidationError(f'This branch {attrs.get("branch").name} already have a warehouse.')

                if isinstance(self.instance, StockLogGrouper) and not self.instance.pk:
                    print(" >>> Cleaning data for StockLogGrouper <<< ")
                    from django.core.exceptions import ValidationError
                    from apps.stockrecord.managers import StockLogConstant
                    C = StockLogConstant
                    attrs['transfer_type'] = self.instance.p_transfer_type
                    attrs["branch"] = attrs.get("branch")

                    if not attrs.get('dealer'):
                        if attrs.get('transfer_type') == C.SALES_OUT:
                            raise ValidationError(f'"Dealer" must be specified for {attrs["transfer_type"]} Entry')
                        if attrs["transfer_type"] == C.DAMAGE_OUT and attrs["reason_damage"] and 'dealer' in attrs[
                            "reason_damage"].lower():
                            raise ValidationError(
                                f'"Dealer" must be specified for {C.DAMAGE_OUT} with {attrs["reason_damage"]}')

                    if not attrs.get("manufacturer"):
                        if attrs["transfer_type"] == C.PURCHASE_IN:
                            raise ValidationError('"Manufacturer" must be specified for a Purchase Entry')
                        if attrs["transfer_type"] == C.DAMAGE_OUT and attrs.get(
                                "reason_damage") and 'manufacturer' in attrs.get("reason_damage").lower():
                            raise ValidationError(
                                f'"Manufacturer" must be specified for {C.DAMAGE_OUT} with {attrs["reason_damage"]}')

                    if not attrs.get("partner") and attrs["transfer_type"] in (C.TRANSFER_IN, C.TRANSFER_OUT):
                        raise ValidationError(f'"Partner" must be specified for a {attrs["transfer_type"]} Entry')
                    usr = outer_self.request.user
                    if (
                            attrs.get("partner")
                            and attrs["partner"] in (attrs["branch"], usr.user_role > usr.ADMIN and usr.account.branch)
                            and attrs["transfer_type"] in (C.TRANSFER_IN, C.TRANSFER_OUT)
                    ):
                        raise ValidationError(
                            f'"Partner Branch" cannot be same as {"your" if usr.user_role > usr.ADMIN else "Owner"} Branch')

                    if not attrs.get("summary") and attrs["transfer_type"] in (
                            C.RETURN_IN, C.TRANSFER_IN, C.DAMAGE_OUT):
                        raise ValidationError(f'"Summary" must be specified for {attrs["transfer_type"]} Entry!')
                if self.context2.get('formset_object'):
                    self.context2.get('formset_object').is_valid()
                return attrs

        if len(branch_required) > 0:
            self.fields.extend(branch_required)

        return MyForm


class ModelSelectorFormMixin(ModelSelectorMixin):

    def get_filterset_kwargs(self, filterset_class):
        kwargs = super(ModelSelectorFormMixin, self).get_filterset_kwargs(filterset_class)
        kwargs['prefix'] = 'filter'
        return kwargs

    @transaction.atomic
    def form_valid(self, form):
        context = self.get_context_data()
        request = self.request
        if form.is_valid():
            obj = form.instance
            if hasattr(obj, 'created_by') and not getattr(obj, 'created_by'):
                obj.created_by = self.request.user
            form.save()
            if not self.is_admin:
                account = request.user.account
                branch = account and account.branch
                if hasattr(form.instance, 'branch'):
                    setattr(form.instance, 'branch', branch)
            # if isinstance(form.instance, AbstractProfile) and hasattr(form.instance, 'user'):
            #     params = {
            #         "username": form.instance.mobile and form.instance.mobile.national_number,
            #         "first_name": obj.name,
            #         "user_role": form.instance.chosen_role,
            #     }
            #     if getattr(form.instance, 'user') is None:
            #         form.instance.user = User.objects.create_user(password=settings.NEW_USER_PASSWORD, **params)
            #     else:
            #         for field, value in params.items():
            #             setattr(form.instance.user, field, value)
            #         form.instance.user.save()
            try:
                created = form.instance and form.instance.pk
                self.object = form.save() or form.instance

                if not created:
                    messages.success(self.request,
                                     f"{form.instance.__class__._meta.verbose_name.capitalize()} "
                                     f"\"{str(form.instance)}\" Updated Successfully!")
                return HttpResponseRedirect(self.get_success_url())
            except Exception as e:
                # if isinstance(form.instance, AbstractProfile) and hasattr(form.instance, 'user'):
                #     if getattr(form.instance, 'user') is not None:
                #         form.instance.user.delete()
                raise e
        return self.form_invalid(form)


def view_set_generator(model, app_name=None, queryset=None, visibility_above=Role.DEFAULT, fields='__all__', **kwargs):
    _app_name = app_name
    _model = model
    _queryset = queryset or model.objects.all()
    _form_class = kwargs.get('form_class')
    _fields = fields if kwargs.get('form_class') is None else None
    _visibility_above = visibility_above
    _redirect_to = kwargs.get('redirect_to', 'update')
    _filter_class = kwargs.get('filter_class')
    _filterset_fields = kwargs.get('filterset_fields', ALL_FIELDS)

    def get_view_kwargs(view='list'):
        if hasattr(model, 'View'):
            return getattr(model.View, f'{view}_view', {})
        return {}

    class DashboardCustomList(ModelSelectorFormMixin, FilterView):
        fields = (_fields or '__all__') if not _app_name else None
        model = _model
        app_name = _app_name
        queryset = _queryset
        paginate_by = 30
        access_to = visibility_above
        redirect_to = _redirect_to
        filter_class = _filter_class
        filterset_fields = _filterset_fields

        def get_filterset_kwargs(self, filterset_class):
            kwargs = super().get_filterset_kwargs(filterset_class)
            kwargs['prefix'] = 'filter'
            return kwargs

        def get_template_names(self):
            return [f'{self.app_name}/{self.model.__name__.lower()}_list.html']

        def get(self, request, *args, **kwargs):
            if self.filter_class:
                return super(DashboardCustomList, self).get(request, *args, **kwargs)
            self.object_list = self.get_queryset()
            allow_empty = self.get_allow_empty()

            if not allow_empty:
                # When pagination is enabled and object_list is a queryset,
                # it's better to do a cheap query than to load the unpaginated
                # queryset in memory.
                if self.get_paginate_by(self.object_list) is not None and hasattr(self.object_list, 'exists'):
                    is_empty = not self.object_list.exists()
                else:
                    is_empty = not self.object_list
                if is_empty:
                    raise Http404('Empty list and “%(class_name)s.allow_empty” is False.' % {
                        'class_name': self.__class__.__name__,
                    })
            context = self.get_context_data()
            return self.render_to_response(context)

        def dispatch(self, request, *args, **kwargs):
            if not self.request.user.is_authenticated or self.request.user.user_role > self.access_to:
                raise PermissionDenied(" You are not authorized to access this page. ")
            return super().dispatch(request, *args, **kwargs)

        filter_object = None

        def get_queryset(self) -> QuerySet:
            qs = super().get_queryset()
            # if self.filter_class:
            #     self.filter_object = ProductFilter(data=self.request.GET, queryset=qs, request=self.request, prefix='filter')
            search_fields = getattr(self.model, 'search_fields', ['name'])
            search_fields = [f'{s}__icontains' for s in search_fields if hasattr(self.model, s)]
            if self.request.GET.get('q'):
                searcher = Q()
                for search_field in search_fields:
                    searcher |= Q(**{search_field: self.request.GET.get('q')})
                qs = qs.filter(searcher)
            return qs

        def get_context_data(self, **kwargs):
            out = super(DashboardCustomList, self).get_context_data(**kwargs)
            if self.filter_object:
                out['filter'] = self.filter_object
                # out['object_list'] = self.filter_object.qs
            return out

    class DashboardCustomCreate(ModelSelectorFormMixin, CreateView):
        model = _model
        app_name = _app_name
        form_class = _form_class
        if not _form_class:
            fields = _fields
        queryset = _queryset
        access_to = visibility_above
        redirect_to = _redirect_to

        def dispatch(self, request, *args, **kwargs):
            if not self.request.user.is_authenticated or self.request.user.user_role > self.access_to:
                raise PermissionDenied(" You are not authorized to access this page.")
            return super().dispatch(request, *args, **kwargs)

        def get_success_url(self):
            return reverse(f'{_app_name}:{model.reverser}-update', kwargs={'pk': self.object.id})

    class DashboardCustomDetail(ModelSelectorFormMixin, UpdateView):
        fields = (_fields or '__all__') if not _app_name else None

        model = _model
        app_name = _app_name
        form_class = _form_class
        success_url = reverse_lazy(f'{_app_name}:{model.reverser}-list')
        fields = _fields
        queryset = _queryset
        access_to = visibility_above
        redirect_to = _redirect_to

        def dispatch(self, request, *args, **kwargs):
            if not self.request.user.is_authenticated or self.request.user.user_role > self.access_to:
                raise PermissionDenied(" You are not authorized to access this page.")
            return super().dispatch(request, *args, **kwargs)

    class DashboardCustomDelete(ModelSelectorFormMixin, DeleteView):
        fields = (_fields or '__all__') if not _app_name else None

        model = _model
        app_name = _app_name
        success_url = reverse_lazy(f'{_app_name}:{model.reverser}-list')
        fields = _fields
        queryset = _queryset
        access_to = visibility_above
        redirect_to = _redirect_to

        def dispatch(self, request, *args, **kwargs):
            if not self.request.user.is_authenticated or self.request.user.user_role > self.access_to:
                raise PermissionDenied("You are not authorized to access this page.")
            return super().dispatch(request, *args, **kwargs)

    list_view = DashboardCustomList.as_view(**get_view_kwargs('list'))
    create_view = DashboardCustomCreate.as_view(**get_view_kwargs('form'))
    update_view = DashboardCustomDetail.as_view(**get_view_kwargs('form'))
    delete_view = DashboardCustomDelete.as_view(**get_view_kwargs('delete'))

    return path(f'{model.reverser}/', include([
        path('', list_view, name=f"{model.reverser}-list"),
        path('create/', create_view, name=f"{model.reverser}-create"),
        path('<int:pk>/', update_view, name=f'{model.reverser}-update'),
        path('<int:pk>/delete/', delete_view, name=f'{model.reverser}-delete'),
    ]))
