[![banner](https://raw.githubusercontent.com/oceanprotocol/art/master/github/repo-banner%402x.png)](https://oceanprotocol.com)

# osmosis-aws-driver

> 💧 Osmosis Data S3 Driver Implementation
> [oceanprotocol.com](https://oceanprotocol.com)


[![Build Status](https://travis-ci.com/oceanprotocol/osmosis-aws-driver.svg)](https://travis-ci.com/oceanprotocol/osmosis-aws-driver)
[![PyPI](https://img.shields.io/pypi/v/osmosis-aws-driver.svg)](https://pypi.org/project/osmosis-aws-driver/)
[![GitHub contributors](https://img.shields.io/github/contributors/oceanprotocol/osmosis-aws-driver.svg)](https://github.com/oceanprotocol/osmosis-aws-driver/graphs/contributors)

---
## Table of Contents

  - [Quickstart](#quickstart)
  - [Code style](#code-style)
  - [Testing](#testing)
  - [New Version](#new-version)
  - [License](#license)

---

## Quickstart

The application interacts with AWS API using boto3 library, so you need to configure your system in order to boto3 can
login as described in https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html.
At the moment there is only a first implementation for the data_plugin, but in the future is going to be an instance
for the computing plugin as well.

boto3 is used to manage the credentials. Therefore, no configuration options need to be specified in the config dictionary.

boto3 will load the credentials from your system [(see the boto documentation)](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html).

## Code style

The information about code style in python is documented in this two links [python-developer-guide](https://github.com/oceanprotocol/dev-ocean/blob/master/doc/development/python-developer-guide.md)
and [python-style-guide](https://github.com/oceanprotocol/dev-ocean/blob/master/doc/development/python-style-guide.md).
    
## Testing

Automatic tests are setup via Travis, executing `tox`.
Our test use pytest framework.

## New Version

The `bumpversion.sh` script helps to bump the project version. You can execute the script using as first argument {major|minor|patch} to bump accordingly the version.

## License

```
Copyright 2018 Ocean Protocol Foundation Ltd.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
