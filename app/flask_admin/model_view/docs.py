from flask_admin.contrib.sqla import ModelView
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms import StringField, SelectField
from app.db.models import Object, ObjectDocument, User
from flask_admin import BaseView, expose

class DocumentsMenuView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/doc_menu.html')

class ObjectDocumentModelView(ModelView):
    can_create = True
    can_edit = False
    can_delete = True

    column_list = ['id', 'file_id', 'object', 'document_type']
    column_labels = {
        'id': 'ID',
        'file_id': 'file_id',
        'object': 'Объект',
        'document_type': 'Тип документа'
    }
    column_searchable_list = ['id', 'file_id']
    column_filters = ['object_id', 'document_type']

    form_columns = ['file_id', 'object_select', 'document_type']
    form_overrides = {
        'file_id': StringField,
        'document_type': SelectField,
    }

    def get_object_query(self):
        return self.session.query(Object).all()

    form_extra_fields = {
        'object_select': QuerySelectField(
            'Объект',
            query_factory=lambda: [],
            get_label='name',
            allow_blank=False,
        ),
        'document_type': SelectField(
            'Тип документа',
            choices=[
                ('estimate', 'смета'),
                ('technical_task', 'техническое задание'),
                ('customer_contacts', 'контакты заказчика')
            ]
        )
    }

    def create_form(self, obj=None):
        form = super().create_form(obj)
        form.object_select.query_factory = self.get_object_query
        return form

    def on_model_change(self, form, model, is_created):
        if hasattr(form, 'object_select') and form.object_select.data:
            model.object_id = form.object_select.data.id
        else:
            model.object_id = None
        if hasattr(form, 'document_type') and form.document_type.data:
            model.document_type = form.document_type.data

    def _object_formatter(self, context, model, name):
        return model.object.name if model.object else '—'

    column_formatters = {
        'object': _object_formatter
    }
    def is_visible(self):
        return False
    
class UserDocumentModelView(ModelView):
    can_create = True
    can_edit = False
    can_delete = True

    column_list = ['id', 'file_id', 'user']
    column_labels = {
        'id': 'ID',
        'file_id': 'file_id',
        'user': 'Пользователь'
    }
    column_searchable_list = ['id', 'file_id']
    column_filters = ['user_id']

    form_columns = ['file_id', 'user_select']
    form_overrides = {
        'file_id': StringField,
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

    def on_model_change(self, form, model, is_created):
        if hasattr(form, 'user_select') and form.user_select.data:
            model.user_id = form.user_select.data.telegram_id
        else:
            model.user_id = None

    def _user_formatter(self, context, model, name):
        return model.user.user_enter_fio if model.user else '—'

    column_formatters = {
        'user': _user_formatter
    }
    def is_visible(self):
        return False