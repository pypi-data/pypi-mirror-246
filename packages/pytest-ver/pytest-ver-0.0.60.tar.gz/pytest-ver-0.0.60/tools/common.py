from dataclasses import dataclass


# --------------------
## holds all common variables for a module/app
@dataclass
class Common:
    ## the version string held in mod_dir_name/lib/version.json
    version = '0.0.60'
    ## the module name (with dashes)
    mod_name = 'pytest-ver'
    ## the local directory name for the module (with underscores)
    mod_dir_name = 'pytest_ver'
    ## flag indicating this is a python module (True) or an app (False)
    is_module = True

    # == typically do not change from here on

    ## the license for the module
    license = 'MIT'
    ## the license string for the classifier section
    classifier_license = 'License :: OSI Approved :: MIT License'
    ## the url for the homepage link
    homepage_url = f'https://bitbucket.org/arrizza-public/{mod_name}/src/master'
    ## the url for the download link
    download_url = f'https://bitbucket.org/arrizza-public/{mod_name}/get/master.zip'
    ## the author name
    author = 'JA'
    ## the contact email
    email = 'cppgent0@gmail.com'

    # == set in main.init()

    ## the long version of the version string
    long_version = 'unknown'
    ## the long description of the module (usually content of README)
    long_desc = 'unknown'
    ## the format of the long desc (usually markdown)
    long_desc_type = 'unknown'
