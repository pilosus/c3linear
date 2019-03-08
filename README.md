# C3 Linearization Algorithm

`c3linear` is a naïve implementation of 
[C3 linearization](https://en.wikipedia.org/wiki/C3_linearization) algorithm. 
It's used in Python 2.3+ for [Method Resolution Order](https://www.python.org/download/releases/2.3/mro/). 
See Raymond Hettinger's [Python’s super() considered super!](https://rhettinger.wordpress.com/2011/05/26/super-considered-super/) for more information.

# About implementation

The recursive implementation can be found at `c3linear.mro.mro`. 
It used an auxiliary function `_merge` as well as a bunch of classes 
to help with algorithm's readability.

# Motivation

The project's come to life as a byproduct of debugging 
an overcomplicated hierarchy of mixin classes. 
I thought I knew how exactly MRO is computed, but it turned out I didn't.

I've tried to keep the code idiomatic and easy to follow 
at the expense of performance. 
The project is really took a couple of hours to complete. 
Although I didn't care about time complexity and 
didn't check correctness as thoroughly as I should, 
I think the project may help someone who want to learn how 
Python's Method Resolution Order works.

# Usage

## Library

* Get the code and install it with `python setup.py install` (Python 3.6+ required)
* Import `from c3linear.mro import mro`
* Check against built-in MRO:
```python
>>> class A: pass
>>> class`B(A): pass
>>> mro(B) == B.mro()
True 
``` 

Take a look at `tests` for more examples.

## Testing

* Install dependencies:
```shell
pip install -e .
```
* (Optional) Install extra packages:
```shell
pip install -e .[extra]
```
* Run tests with:
```shell
python setup.py test
```
* Run `flake8` for PEP8 compliance testing:
```shell
python setup.py flake8
```
* Run `mypy`:
```shell
mypy c3linear/
```

# Contributing

If you've found a bug, please open an issue describing the problem first.


# Licence

The project is licensed under MIT License. For further information see
`LINCENSE` file.
