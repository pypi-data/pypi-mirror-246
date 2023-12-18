from setuptools import setup, find_packages
import pathlib

dependencies = ['numpy']
version = '2.12.5'

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / 'README.md').read_text(encoding='utf-8')
setup(
    name='netwk',
    version=version,
    description='Create fast, optimized, and easy-to-use neural networks.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/flowa-ai/netwk',
    author='flowa.ai',
    author_email='flowa.dev@gmail.com',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Scientific/Engineering :: Mathematics',
    ],
    keywords='network, machine learning, ai, neural network',
    packages=find_packages(),
    install_requires=dependencies,
    python_requires='>=3.6',
)