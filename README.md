## Carbon ![Unmaintained](https://img.shields.io/badge/status-unmaintained-red.svg)
Originally developed for ACM contests but can be used in any other sphere of activity where program need to be compiled, executed and checked for the right answer to specified input.

### Requirements
* colorlog
* psutil
* Linux based OS (tested on Ubuntu 14.04)

### Security
For running untrusted code Carbon needs to be run by non-root user (this will not give permissions to program and engine will care about time and memory limits).

### Installation
```bash
python setup.py install
```

### Usage
```python
import logging
from carbon.engine import Engine
from carbon.langs_config import py

# init engine with minimal logging level of DEBUG
en = Engine(logging.DEBUG)

# let's test some code for implementing sum of two integers
# and autoremove this file after testing
en.test_program('code.py', py, '4 5', '9', True)
```

### ToDo
* Add length limit to STDOUT of program
* Move from dicts to config classes
