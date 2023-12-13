# tabuletta

## <span style="color:#22b6e3">Installation</span>
Installing this library is super easy!

```python
    pip install tabuletta
```

## <span style="color:#22b6e3">Intro</span>
Tbuletta is a python library that print's arrays in a tabular form with some customisation.

## <span style="color:#22b6e3">Example</span>
This library is extremly simple, to use it make a list of lists, each inner list should be a row. The amount of elements in each inner list needs to be uniform.

For example,
```python
table = [
    [5, 2, 3.5],
    [4.1, 900, 2],
    ["Sup", 5, 1]
]
```

Will print:
```
+-----------------+
| 5   | 2   | 3.5 |
| 4.1 | 900 | 2   |
| Sup | 5   | 1   |
+-----------------+
```

It can also print:
```
+-----------------+
| 5   | 2   | 3.5 |
+-----+-----+-----+
| 4.1 | 900 | 2   |
| Sup | 5   | 1   |
+-----------------+
```

It's all your choice.

## <span style="color:#22b6e3">Using tabuletta</span>
To use tabuletta, simply import tabuletta after following the installation instructions from above
```python
import tabuletta
```

Then, create the list you would like to print
```python
myList = [
    ["Reg no", "Email"],
    ["20ABC1000", "John@fakeemail.com"],
    ["21BCD0001", "Wick@fakeemail.com"]
]
```

Then simply print it! Choose whether or not you would like field names (use <span style="color:#f79914">`True`</span> if so, don't put anything if not (don't include `useFieldNames` at all) because it defaults to `False`). 

```python
# NOTE: useFieldNames defaults to False, so, if you don't type useFieldNames=True it automatically goes to False
tabuletta.printTable(myList, useFieldNames=True)
```

As output, you get:

```
+-----------------------------------------------+
| Reg no                  | Email              |
+-----------------------+-----------------------+
| 20ABC1000               | John@fakeemail.com |
| 21BCD0001               | Wick@fakeemail.com |
+-----------------------------------------------+
```

If you didn't want to use field names then you would only have to write:

```python
tabuletta.printTable(myList)
```

Another example:
```python
myList = [
    ["", "a", "b"],
    ["x", "a + x", "a + b"],
    ["z", "a + z", "z + b"]
]
```
From that, you get:
```
+-----------------------+
|       | a     | b     |
+-------+-------+-------+
| x     | a + x | a + b |
| z     | a + z | z + b |
+-----------------------+
```

## Using colors
You might want to use colors in tabuletta. 

To use them simply use RGB values, so, using the example from above:

```python
import tabuletta

myList = [
    ["", "a", "b"],
    ["x", "a + x", "a + b"],
    ["z", "a + z", "z + b"]
]

# give the color name
tabuletta.printTable(myList, useFieldNames=True, color="red")
```

As output you get:

![](ImageInReadME/color_table1.png)

Some more examples of colors:

![](ImageInReadME/color_table2.png)

![](ImageInReadME/color_table3.png)

The available color options are : red, blue, orange, cyan, pink, green, yellow


