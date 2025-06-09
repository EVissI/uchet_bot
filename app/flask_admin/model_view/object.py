from flask_admin.contrib.sqla import ModelView
from wtforms import SelectMultipleField, TextAreaField
from flask_admin.form import Select2Widget
from app.db.models import ObjectCheck, ObjectDocument, ObjectMember, ObjectPhoto, ProficAccounting, User
import flask

from app.flask_admin.model_view.base import AuthModelView


class ObjectModelView(AuthModelView):
    can_create = True
    can_edit = True
    can_delete = True

    column_list = [
        'id', 'name', 'description', 'is_active', 'members'
    ]
    column_labels = {
        'id': 'ID',
        'name': 'Название',
        'description': 'Описание',
        'is_active': 'Актуален',
        'members': 'Пользователи'
    }
    column_searchable_list = ['id', 'name', 'description']
    column_filters = ['is_active']
    column_editable_list = ['is_active']
    form_columns = ['name', 'description', 'is_active', 'user_selection']
    form_overrides = {
        'description': TextAreaField,
    }

    form_extra_fields = {
        'user_selection': SelectMultipleField(
            'Пользователи',
            coerce=int,
            widget=Select2Widget(multiple=True),
            choices=[],
            default=[]
        )
    }

    def _members_formatter(self, context, model, name):
        return ', '.join([f"{user.user_enter_fio} ({user.telegram_id})" for user in model.members])

    column_formatters = {
        'members': _members_formatter
    }

    def edit_form(self, obj=None):
        form = super().edit_form(obj)
        users = (
            self.session.query(User)
            .filter_by(can_use_bot=True)
            .order_by(User.user_enter_fio)
            .all()
        )
        current_ids = []
        if obj:
            current_ids = [m.user_id for m in obj.object_members]
        form.user_selection.choices = [(u.telegram_id, u.user_enter_fio) for u in users]
        form.user_selection.data = current_ids
        return form

    def create_form(self, obj=None):
        form = super().create_form(obj)
        users = (
            self.session.query(User)
            .filter_by(can_use_bot=True)
            .order_by(User.user_enter_fio)
            .all()
        )
        form.user_selection.choices = [(u.telegram_id, u.user_enter_fio) for u in users]
        return form

    def on_model_change(self, form, model, is_created):
        super().on_model_change(form, model, is_created)
        try:
            selected_ids = flask.request.form.getlist('user_selection', type=int)
            session = self.session
            session.query(ObjectMember).filter_by(
                object_id=model.id
            ).delete(synchronize_session='fetch')
            session.flush()
            for user_id in selected_ids:
                member = ObjectMember(
                    user_id=user_id,
                    object_id=model.id
                )
                session.add(member)
            session.commit()
        except Exception as e:
            session.rollback()
            raise Exception(f'Ошибка при сохранении пользователей: {str(e)}')
    
    def on_model_delete(self, model):
        super().on_model_delete(model)
        """
        Явно удаляем связанные записи перед удалением объекта
        """
        session = self.session
        try:
            session.query(ObjectDocument).filter_by(object_id=model.id).delete()
            session.query(ObjectCheck).filter_by(object_id=model.id).delete()
            session.query(ObjectPhoto).filter_by(object_id=model.id).delete()
            session.query(ObjectMember).filter_by(object_id=model.id).delete()
            session.query(ProficAccounting).filter_by(object_id=model.id).delete()
            session.flush()
        except Exception as e:
            session.rollback()
            raise Exception(f'Ошибка при удалении связанных данных: {str(e)}')