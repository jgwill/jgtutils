from setuptools import setup, find_packages

setup(
    name='jgtutils',
    version='0.1.3',
    packages=find_packages(),
    description='A utility package common to other JGT projects.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Guillaume Isabelle',
    author_email='jgi@jgwill.com',
    url='https://github.com/jgwill/jgtutils',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    keywords='utilities',
    project_urls={
        'Bug Reports': 'https://github.com/jgwill/jgtutils/issues',
        'Source': 'https://github.com/jgwill/jgtutils',
    },
)