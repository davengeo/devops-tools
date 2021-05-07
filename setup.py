from setuptools import setup

setup(
    author="David Navarro Alvarez",
    author_email="me@davengeo.com",
    description="devops base library dist",
    url="https://github.com/davengeo/devops-tools",
    name="devops-tools-daven",
    version='0.0.7',
    packages=[
        'devopstoolsdaven',
        'devopstoolsdaven.reports',
        'devopstoolsdaven.common',
        'devopstoolsdaven.templates',
        'devopstoolsdaven.utils'
    ],
    install_requires=[
        'argparse',
        'chevron',
        'cloudevents',
        'json-spec',
        'invoke',
        'pyramda',
        'datasette',
        'PyYAML',
        'fluent-logger',
        'prometheus-client'
    ],
    package_data={
        'config': ['config/templates/hello_world.mustache', 'config/example/example.json'],
        'ini': ['app.ini']
    },
    include_package_data=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: European Union Public Licence 1.2 (EUPL 1.2)',
        'Programming Language :: Python :: 3.8',
        'Topic :: System :: Systems Administration',
    ]
)
