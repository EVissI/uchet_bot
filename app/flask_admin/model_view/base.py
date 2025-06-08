from flask_admin.contrib.sqla import ModelView
import flask



class AuthModelView(ModelView):
    def is_accessible(self):
        return flask.session.get('logged_in')

    def inaccessible_callback(self, name, **kwargs):
        return flask.redirect(flask.url_for('login'))
