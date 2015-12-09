from setuptools import setup

setup(name='govlab-static-tools',
      version='0.1',
      description='Tools for GovLab static site generation',
      url='http://github.com/govlab/govlab-static-tools',
      author='Atul Varma',
      author_email='varmaa@gmail.com',
      license='MIT',
      install_requires=[
          'colorama',
          'staticjinja',
          'argh',
      ],
      packages=['govlabstatic'],
      zip_safe=False)
