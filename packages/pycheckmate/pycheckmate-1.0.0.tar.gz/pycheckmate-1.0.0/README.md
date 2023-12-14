# pycheckmate

pycheckmate is a library designed to analyze Python code for various properties, focusing primarily on the evaluation of code authored by programming novices.


## Installation

pycheckmate requires at least the following Python packages:

* python >= 3.9 (only for method `print_ast`)
* ast

# Documentation

The documentation for the latest pycheckmate is currently in progress.


## Example Usage
```
from pycheckmate import PyCheckMate

#store code as str in variable source_code
with open("testing_file.py") as file:
    source_code = file.read()

reqs_args = {
    'param1': { 'default': 0 },
    'param2': { 'type': int }
}

pcm = PyCheckMate(source_code) 

check_func_name = pcm.has_function("test_function")
# check_func_name is a dictionary, could be for example:
#{'passed': True, 'note': "Function 'test_function' found."}

check_func_params = pcm.function_has_parameters("test_function", required_args=reqs_args, required_vararg=False, required_kwarg="kwarg")
# check_func_params is a dictionary, could be for example:
#{'passed': False, 'note': 
    "Parameter 'param1' of function 'test_function' is completly missing.
    Parameter 'param2' of function 'test_function' is of wrong type, expected '<class 'int'>', got 'None'..
    Your function has a parameter to pass a variable number of arguments to the function. Here you are not allowed to use this type of parameter.
    Your function is missing a parameter to pass a variable number of keyworded arguments to the function."}
```

## Testing


```
python -m unittest discover tests "*_tests.py"
```