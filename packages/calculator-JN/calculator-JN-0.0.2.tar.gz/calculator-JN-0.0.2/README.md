# Calculator
## Overview
This Calculator is a simple Python class designed to perform basic arithmetic operations including addition, subtraction, multiplication, and division. It can also calculates the n-th root of a number and reset the current result.
## Features
- Basic Arithmetic Operations: Perform addition, subtraction, multiplication, and division.
- N-th Root Calculation: Calculate the n-th root of the current result.
- Reset Memory: Calculator has its own memory and it manipulates its starting number 0 until it is reset.
- Input Validation: Validates all inputs to ensure they are numeric.
- Error Handling: Handles invalid root calculations when the root is even and the number is negative
## Installation
This package has been uploaded on PyPI and you can install it using pip
```
pip install calculator-JN
```
## Usage
### Initialization
Create an instance of the Calculator class:
```
from calculator import Calculator
calc = Calculator()
```

### Performing Operations
You can perform arithmetic operations as follows:
```
result = calc.add(5)
result = calc.subtract(2)
result = calc.multiply(3)
result = calc.divide(4)
result = calc.n_root(2)
```
### Resetting the Calculator
Reset the calculator to its initial state:
```
calc.reset()
```
## Requirements
Python 3.x
## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
