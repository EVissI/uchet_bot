from flask_admin.contrib.sqla import ModelView
from wtforms import SelectField, TextAreaField
from wtforms_sqlalchemy.fields import QuerySelectField
from app.db.models import Object, User, ProficAccounting, ObjectProficAccounting
from app.flask_admin.model_view.base import AuthModelView

class ProficAccountingModelView(AuthModelView):
    can_create = False
    can_edit = True
    can_delete = True

    column_list = ['id', 'amount', 'purpose', 'payment_type', 'user']
    column_labels = {
        'id': 'ID',
        'amount': 'Сумма',
        'purpose': 'Назначение',
        'payment_type': 'Тип',
        'user': 'Пользователь'
    }
    column_searchable_list = ['id', 'purpose', 'amount']
    column_filters = ['payment_type', 'created_by']

    form_columns = ['amount', 'purpose', 'payment_type', 'user_select']
    form_overrides = {
        'purpose': TextAreaField,
        'payment_type': SelectField,
    }
    form_args = {
        'payment_type': {
            'choices': [
                ('приход', 'Приход'),
                ('расход', 'Расход')
            ]
        }
    }

    def get_user_query(self):
        return self.session.query(User).all()

    form_extra_fields = {
        'user_select': QuerySelectField(
            'Пользователь',
            query_factory=lambda: [],
            get_label='user_enter_fio',
            allow_blank=False,
        )
    }

    def create_form(self, obj=None):
        form = super().create_form(obj)
        form.user_select.query_factory = self.get_user_query
        return form

    def edit_form(self, obj=None):
        form = super().edit_form(obj)
        form.user_select.query_factory = self.get_user_query
        return form

    def on_form_prefill(self, form, id):
        item = self.get_one(id)
        if item and item.user:
            form.user_select.data = item.user
        else:
            form.user_select.data = None

    def on_model_change(self, form, model, is_created):
        super().on_model_change(form, model, is_created)
        if hasattr(form, 'user_select') and form.user_select.data:
            model.created_by = form.user_select.data.telegram_id
        else:
            model.created_by = None

    def _user_formatter(self, context, model, name):
        return model.user.user_enter_fio if model.user else '—'

    column_formatters = {
        'user': _user_formatter
    }


class ObjectProficAccountingModelView(AuthModelView):
    can_create = False
    can_edit = True
    can_delete = True

    column_list = ['id', 'object', 'amount', 'purpose', 'payment_type', 'user']
    column_labels = {
        'id': 'ID',
        'object': 'Объект',
        'amount': 'Сумма',
        'purpose': 'Назначение',
        'payment_type': 'Тип',
        'user': 'Пользователь'
    }
    column_searchable_list = ['id', 'purpose', 'amount']
    column_filters = ['payment_type', 'object_id', 'created_by']

    form_columns = ['object_select', 'amount', 'purpose', 'payment_type', 'user_select']
    form_overrides = {
        'purpose': TextAreaField,
        'payment_type': SelectField,
    }
    form_args = {
        'payment_type': {
            'choices': [
                ('приход', 'Приход'),
                ('расход', 'Расход')
            ]
        }
    }

    def get_object_query(self):
        return self.session.query(Object).all()

    def get_user_query(self):
        return self.session.query(User).all()

    form_extra_fields = {
        'object_select': QuerySelectField(
            'Объект',
            query_factory=lambda: [],
            get_label='name',
            allow_blank=False,
        ),
        'user_select': QuerySelectField(
            'Пользователь',
            query_factory=lambda: [],
            get_label='user_enter_fio',
            allow_blank=False,
        )
    }

    def create_form(self, obj=None):
        form = super().create_form(obj)
        form.object_select.query_factory = self.get_object_query
        form.user_select.query_factory = self.get_user_query
        return form

    def edit_form(self, obj=None):
        form = super().edit_form(obj)
        form.object_select.query_factory = self.get_object_query
        form.user_select.query_factory = self.get_user_query
        return form

    def on_form_prefill(self, form, id):
        item = self.get_one(id)
        if item and item.object:
            form.object_select.data = item.object
        else:
            form.object_select.data = None
        if item and item.user:
            form.user_select.data = item.user
        else:
            form.user_select.data = None

    def on_model_change(self, form, model, is_created):
        super().on_model_change(form, model, is_created)
        if hasattr(form, 'object_select') and form.object_select.data:
            model.object_id = form.object_select.data.id
        else:
            model.object_id = None
        if hasattr(form, 'user_select') and form.user_select.data:
            model.created_by = form.user_select.data.telegram_id
        else:
            model.created_by = None

    def _object_formatter(self, context, model, name):
        return model.object.name if model.object else '—'

    def _user_formatter(self, context, model, name):
        return model.user.user_enter_fio if model.user else '—'

    column_formatters = {
        'object': _object_formatter,
        'user': _user_formatter
    }