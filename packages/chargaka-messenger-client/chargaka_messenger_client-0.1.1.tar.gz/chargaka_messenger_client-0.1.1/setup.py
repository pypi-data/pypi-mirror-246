from setuptools import setup, find_packages

setup(name="chargaka_messenger_client",
      version="0.1.1",
      description="chargaka_messenger_client",
      author="Artem",
      author_email="warload22@gmail.com",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
