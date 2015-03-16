# -*- coding: utf-8 -*-
import json
import urllib2
from datetime import datetime, date
from django.utils.crypto import salted_hmac
from django.utils.http import base36_to_int, int_to_base36
from rest_framework_jwt.settings import api_settings


def date_handler(obj):
    return obj.isoformat() if hasattr(obj, 'isoformat') else obj


def is_num(data):
    try:
        int(data)
        return True
    except ValueError:
        return False


def is_email_filter(data):
    if "@" in data:
        return True
    else:
        return False


def send_email(subject_template_name, html_email_template_name, text_email_template_name, from_email, to_emails,
               context_dictionary=None, headers=None, bcc=None, context=None, attachments=None):
    if not isinstance(to_emails, (list, tuple)):
        to_emails = [to_emails, ]
    OutboundNotification.objects.send_notification('EM', to_emails, context,
                                                   subject_template_name, html_email_template_name,
                                                   text_email_template_name, from_email,
                                                   to_emails, context_dictionary, headers, bcc, attachments)


def get_complete_name_for_email(name, email):
    return '{name} <{email}>'.format(name=name, email=email)


def jwt_payload_handler(user):
    return {
        'user_id': user.pk,
        'email': user.get_username(),
        'exp': datetime.utcnow() + api_settings.JWT_EXPIRATION_DELTA
    }


def diff_month(d1, d2):
    return (d1.year - d2.year)*12 + d1.month - d2.month


class RequestHelper(object):
    """
    Request helper class, this will help you to call and read externals urls
    """

    @staticmethod
    def _open(url, headers=None, data=None):
        if not headers: headers = {}

        try:
            opener = urllib2.build_opener()
            if data:
                request = urllib2.Request(url, data=data)
            else:
                request = urllib2.Request(url)

            for key, value in headers.items():
                request.add_header(key, value)
            response = opener.open(request)
        except urllib2.HTTPError:
            raise

        return response

    @staticmethod
    def get(url, headers=None):
        return RequestHelper._open(url, headers)

    @staticmethod
    def post(url, headers=None, data=None):
        return RequestHelper._open(url, headers, data)


def load_city_data():
    import os
    import xlrd
    from uakari.models import City

    PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
    book = xlrd.open_workbook(os.path.join(PROJECT_PATH, 'fixtures/city.xls'))

    sh = book.sheet_by_name('city')
    for rx in range(1, sh.nrows):
        city_name = sh.row(rx)[0].value
        city_name = city_name.capitalize()
        City.objects.get_or_create(name=city_name)


def load_country_data():
    import os
    import xlrd
    from uakari.models import Country

    PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
    book = xlrd.open_workbook(os.path.join(PROJECT_PATH, 'fixtures/country.xls'))

    sh = book.sheet_by_name('country')
    for rx in range(1, sh.nrows):
        country_name = sh.row(rx)[0].value
        country_name = country_name.capitalize()
        Country.objects.get_or_create(name=country_name)


class ObjectTokenGenerator(object):
    def make_token(self, obj, salt=None):
        """
        Returns a token for an object with a timestamp to check expiration
        """
        return self._make_token_with_timestamp(obj, self._num_days(date.today()), salt)

    def get_pk(self, token):
        try:
            ts_b36, pk_b36, hash = token.split("-")
            pk = base36_to_int(pk_b36)
            return pk
        except ValueError:
            return None

    def check_token(self, obj, token, salt=None, expiration_days=0):
        """
        Check that a token is valid and has not expired
        """
        # Parse the token
        try:
            ts_b36, pk_b36, hash = token.split("-")
            ts = base36_to_int(ts_b36)
            pk = base36_to_int(pk_b36)
        except ValueError:
            return False

        # Check the timestamp is within limit and that it is the correct object
        if (self._num_days(date.today()) - ts) > expiration_days or pk != obj.pk:
            return False

        # Check that the timestamp/uid has not been tampered with
        temp_token = self._make_token_with_timestamp(obj, ts, salt)
        if temp_token != token:
            return False

        return True

    def _make_token_with_timestamp(self, obj, timestamp, salt=None):
        # timestamp is number of days since 2001-1-1.  Converted to
        # base 36, this gives us a 3 digit string until about 2121
        ts_b36 = int_to_base36(timestamp)
        pk_b36 = int_to_base36(obj.pk)

        # By hashing on the internal state of the user and using state
        # that is sure to change (the password salt will change as soon as
        # the password is set, at least for current Django auth, and
        # last_login will also change), we produce a hash that will be
        # invalid as soon as it is used.
        # We limit the hash to 20 chars to keep URL short
        key_salt = salt or "utilities.TokenGenerator"

        # Ensure results are consistent across DB backends

        hash = salted_hmac(key_salt, obj.pk).hexdigest()[::2]
        return "%s-%s-%s" % (ts_b36, pk_b36, hash)

    def _num_days(self, dt):
        return (dt - date(2001, 1, 1)).days

token_generator = ObjectTokenGenerator()


def recursive_asdict(d):
    """Convert Suds object into serializable format."""
    out = {}
    for k, v in asdict(d).iteritems():
        if hasattr(v, '__keylist__'):
            out[k] = recursive_asdict(v)
        elif isinstance(v, list):
            out[k] = []
            for item in v:
                if hasattr(item, '__keylist__'):
                    out[k].append(recursive_asdict(item))
                else:
                    out[k].append(item)
        else:
            out[k] = v
    return out


def suds_to_json(data):
    return json.dumps(recursive_asdict(data), encoding='utf8', ensure_ascii=False)