# unitclass

`unitclass` is a physical unit class suitable for calculations in the sciences.
This library provides a `Unit` class that encapsulates a numerical value with a
physical unit. It is intended for both interactive and library use.

`unitclass` supports all [SI
units](https://www.nist.gov/pml/owm/metric-si/si-units) and prefixes, as well as
every reasonably common English/Imperial unit and other special units (e.g.
bytes and ppm).

## Usage Examples

`Unit()` takes strings or numbers and strings. Any number appended to a unit is
assumed to be an exponent. e.g. `m2` is `m²` and `in3` is `in³`. You can create
compound units with `*` and `/` operators, e.g. `N*m` or `ft/min`. There should
only be one division operator in a unit, but you can have any number of
multiplied units on the left and right sides of the division operator. e.g
`N*s2/m*kg` is interpreted as $\frac{N \cdot s^2}{m \cdot kg}$.

### Basic Usage

```python
>>> from unitclass import Unit
>>> Unit('1 in') # number and unit in a string
1 in
>>> Unit(1.0, 'in') # number and unit as separate arguments
1 in
>>> Unit(1, 'in', 'mm') # convert on-the-fly from one unit to another
25.4 mm
>>> a = Unit(1, 'in')
>>> b = Unit(1, 'ft')
>>> a*12 + b
24 in

```

#### Exponents

```python
>>> from unitclass import Unit
>>> Unit('1 m3')
1 m³
>>> Unit('1 in4')
1 in⁴
>>> Unit('1 m3').to('in3')
61023.7 in³
>>> Unit('10 in2') / Unit('1 in')
10 in

```

#### Compound Units

```python
>>> Unit('1 lbf*ft*s2')
1 lb·ft·s²
>>> Unit(100, 'ft/min')
100 ft/min
>>> Unit('1 N*s2/(m*kg)')
1 N·s²/(m·kg)
>>> Unit(100, 'ft') / Unit(1, 'min')
100 ft/min

```

#### Conversion

```python
>>> from unitclass import Unit
>>> Unit(1, 'in', 'mm') # convert on-the-fly from one unit to another
25.4 mm
>>> b = Unit(1, 'ft')
>>> b.to('in') # convert method
12 in
>>> b.to('mm')
304.8 mm
>>> Unit('1 N*m').to('in*lb')
8.85075 in·lb
>>> Unit(100, 'ft/min').to('mph') 
1.13636 mph
>>> Unit(100, 'ft/min').to('kph')
1.8288 kph

```

### Listing/Searching Built-in Units

To see what units are available (output is abbreviated below):

```python
>>> import unitclass as uc
>>> uc.list_units()
s     ->unit of time       aliases: ['second', 'seconds', 'sec', 'secs']
    ...

```

You can also limit the search to a certain quantity:

```python
>>> import unitclass as uc
>>> uc.list_units(qty='data')
B     ->unit of data       aliases: ['byte', 'bytes']
KB    ->unit of data       aliases: ['kilobyte', 'kilobytes']
MB    ->unit of data       aliases: ['megabyte', 'megabytes']
GB    ->unit of data       aliases: ['gigabyte', 'gigabytes']
TB    ->unit of data       aliases: ['terabyte', 'terabytes']
PB    ->unit of data       aliases: ['petabyte', 'petabytes']
EB    ->unit of data       aliases: ['exabyte', 'exabytes']

```

*Tip: For a list of available quanities, use the function `list_quantities()`.
Example usage is below in the Custom Unit section.*

And you can search for a certain string in a unit or unit alias:

```python
>>> import unitclass as uc
>>> uc.list_units(qty='data', search='ga')
MB    ->unit of data       aliases: ['megabyte', 'megabytes']
GB    ->unit of data       aliases: ['gigabyte', 'gigabytes']
>>> uc.list_units(search='mile')
mi    ->unit of length     aliases: ['mile', 'miles', 'statutemile', 'statutemiles', 'smi']
nmi   ->unit of length     aliases: ['nauticalmile', 'nauticalmiles']
gmi   ->unit of length     aliases: ['geographicalmile', 'geographicalmiles']
mph   ->unit of speed      aliases: ['mileperhour']

```

### Simplifying and Expanding Units

The `expand()` method expands the unit to its fundamental units while
`simplify()` combines units to a single compound unit if one exists for the
given combination of units. For all options, type `help(Unit.expand)` or
`help(Unit.simplify)` at an interactive prompt.

```python
>>> a = Unit('1 W')/Unit('1 A')
>>> a
1 W/A
>>> a.expand()
1 m²·kg/(A·s³)
>>> a.simplify()
1 V

```

### Add Custom Unit

In the example below, a custom unit is being added. The unit measures the
quantity "length", the unit is called "blake", two aliases for that unit are
"blakes" and "bunits", and 1 blake equals 6 ft.

The fields are as follows: `<quantity>, <name>, <aliases>, <factor>, <factor unit>`

Once the custom unit is added, it can be used the same as any other built-in unit.

```python
>>> import unitclass as uc
>>> uc.add_unit("length", "blake", "blakes bunits", 6, 'ft')
>>> c = Unit(12, 'in', 'blakes')
>>> c
0.166667 blake
>>> Unit(12*12, 'in', 'blakes')
2 blake

```

You can also bulk load custom units from a CSV file. The CSV would take the same
form as the `add_unit()` function above. Here is an example CSV with two custom
units:

```csv
length, myin, myinch my_inch, 1/8.0, in
angle, myang,, 1/1e-12*sin(2*pi), rad
```

And then it is loaded with the `import_units()` method:

```python
>>> import unitclass as uc
>>> uc.import_units('customunits.csv')

```

When adding custom units, it is helpful to know what *quantities* are available.
(E.g. length, time, force, etc.) These are the quantities that are being
measured, or the categories of measurement, not the units themselves. To list
them all, use the `list_quantities()` method (the output has been abbreviated
below):

```python
>>> import unitclass as uc
>>> uc.list_quantities()
absorbed_dose
acceleration
amount
angle
angular speed
area
    ...
speed
time
torque
unitless
voltage
volume

```

### Converting without using the Unit class

You can skip creating a Unit class if you prefer to just do a quick conversion.

```python
>>> import unitclass as uc
>>> uc.convert(1, 'in', 'mm')
25.4
>>> uc.convert(55, 'mph', 'kph')
88.51391999999998
>>> uc.convert(40, 'lb/ft3', 'kg/m3')
640.7385327602261

```

## Caveats

### Force/Mass

Because people expect to convert from pounds to kilograms (i.e. force to mass), this library
will automatically handle conversion to/from forces and masses when explicit conversion is requested. This is accomplished by dividing or multiplying by the acceleration of gravity as needed, which makes conversion between force and mass intuitive for the layman
and convenient for the rest.

### Temperature

Because of the nature of the temperature scales, a simple multiplier does not
work, so temperature is handled independently of the other units. This leads to
a the limitations that you cannot have custom or compound units with
temperature. This is a rare use case, so fixing this limitation is a low
priority.
