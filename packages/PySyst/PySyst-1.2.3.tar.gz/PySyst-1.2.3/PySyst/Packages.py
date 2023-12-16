# PySyst - Packages

''' This is the "Packages" module. '''

'''
Copyright 2023 Aniketh Chavare

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

# Imports
import requests
import pkg_resources
import importlib_metadata
from bs4 import BeautifulSoup

# Function 1 - List Packages
def list_packages(language):
    # Variables
    languages = ["python"]

    # Checking the Data Type of "language"
    if (isinstance(language, str)):
        # Checking the Value of "language"
        if (language in languages):
            # Returning the List of Packages Installed
            return sorted(["%s==%s" % (package.key, package.version) for package in pkg_resources.working_set])
        else:
            raise Exception("The 'language' argument must be a valid programming language's name. The available languages are: " + str(languages))
    else:
        raise TypeError("The 'language' argument must be a string.")

# Class 1 - Python
class Python:
    # Function 1 - Init
    def __init__(self, name):
        # Checking the Data Type of "name"
        if (isinstance(name, str)):
            # Try/Except - Checking if Package Exists
            try:
                # Assigning the Variable
                package_metadata = importlib_metadata.metadata(name)
            except importlib_metadata.PackageNotFoundError:
                # Raising an Error
                raise Exception("No package metadata was found for {0}.".format(name))

            # Specifying and Declaring the Attributes
            for i in package_metadata:
                exec("self.{0} = package_metadata.get('{1}')".format(i.replace("-", "_").lower(), i))
        else:
            raise TypeError("The 'name' argument must be a string.")

    # Function 2 - Get Attributes
    def get_attributes(self):
        # Returning the List of Attributes' Keys
        return list(vars(self).keys())

    # Function 3 - Get Versions
    def get_versions(self):
        # Variables
        package_version = BeautifulSoup(requests.get("https://pypi.org/project/{0}".format(self.name)).text, "html.parser").body.main.find_all("div")[1].h1.text.strip().split()[1]

        # Returning the Dictionary
        return {
            "Latest": package_version,
            "Installed": self.version,
            "Upgrade Needed": self.version < package_version
        }