[![banner](https://raw.githubusercontent.com/oceanprotocol/art/master/github/repo-banner%402x.png)](https://oceanprotocol.com)

# osmosis-aws-driver

> 💧 Osmosis AWS Driver Implementation
> [oceanprotocol.com](https://oceanprotocol.com)

[![Build Status](https://travis-ci.com/oceanprotocol/osmosis-aws-driver.svg)](https://travis-ci.com/oceanprotocol/osmosis-aws-driver)
[![PyPI](https://img.shields.io/pypi/v/osmosis-aws-driver.svg)](https://pypi.org/project/osmosis-aws-driver/)
[![GitHub contributors](https://img.shields.io/github/contributors/oceanprotocol/osmosis-aws-driver.svg)](https://github.com/oceanprotocol/osmosis-aws-driver/graphs/contributors)

---

## Table of Contents

- [Setup](#setup)
- [Code Style](#code-style)
- [Testing](#testing)
- [New Version](#new-version)
- [License](#license)

---

## Setup

To use Amazon S3 storage with Brizo, you must set up some Amazon S3 storage and set some AWS configuration settings on the computer where Brizo is running. For details, see:

- [the README.md file in the Brizo repository](https://github.com/oceanprotocol/brizo/blob/develop/README.md) and
- [the tutorial about how to set up Amazon S3 storage for use with Ocean Protocol](https://docs.oceanprotocol.com/tutorials/amazon-s3-for-brizo/)

Alternatively, you can set the access keys/secret in environment variables as in the file `aws-access-env-vars`. 
 
## Code Style

Information about our Python code style is documented in the [python-developer-guide](https://github.com/oceanprotocol/dev-ocean/blob/master/doc/development/python-developer-guide.md)
and the [python-style-guide](https://github.com/oceanprotocol/dev-ocean/blob/master/doc/development/python-style-guide.md).

## Testing

Automatic tests are setup via Travis, executing `tox`.
Our tests use the pytest framework.

## New Version

The `bumpversion.sh` script helps to bump the project version. You can execute the script using as first argument {major|minor|patch} to bump accordingly the version.

## License

```text
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
```
