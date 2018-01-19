from wtforms import Form, PasswordField, StringField, validators


class UserLoginForm(Form):
    login = StringField(
        'Login', [validators.Required(),
                  validators.Length(min=3, max=256)]
    )
    password = PasswordField(
        'Password', [validators.Required(),
                     validators.Length(min=8, max=256)]
    )
