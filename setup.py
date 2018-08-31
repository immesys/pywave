from setuptools import setup

setup(
  name="wave",
  version="3.0.0",
  packages=['wave'],
  license="GPLv3",
  install_requires=[
    "grpcio-tools",
    "googleapis-common-protos",
  ]
)
