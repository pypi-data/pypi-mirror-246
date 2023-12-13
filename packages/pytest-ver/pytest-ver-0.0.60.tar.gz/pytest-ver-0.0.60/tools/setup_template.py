from setuptools import setup
from setuptools import find_packages

print('version:  v', '$$version$$')
print('module : ', '$$mod_dir_name$$')

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
        '$$classifier_license$$',
    ],

    # common attributes from here on
    name='$$mod_name$$',
    # TODO delete; package_dir={'': '$$root_dir$$/$$mod_dir_name$$'},
    packages=find_packages(include=f'$$root_dir$$/$$mod_dir_name$$*', ),
    include_package_data=True,
    exclude_package_data={f'$$root_dir$$/$$mod_dir_name$$/lib': ['.gitignore']},
    version='$$version$$',
    license='$$license$$',
    long_description='$$long_desc$$',
    long_description_content_type='$$long_desc_type$$',
    author='$$author$$',
    author_email='$$email$$',
    url='$$homepage_url$$',
    download_url='$$download_url$$',
)
# @formatter:on
