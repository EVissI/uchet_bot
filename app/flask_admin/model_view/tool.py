from flask_admin.contrib.sqla import ModelView
from wtforms import SelectField, TextAreaField
from wtforms_sqlalchemy.fields import QuerySelectField
from app.db.models import User
from app.flask_admin.model_view.base import AuthModelView


class ToolModelView(AuthModelView):
    can_create = True
    can_edit = True
    can_delete = True

    column_list = [
        'id', 'name', 'status', 'user', 'description'
    ]
    column_labels = {
        'id': 'ID',
        'name': 'Название',
        'status': 'Статус',
        'user': 'Закреплён за',
        'description': 'Описание'
    }
    column_searchable_list = ['id', 'name', 'description']
    column_filters = ['status', 'user_id']
    form_columns = ['name', 'status', 'description', 'user_select']
    form_overrides = {
        'status': SelectField,
        'description': TextAreaField,
    }
    form_args = {
        'status': {
            'choices': [
                ('свободный', 'Свободный'),
                ('занят', 'Закреплён'),
                ('в ремонте', 'В ремонте')
            ]
        }
    }

    def get_user_query(self):
        return self.session.query(User).all()

    form_extra_fields = {
        'user_select': QuerySelectField(
            'Закреплён за',
            query_factory=lambda: [],
            get_label='user_enter_fio',
            allow_blank=True,
            blank_text='Не закреплён',
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
        tool = self.get_one(id)
        if tool and tool.user:
            form.user_select.data = tool.user
        else:
            form.user_select.data = None

    def on_model_change(self, form, model, is_created):
        super().on_model_change(form, model, is_created)
        if hasattr(form, 'user_select') and form.user_select.data:
            model.user_id = form.user_select.data.telegram_id
        else:
            model.user_id = None

    def _user_formatter(self, context, model, name):
        return model.user.user_enter_fio if model.user else '—'

    column_formatters = {
        'user': _user_formatter
    }
