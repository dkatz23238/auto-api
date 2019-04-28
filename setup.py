from setuptools import setup, find_packages

setup(name='autoapi',
      version='0.1',
      description='Automatically generate code for a backend rest API',
      long_description='Automatically generate code for a backend rest API',
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
      ],
      keywords='api code-generation json flask',
      url='http://github.com/storborg/funniest',
      author='David Katz',
      author_email='davidemmanuelkatz@gmail.com',
      license='MIT',
      packages=find_packages(),
      install_requires=[
          'jinja2', 'oyaml', 'pyyaml'
      ],
      include_package_data=True,
      zip_safe=False)
