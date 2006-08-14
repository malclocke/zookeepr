import datetime
import md5
import random

class Person(object):
    """Stores both account login details and personal information.

    We assume a 1-1 mapping of user accounts to personal details,
    for convenience, and so through the act of logging in we get
    all the information about that person.
    """
    def __init__(self, handle=None, email_address=None, password=None,
                 firstname=None, lastname=None, phone=None, fax=None,
                 creation_timestamp=None,
                 activated=None,
                 ):
        # account information
        self.email_address = email_address
        self.password = password
        self.activated = activated or False
        self.creation_timestamp = creation_timestamp or datetime.datetime.now()

        self.handle = handle
        if self.fullname is not None:
            self.fullname = fullname
        else:
            self.firstname = firstname
            self.lastname = lastname
        self.phone = phone
        self.fax = fax

        # url_hash should never be modifiable by the caller directly
        self._update_url_hash()

    def _set_password(self, value):
        if value is not None:
            self.password_hash = md5.new(value).hexdigest()

    def _get_password(self):
        return self.password_hash

    password = property(_get_password, _set_password)

    def check_password(self, value):
        """Check the given password is equal to the stored one"""
        return self.password_hash == md5.new(value).hexdigest()

    def _set_creation_timestamp(self, value):
        if value is None:
            self._creation_timestamp = datetime.datetime.now()
        else:
            self._creation_timestamp = value
        self._update_url_hash()

    def _get_creation_timestamp(self):
        return self._creation_timestamp

    creation_timestamp = property(_get_creation_timestamp, _set_creation_timestamp)

    def _get_url_hash(self):
        return self._url_hash

    url_hash = property(_get_url_hash)

    def _update_url_hash(self):
        """Update the stored URL hash for this person.

        Call this when an element of the URL hash has changed
        (i.e. either the email address or timestamp)
        """
        nonce = random.randrange(0, 2**30)
        magic = "%s&%s&%s" % (self.email_address,
                              self.creation_timestamp,
                              nonce)
        self.url_hash = md5.new(magic).hexdigest()

    def __repr__(self):
        return '<Person id="%s" email="%s">' % (self.id, self.email_address)

    def _set_fullname(self, value):
        if value is not None:
            self.firstname = value.split(' ')[0]
            self.lastname = ' '.join(value.split(' ')[1:])
        else:
            self.firstname = None
            self.lastname = None

    def _get_fullname(self):
        r = self.firstname
        if self.lastname:
            r = r + ' ' + self.lastname
        return r

    fullname = property(_get_fullname, _set_fullname)


class Role(object):
    def __init__(self, name=None):
        self.name = name

    def __repr__(self):
        return '<Role id="%s" name="%s">' % (self.id, self.name)