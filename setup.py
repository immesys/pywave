from setuptools import setup

setup(
  name="wave3",
  version="3.0.0",
  packages=['wave3'],
  license="GPLv3",
  install_requires=[
    "grpcio-tools",
    "googleapis-common-protos",
  ]
)
