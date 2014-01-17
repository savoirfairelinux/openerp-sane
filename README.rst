openerp-sane: Bring sanity back, one step at a time
===================================================

openerp-sane is a collection of small utilities, making OpenERP development seem less like ancient
warfare with blood and guts everywhere, and more like Python.

For now, there's just one utility: the ``@oemeth`` method decorator which straightens out our we
manage the famous ``ids`` argument in our model methods. Example:

.. code-block:: python

    def myaction(self, cr, uid, ids, context=None): pass

Normally, ``ids`` is supposed to be a list of ``int``, but *sometimes*, just, **sometimes**, we get
a naked ``int``, then our method crashes. We have to add code like:

.. code-block:: python

    if isinstance(ids, (int, long)):
        ids = [ids]

On top of that, there's another annoyance: why, oh *why* do all my methods have to handle cases
with multiple ``ids``? When I have an action for some button in a form, I *know* it's only ever
going to handle one id at a time. I can do ``ids[0]`` easily enough, but if I really want to be
on the safe side, I'll make sure that ``ids`` is a list first. Aren't you tired of that ridiculous
dance? Well, that's why we have ``@oemeth``

Usage
-----

``@oemeth`` is a method decorator that takes 2 (optional, default to ``False``) arguments:
``single`` and ``browse``. By default, it simply makes sure that ``ids`` is a list:

.. code-block:: python

    from openerp_sane import oemeth

    # [...]

    @oemeth
    def myaction(self, cr, uid, ids, context=None):
        # Write code that assumes ids is a list

With ``single`` to ``True``, we enforce a single ``int`` id:

.. code-block:: python

    @oemeth(single=True)
    def myaction(self, cr, uid, objid, context=None):
        # objid is an ``int``.
        # WARNING: Use this only when you're sure that you'll only ever have single arguments.
        # If the input is a list with a len() != 1, an exception is raised.

With ``browse`` to ``True``, we wrap our id(s) in a ``self.browse()`` call:

.. code-block:: python

    @oemeth(browse=True)
    def myaction(self, cr, uid, objs, context=None):
        # objs is a list of browse records

Install
-------

You can't wait to start using it in your modules, right? openerp-sane can be installed from PyPI::

    $ pip install openerp-sane

When you use it in a module, you can document its dependency to it in your ``__openerp__.py``:

.. code-block:: python

    {
        # [...]
        'external_dependencies': {
            'python': ['openerp_sane'],
        },
        # [...]
    }

Bits of wisdom
--------------

Don't use ``single`` (which requires to always have exactly one id all the time) on ``on_change``
methods. Sure, most of the time you get a single id, but if your call is made on a record that
isn't committed yet, you will get zero ids, which will raise an exception. In the future, maybe the
``single`` mode will support zero ids situations.
