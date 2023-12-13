from distutils.core import setup
import setuptools

readme = open('README.md').read()
license = open("license.txt").read()
packages = ['zscTest'] # 唯一的包名，自己取名
setup(name='zscTest',
    version='1.0.0',
    author='zhengshuchan',
    packages=packages,
    description='the utils',
    long_description=readme,
    author_email='749887528@qq.com',
    include_package_data=True,
    python_requires=">=3.7",
    license=license
    )