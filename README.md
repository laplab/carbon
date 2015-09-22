## Carbon Engine
Originally developed for ACM contests but can be used in any other sphere of activity where program need to be compiled, executed and checked for the right answer to specified input.

### Requirements
* colorlog
* psutil
* Linux based OS (tested on Ubuntu 14.04)

### Security
For running untrusted code Carbon needs to be run by non-root user (this will not give permissions to program and engine will care about time and memory limits).

### Usage
An example can be found in `engine.py`. By running:
```bash
python engine.py
```
You will test simple python program with syntax error. Try to play around with code passed to Carbon and see the log output in console.

### Structure
* `engine.py` - Carbon Engine base class for testing programs.
* `errors.py` - All errors that can be throwed by Carbon.
* `helpers.py` - Helpers classes and functions such as `Map` class.
* `langs_config.py` - Just some examples of languages' configs.
* `process.py` - Class for running processes with limits.
* `program.py` - Class for running programs based on language config.

### ToDo
* Add length limit to STDOUT of program