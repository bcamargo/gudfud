
class BaseUserMixin(object):
    """
    Mixin to provide access to useful properties and methods of a base user
    This class assumes any model that inherits from this class will have a base_user attribute
    """
    @property
    def email(self):
        return self.base_user.email

    @email.setter
    def email(self, value):
        self.base_user.email = value

    @property
    def password(self):
        return self.base_user.password

    @property
    def first_name(self):
        return self.base_user.first_name

    @first_name.setter
    def first_name(self, value):
        self.base_user.first_name = value

    @property
    def last_name(self):
        return self.base_user.last_name

    @last_name.setter
    def last_name(self, value):
        self.base_user.last_name = value

    @property
    def gender(self):
        return self.base_user.gender

    @gender.setter
    def gender(self, value):
        self.base_user.gender = value

    @property
    def salutation(self):
        return self.base_user.salutation

    @salutation.setter
    def salutation(self, value):
        self.base_user.salutation = value

    @property
    def is_active(self):
        return self.base_user.is_active

    @property
    def date_joined(self):
        return self.base_user.date_joined

    @property
    def image(self):
        return self.base_user.image

    @image.setter
    def image(self, value):
        self.base_user.image = value

    @property
    def referred_by(self):
        return self.base_user.referred_by

    @referred_by.setter
    def referred_by(self, value):
        self.base_user.referred_by = value

    @property
    def thumbnail_image(self):
        return self.base_user.thumbnail_image

    @property
    def full_name(self):
        return self.base_user.get_full_name()

    @property
    def is_physician(self):
        return self.base_user.is_physician

    @property
    def is_assistant(self):
        return self.base_user.is_assistant

    @property
    def is_email_verified(self):
        return self.base_user.is_email_verified

    @property
    def password(self):
        return self.base_user.password

    @property
    def is_registration_completed(self):
        return self.base_user.is_registration_completed

    def set_password(self, raw_password):
        self.base_user.set_password(raw_password)

    def get_username(self):
        return self.base_user.get_username()

    def check_password(self, raw_password):
        return self.base_user.check_password(raw_password)

    def get_short_name(self):
        return self.base_user.get_short_name()

    def get_password_reset_token(self):
        return self.base_user.get_password_reset_token()

    def check_password_reset_token(self, token):
        return self.base_user.check_password_reset_token(token)

    def check_token_and_generate_new_password(self, token):
        return self.base_user.check_token_and_generate_new_password(token)

    def is_authenticated(self):
        return self.base_user.is_authenticated()

    def email_user(self, subject_template_name, html_email_template_name, text_email_template_name, from_email,
                   context_dictionary=None):
        return self.base_user.send_email(subject_template_name, html_email_template_name, text_email_template_name,
                                         from_email, [self.email], context_dictionary)

    def verify_email(self, activation_key):
        return self.base_user.verify_email(activation_key)

    def email_confirmation_email(self):
        return self.base_user.email_confirmation_email()