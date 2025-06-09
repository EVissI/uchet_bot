from flask_admin.contrib.sqla import ModelView
import flask

from app.db.models import AdminActionLog



class AuthModelView(ModelView):
    def is_accessible(self):
        if not flask.session.get('admin_id'):
            return False
        return True

    def inaccessible_callback(self, name, **kwargs):
        return flask.redirect(flask.url_for('admin_login'))

    def _log_action(self, action, model, record_id, details=None):
        try:
            log = AdminActionLog(
                admin_user_id=flask.session['admin_id'],
                action=action,
                model=model.__tablename__,
                record_id=record_id,
                details=details
            )
            self.session.add(log)
            self.session.flush() 
        except Exception as e:
            self.session.rollback()
            raise Exception(f'Failed to log action: {str(e)}')

    def on_model_change(self, form, model, is_created):
        try:
            if is_created:
                self.session.flush()
                self._log_action('create', type(model), model.id, 
                               {'data': {k: str(v) for k, v in form.data.items()}})
            else:
                self._log_action('edit', type(model), model.id,
                               {'changes': {k: str(v) for k, v in form.data.items()}})
        except Exception as e:
            self.session.rollback()
            raise

    def on_model_delete(self, model):
        try:
            self._log_action('delete', type(model), model.id)
        except Exception as e:
            self.session.rollback()
            raise