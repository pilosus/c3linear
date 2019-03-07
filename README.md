# C3 Linearization Algorithm

`c3linear` is a naïve implementation of 
[C3 linearization](https://en.wikipedia.org/wiki/C3_linearization) algorithm. 
It's used in Python 2.3+ for [Method Resolution Order](https://www.python.org/download/releases/2.3/mro/). 
See Raymond Hettinger's [Python’s super() considered super!](https://rhettinger.wordpress.com/2011/05/26/super-considered-super/) for more information.

# About implementation

The recursive implementation can be found at `c3linear.mro.mro`. 
It used an auxiliary function `_merge` as well as a bunch of classes 
to help with algorithm's readability.

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
*(Optional) Install extra packages:
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

# Contributing

The project is really took a couple of hours to complete. 
It's primarily intended as a little auxiliary material 
for teaching newbies what's MRO.

If you've found a bug, please open an issue describing the problem first.


# Licence

The project is licensed under MIT License. For further information see
`LINCENSE` file.
