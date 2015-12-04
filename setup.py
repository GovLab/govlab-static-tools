from setuptools import setup

setup(name='govlab-static-tools',
      version='0.1',
      description='Tools for GovLab static site generation',
      url='http://github.com/govlab/govlab-static-site-tools',
      author='Atul Varma',
      author_email='varmaa@gmail.com',
      license='MIT',
      install_requires=[
          'colorama',
          'staticjinja',
      ],
      packages=['govlabstatic', 'govlabstatic.script'],
      zip_safe=False)
