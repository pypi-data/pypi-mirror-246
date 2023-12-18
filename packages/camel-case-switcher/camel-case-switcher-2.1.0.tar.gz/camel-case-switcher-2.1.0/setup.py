# noinspection PyProtectedMember
from setuptools import _install_setup_requires
_install_setup_requires(dict(setup_requires=[ 'extended-setup-tools' ]))

from extended_setup import ExtendedSetupManager
ExtendedSetupManager('camel_case_switcher').setup \
(
    short_description = "Python tool for changing style in name of functions etc. from camelCase/CamelCase to the snake_case.",
    min_python_version = '3.6',
    author_email='ussx.hares@yandex.ru',
    keywords=[ 'camel_case', 'strings', 'snake_case' ],
    classifiers =
    [
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: BSD License',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
        'Topic :: Text Processing',
    ]
)
