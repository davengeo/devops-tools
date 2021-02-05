from setuptools import setup

setup(
    author="David Navarro Alvarez",
    author_email="me@davengeo.com",
    description="devops base library dist",
    url="https://github.com/davengeo/",
    name="devops-tools",
    packages=[
        'devops',
        'devops.reports',
        'devops.common'
    ],
    install_requires=['chevron, cloudevents, json-spec, invoke'],
)
