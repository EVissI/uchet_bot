from flask_admin.contrib.sqla import ModelView
import flask

from app.db.models import AdminActionLog


class AuthModelView(ModelView):
    def is_accessible(self):
        if not flask.session.get("admin_id"):
            return False
        return True

    def inaccessible_callback(self, name, **kwargs):
        return flask.redirect(flask.url_for("admin_login"))

    def _log_action(self, action, model, record_id=None, details=None):
        try:
            # Get primary key value
            primary_key = model.__table__.primary_key.columns.keys()[0]
            if record_id is None:
                if isinstance(model, type):
                    return
                record_id = getattr(model, primary_key)

            log = AdminActionLog(
                admin_user_id=flask.session["admin_id"],
                action=action,
                model=model.__tablename__,
                record_id=str(record_id),
                details=details,
            )
            self.session.add(log)
            self.session.flush()
        except Exception as e:
            self.session.rollback()
            raise Exception(f"Failed to log action: {str(e)}")

    def on_model_change(self, form, model, is_created):
        try:
            form_data = {}
            for k, v in form.data.items():
                if hasattr(v, "telegram_id"): 
                    form_data[k] = {"id": v.telegram_id, "type": "User"}
                elif hasattr(v, "id"):  
                    form_data[k] = {"id": v.id, "type": v.__class__.__name__}
                else:
                    form_data[k] = str(v)

            if is_created:
                self.session.flush()
                self._log_action("create", model, None, {"data": form_data})
            else:
                self._log_action("edit", model, None, {"changes": form_data})
        except Exception as e:
            self.session.rollback()
            raise

    def on_model_delete(self, model):
        try:
            self._log_action("delete", model, None)
        except Exception as e:
            self.session.rollback()
            raise
