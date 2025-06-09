from flask_admin.contrib.sqla import ModelView
from wtforms import TextAreaField, StringField
from wtforms.validators import Optional
from app.db.models import MaterialReminder
from app.flask_admin.model_view.base import AuthModelView

class MaterialReminderModelView(AuthModelView):
    can_create = True
    can_edit = True
    can_delete = True

    column_list = ['id', 'description', 'file_id', 'storage_location', 'is_active']
    column_labels = {
        'id': 'ID',
        'description': 'Описание',
        'file_id': 'Фото (file_id)',
        'storage_location': 'Местоположение',
        'is_active': 'Актуален'
    }
    column_searchable_list = ['id', 'description', 'storage_location']
    column_filters = ['is_active']

    # Позволяет менять актуальность прямо из списка
    column_editable_list = ['is_active']

    form_columns = ['description', 'file_id', 'storage_location', 'is_active']
    form_overrides = {
        'description': TextAreaField,
        'file_id': StringField,
        'storage_location': StringField,
    }
    form_args = {
        'file_id': {'validators': [Optional()]},
        'storage_location': {'validators': [Optional()]},
    }

    def scaffold_form(self):
        form_class = super().scaffold_form()
        if not hasattr(form_class, 'is_active'):
            from wtforms import BooleanField
            form_class.is_active = BooleanField('Актуален')
        return form_class

    def on_model_change(self, form, model, is_created):
        super().on_model_change(form, model, is_created)
        if not hasattr(model, 'is_active'):
            model.is_active = True