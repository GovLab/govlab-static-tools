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
          'argh',
          'pylinkchecker',
      ],
      dependency_links=[
          'git+git://github.com/mtlevolio/pylinkchecker.git#egg=pylinkchecker'
      ],
      packages=['govlabstatic'],
      zip_safe=False)
