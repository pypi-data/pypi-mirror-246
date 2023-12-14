from setuptools import setup

setup(
    name='jwtauthenticatortest1',
    version='1.0.1',
    license='Apache 2.0',
    packages=['jwtauthenticatortest1'],
    install_requires=[
        'jupyterhub',
        'pyjwt',
    ]
)
