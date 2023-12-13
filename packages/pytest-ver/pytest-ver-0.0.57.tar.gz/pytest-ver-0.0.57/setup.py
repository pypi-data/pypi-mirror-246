# TODO delete; from setuptools import find_packages
from setuptools import setup

from tools import main
from tools.debug_logger import DebugLogger as log

main.init()
log.start(f'{"version": <11}: v{main.Common.version}')
log.line(f'{"module": <11}: {main.Common.mod_dir_name}')

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
        main.Common.classifier_license,
    ],

    # common attributes from here on
    name=main.Common.mod_name,
    package_dir={'': main.Common.mod_dir_name},
    # TODO delete; packages=find_packages(include=f'{root_dir}/{main.Common.mod_dir_name}*', ),
    # TODO delete; include_package_data=True,
    exclude_package_data={f'{main.root_dir}/{main.Common.mod_dir_name}/lib': [".gitignore"]},
    version=main.Common.version,
    license=main.Common.license,
    long_description=main.Common.long_desc,
    long_description_content_type=main.Common.long_desc_type,
    author=main.Common.author,
    author_email=main.Common.email,
    url=main.Common.homepage_url,
    download_url=main.Common.download_url,
)
# @formatter:on

log.ok('setup completed successfully')
