from distutils.core import setup

setup(
    name='ormx',
    packages=['ormx'],
    version='0.1.4.11',
    license='MIT',
    description='SQLite3 ORM package',
    author='Murodov Azizmurod',
    author_email='murodovazizmurod@gmail.com',
    url='https://murodovazizmurod.github.io/ormx/',
    download_url='https://github.com/murodovazizmurod/ormx/archive/v_01.tar.gz',
    keywords=['ormx', 'orm', 'python-orm', 'python'],
    install_requires=[
        'prettytable'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
