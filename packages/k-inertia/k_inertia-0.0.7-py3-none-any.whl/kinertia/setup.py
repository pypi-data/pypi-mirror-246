from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Developers',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='k_inertia',
  version='0.0.1',
  description='K-Inertia: A User-Friendly Machine Learning Library K-Inertia or Kavish Inertia is a Python machine learning library designed for simplicity and ease of use. With a focus on user-friendly interfaces, K-Inertia provides implementations of various machine learning algorithms, including regression, logistic regression, k-nearest neighbors, naive Bayes, support vector machines, and k-means clustering.',
  long_description=open('README.md').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Kavish Tomar',
  author_email='kavishtomar2@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='machine learning, k_inertia, k-inertia, learning, ai, AI , ml, ML, K-Inertia, Machine Learning', 
  packages=find_packages(),
  install_requires=['numpy'],
  setup_requires=['numpy']
)