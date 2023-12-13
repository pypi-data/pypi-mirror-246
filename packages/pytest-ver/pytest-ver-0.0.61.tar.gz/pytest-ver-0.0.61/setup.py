from setuptools import find_packages
from setuptools import setup

print('     setup: version:  v0.0.61')
print('     setup: module :  pytest_ver')

# @formatter:off
setup(
    description='Pytest module with Verification Protocol, Verification Report and Trace Matrix',
    keywords=['verification', 'pytest'],
    install_requires=[
        'docx',
        'jsmin',
        'pytest',
        'pytest-check',
        'python-docx',
        'reportlab',
    ],
    classifiers=[
        # Choose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable"
        'Development Status :: 4 - Beta',
        'Framework :: Pytest',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing :: Acceptance',
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: MIT License',
    ],

    # common attributes from here on
    name='pytest-ver',
    packages=find_packages(include=f'./pytest_ver*', ),
    include_package_data=True,
    exclude_package_data={f'./pytest_ver/lib': ['.gitignore']},
    version='0.0.61',
    license='MIT',
    long_description='unknown',
    long_description_content_type='unknown',
    author='JA',
    author_email='cppgent0@gmail.com',
    url='https://bitbucket.org/arrizza-public/pytest-ver/src/master',
    download_url='https://bitbucket.org/arrizza-public/pytest-ver/get/master.zip',
)
# @formatter:on

print('     setup: done')
