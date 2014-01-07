from setuptools import setup

setup(
    name = "openerp-sane",
    version = "0.1",
    url = "https://github.com/savoirfairelinux/openerp-sane",
    py_modules = ['openerp_sane'],
    author="Savoir-faire Linux",
    author_email="virgil.dupras@savoirfairelinux.com",
    description="Small utilities to ease OpenERP development",
    long_description=open('README.rst', 'rt').read(),
    license="AGPL",
)
