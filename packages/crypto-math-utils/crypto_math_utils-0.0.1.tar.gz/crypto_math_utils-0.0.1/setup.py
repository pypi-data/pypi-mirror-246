from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 11',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='crypto_math_utils',
  version='0.0.1',
  description='Computes the coefficient of Bezouts identity',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Pratyush Prasad Sahoo',
  author_email='prats.sahoo2k22@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='gcd bezouts euclidean', 
  packages=find_packages(),
  install_requires=[''] 
)