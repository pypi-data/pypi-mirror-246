from distutils.core import setup
from setuptools import find_packages

with open("README.MD", "r") as f:
  long_description = f.read()

setup(name='my_awesome_package1',  # 包名
      version='0.4.0',  # 版本号
      description='A small example package',
      long_description=long_description,
      author='mike_talk',
      author_email='762357658@qq.com',
      url='',
      install_requires=[],
      license='MIT License',
      packages=find_packages(),
      platforms=["all"],
      classifiers=[
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Natural Language :: Chinese (Simplified)',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Topic :: Software Development :: Libraries'
      ],
      )
