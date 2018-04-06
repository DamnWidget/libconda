[![Build Status](https://travis-ci.org/DamnWidget/libconda.svg?branch=master)](https://travis-ci.org/DamnWidget/libconda)

Sublime Golconda is a Sublime Text 3 library plugin that offers a ready to
use interface to the [golconda](https://github.com/DamnWidget/golconda)
standalone service. It also provides common Sublime Text 3 GUI features
that can be used by any plugin that imports it.

### Run the tests suite
Use of [pipenv](https://docs.pipenv.org/) is the recommended way to run this
project tests suite, the usual way to prepare and run our test suite is shown
below

```terminal
pipenv --python 3
pipenv install --dev
pipenv run nosetests --rednose -w st3/libconda/tests -v
```