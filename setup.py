from setuptools import setup, find_packages

setup(
    name='QuantumShield-LWE',
    version='0.1.0',
    author='pywitcher',
    author_email='seyyed.fazel.ebrahimi@gmail.com',
    description='Advanced multi-block LWE cryptosystem with innovative noise and block matrix structure',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/pywitcher/QuantumShield-LWE-cryptography',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'numpy>=1.21',
        'scipy>=1.7',
    ],
    python_requires='>=3.8',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
