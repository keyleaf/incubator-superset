# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from flask import g, redirect, flash
from flask_appbuilder._compat import as_unicode
from flask_appbuilder.security.views import AuthRemoteUserView, expose
from flask_login import login_user

# import the remote server here
# remote server API to authenticate username/Email
from . import remote_server_api

from flask_appbuilder.security.forms import LoginForm_db

import logging

logger = logging.getLogger(__name__)


class MyAuthRemoteUserView(AuthRemoteUserView):
    # this front-end template should be put under the folder `superset/templates/appbuilder/general/security`
    # so that superset could find this templates to render
    # login_template = 'appbuilder/general/security/login_my.html'
    login_template = 'appbuilder/general/security/login_db.html'
    title = "Auth Center"

    # this method is going to overwrite 
    # https://github.com/dpgaspar/Flask-AppBuilder/blob/master/flask_appbuilder/security/views.py#L556
    @expose('/login/', methods=['GET', 'POST'])
    def login(self):
        logger.info("My special login...")
        if g.user is not None and g.user.is_authenticated():
            return redirect(self.appbuilder.get_url_for_index)

        form = LoginForm_db()

        if form.validate_on_submit():
            logger.info("going to auth MY user: %s" % form.username.data)
            my_user = remote_server_api.AuthCenter.authenticate(form.username.data,
                                                                form.password.data)
            # if my_user is authenticated                          
            if my_user:
                user = self.appbuilder.sm.auth_user_remote_user(
                    my_user.get('username'))
                if user is None:
                    flash(as_unicode(self.invalid_login_message), 'warning')
                else:
                    login_user(user)
                    return redirect(self.appbuilder.get_url_for_index)
            else:
                flash(as_unicode(self.invalid_login_message), 'warning')
        else:
            if form.errors.get('email') is not None:
                flash(
                    as_unicode(" ".join(form.errors.get('email'))), 'warning')

        return self.render_template(
            self.login_template,
            title=self.title,
            form=form,
            appbuilder=self.appbuilder)
