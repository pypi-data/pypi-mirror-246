from setuptools import setup,find_packages

setup(
  name='mindpype',
  version='0.1.0',
  author='Nicolas Ivanov, Aaron Lio',
  author_email='nicolas.ivanov94@gmail.com',
  description='A library for building BCI data processing pipelines.',
  packages=['mindpype'],
  install_requires=['matplotlib==3.5.2', 
                    'more-itertools==8.2.0',
                    'numpy==1.22.4',
                    'numpydoc==0.9.2',
                    'pyriemann==0.2.7',
                    'scikit-learn==1.1.1',
                    'scipy==1.8.1',
                    'pylsl==1.14.0',
                    'pyxdf==1.16.4',
                    'liesl==0.3.5.0',
                    'mne==1.4.2'],
  classifiers=[
      'Programming Language :: Python :: 3',
      'License :: OSI Approved :: BSD License',
      'Operating System :: OS Independent',
      'Intended Audience :: Science/Research',
      'Topic :: Scientific/Engineering :: Human Machine Interfaces',
    ],
  python_requires='>=3.8'
)
