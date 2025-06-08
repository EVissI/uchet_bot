from flask_admin.contrib.sqla import ModelView
from wtforms import SelectField, SelectMultipleField
from flask_admin.form import Select2Widget
from app.db.models import ObjectMember, Object, User
import flask


class UserModelView(ModelView):
    can_create = False
    can_delete = False
    can_edit = True

    column_list = [
        'telegram_id',
        'user_enter_fio',
        'username',
        'phone_number',
        'role',
        'objects'
    ]
    column_labels = {
        'telegram_id': 'Telegram ID',
        'user_enter_fio': 'ФИО',
        'username': 'Username',
        'phone_number': 'Телефон',
        'role': 'Роль',
        'objects': 'Объекты'
    }

    form_columns = [
        'user_enter_fio',
        'username',
        'phone_number',
        'role',
        'object_selection'
    ]

    form_overrides = {
        'role': SelectField
    }

    form_args = {
        'role': {
            'choices': [
                (User.Role.admin.value, 'Администратор'),
                (User.Role.worker.value, 'Работник'),
                (User.Role.foreman.value, 'Прораб'),
                (User.Role.buyer.value, 'Закупщик')
            ]
        }
    }

    def _objects_formatter(self, context, model, name):
        return ', '.join([f"{obj.name} ({obj.id})" for obj in model.objects])

    column_formatters = {
        'objects': _objects_formatter
    }


    form_extra_fields = {
        'object_selection': SelectMultipleField(
            'Объекты',
            coerce=int,
            widget=Select2Widget(multiple=True),
            choices=[],
            default=[]
        )
    }

    def edit_form(self, obj=None):
        form = super().edit_form(obj)
        objects = (
            self.session.query(Object)
            .filter_by(is_active=True)
            .order_by(Object.id)
            .all()
        )
        current_ids = []
        if obj:
            current_ids = [om.object_id for om in obj.object_members]
            print(f"[DEBUG] Pre-selected objects: {current_ids}")

        form.object_selection.choices = [(o.id, o.name) for o in objects]
        form.object_selection.data = current_ids
        return form

    def create_form(self, obj=None):
        form = super().create_form(obj)
        objects = (
            self.session.query(Object)
            .filter_by(is_active=True)
            .order_by(Object.id)
            .all()
        )
        form.object_selection.choices = [(o.id, o.name) for o in objects]
        return form

    def on_model_change(self, form, model, is_created):
        try:
            print("[DEBUG] Starting model change...")
            selected_ids = flask.request.form.getlist('object_selection', type=int)
            print("[DEBUG] Selected objects from POST:", selected_ids)

            session = self.session
            session.query(ObjectMember).filter_by(
                user_id=model.telegram_id
            ).delete(synchronize_session='fetch')
            session.flush()
            for object_id in selected_ids:
                member = ObjectMember(
                    user_id=model.telegram_id,
                    object_id=object_id
                )
                session.add(member)
                print(f"[DEBUG] Added relationship for object {object_id}")
            session.commit()
            print("[DEBUG] Changes saved successfully")
        except Exception as e:
            print(f"[ERROR] Failed to save changes: {str(e)}")
            session.rollback()
            raise Exception(f'Ошибка при сохранении объектов: {str(e)}')