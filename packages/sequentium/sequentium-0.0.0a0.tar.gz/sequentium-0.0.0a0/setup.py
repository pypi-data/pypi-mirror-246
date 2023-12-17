from setuptools import setup, find_namespace_packages

from sequence import __version__

setup(
  name='sequentium',
  version=f'{__version__}',
  license='MIT',
  author='Vasco Schiavo',
  author_email='vasco.schiavo@protonmail.com',
  url='https://github.com/VascoSch92',
  description='A package to work with sequences',
  packages=find_namespace_packages(include=['sequence*'], exclude=['tests']),
  entry_points={
        'console_scripts': ['sequence=sequence:main']
    },
  download_url='https://github.com/user/reponame/archive/v_01.tar.gz',
  keywords=['MATH'],   # Keywords that define your package best
  classifiers=[
    'Development Status :: 1 - Planning',
    'Intended Audience :: Education',
    'Intended Audience :: End Users/Desktop',
    'Intended Audience :: Science/Research',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    'Programming Language :: Python :: 3.11',
    'Programming Language :: Python :: 3.12',
    'Topic :: Education',
    'Topic :: Scientific/Engineering :: Mathematics',
  ],
)

