# -*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program. If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from functools import wraps
import datetime
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT

def get_browse_records(self, cr, uid, ids, *args, **kwargs):
    # We could try, when context isn't in kwargs, to try for the last argument in args, but
    # that's too dangerous, so we go with None. You should always pass context as a kwarg.
    context = kwargs.get('context')
    return self.browse(cr, uid, ids, context=context)

def oemeth(single=False, browse=False):
    def decorator_single(func):
        @wraps(func)
        def wrapper(self, cr, uid, ids, *args, **kwargs):
            if isinstance(ids, (list, tuple)):
                if len(ids) != 1:
                    raise Exception("Method expecting a single target received many.")
                ids = ids[0]
            if browse:
                ids = get_browse_records(self, cr, uid, ids, *args, **kwargs)
            return func(self, cr, uid, ids, *args, **kwargs)

        return wrapper

    def decorator_multi(func):
        @wraps(func)
        def wrapper(self, cr, uid, ids, *args, **kwargs):
            if isinstance(ids, (int, long)):
                ids = [ids]
            if browse:
                ids = get_browse_records(self, cr, uid, ids, *args, **kwargs)
            return func(self, cr, uid, ids, *args, **kwargs)

        return wrapper

    if callable(single): # naked @oemeth. single is in fact a func to wrap
        return decorator_multi(single)
    return decorator_single if single else decorator_multi

def s2d(str_date):
    """Converts a value from ``fields.date()`` (a string) into a proper ``datetime.date``.

    Returns ``False`` if not a valid date (it was probably a ``False`` value).
    """
    try:
        return datetime.datetime.strptime(str_date, DEFAULT_SERVER_DATE_FORMAT).date()
    except (ValueError, TypeError):
        return False

def d2s(date):
    """Converts a ``datetime.date`` into a value that can be written in a ``fields.date()``.

    If ``date`` is not a date, returns ``False``, which will be interpreted by OE as a null value.
    """
    try:
        return date.strftime(DEFAULT_SERVER_DATE_FORMAT)
    except AttributeError:
        return False
