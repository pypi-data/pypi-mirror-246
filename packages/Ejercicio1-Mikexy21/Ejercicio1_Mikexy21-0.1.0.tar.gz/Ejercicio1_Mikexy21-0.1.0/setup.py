from setuptools import setup, find_packages


# leer el contenido de README.md
with open("README.md","r",encoding="utf-8") as fh:
    long_description = fh.read()


setup(
    name="Ejercicio1_Mikexy21",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[],
    author="Mikeee",
    description="Ejemplo 1",
    long_description=long_description,
    long_description_content_type="text/markdown")
