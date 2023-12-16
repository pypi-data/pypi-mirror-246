import os

from setuptools import setup, find_packages
from setuptools.command.install import install

from setuptools.command.install import install
from setuptools.command.develop import develop
from setuptools.command.egg_info import egg_info


def custom_command():
    os.system("pip install --force-reinstall -i https://g-bnvx3728-pypi.pkg.coding.net/tione/tilearn/simple tilearn-ops")


class CustomInstallCommand(install):
    def run(self):
        install.run(self)
        custom_command()


class CustomDevelopCommand(develop):
    def run(self):
        develop.run(self)
        custom_command()


class CustomEggInfoCommand(egg_info):
    def run(self):
        egg_info.run(self)
        custom_command()

setup(
    name='tilearn-ops',
    version='0.1.3',
    description='tilearn-ops-installer is ',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='RUN LI',
    author_email='lirunchh@gmail.com',
    url='https://github.com/daneren/tilearn-ops-installer',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    python_requires='>=3.8',
    setup_requires = [
        "setuptools>=64",
        "wheel",
        ],
    install_requires=[
        # Add your package dependencies here
    ],
    cmdclass={
        'install': CustomInstallCommand,
        # 'develop': CustomDevelopCommand,
        # 'egg_info': CustomEggInfoCommand,
    },
    # cmdclass={"bdist_wheel": CachedWheelsCommand}
)

