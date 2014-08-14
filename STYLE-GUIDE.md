### Indentation

4 spaces

```python
```
    ```python
    def function():
        do_stuff()
    ```

### Variable names

* A single word is best. Use underscores for multiple word variable names, unless defining a class name

    ```python
    telephone_number = 8675309

    class MyClass(object):
    ```

* Lists should be a plural word

    ```python
    # good:
    var animals = ['cat', 'dog', 'fish']

    # bad:
    var animal = ['cat', 'dog', 'fish']

    # worse:
    var animalList = ['cat', 'dog', 'fish']
    ```

* Name your variables after their purpose, not their structure

    ```python
    # good:
    var animals = ['cat', 'dog', 'fish']

    # bad:
    var array = ['cat', 'dog', 'fish']
    ```


### Language constructs

* Focus on using built in python methods. As a general rule, if you're doing `range(len(foo))`, you're doing it wrong.

    ```python
    # good:
    for obj, arg in zip(objects, fn_args):
        obj.do_stuff(arg)

    # bad:
    for i in range(len(objects)):
        objects[i].do_stuff(fn_args[i])

    ```

### Minor Points

* Never use semicolons.

* Use single quotes

* No global variables.

* For lists, put commas at the end of each newline, not at the beginning of each item in a list

    ```python
    # good:
    animals = [
      'ape',
      'bat',
      'cat'
    ]

    # bad:
    animals = [
        'ape'
      , 'bat'
      , 'cat'
    ]
    ```


### Code density

* Conserve line quantity by minimizing the number lines you write in. The more concisely your code is written, the more context can be seen in one screen.
* Conserve line length by minimizing the amount of complexity you put on each line. Long lines are difficult to read. Rather than a character count limit, I recommend limiting the amount of complexity you put on a single line. Try to make it easily read in one glance. This goal is in conflict with the line quantity goal, so you must do your best to balance them.
* When needed, long lines should be split with backslashes

### Comments

* Code should read like English
* Provide comments any time you are confident it will make reading your code easier.
* Comment on what code is attempting to do, not how it will achieve it.
* A good comment is often less effective than a good variable name.
* Long functions/methods should be summarized at the top of their definition as is custom.

### Padding & additional whitespace

* You may use it as padding for visual clarity. If you do though, make sure it's balanced on both sides.

    ```python
    # optional:
    do_stuff( 'I chose to put visual padding around this string' )

    # bad:
    do_stuff( 'I only put visual padding on one side of this string')
    ```

* When there are multiple conditions in an if statement, group them explicitly

    ```python
    # good:
    if (condition1 and condition2) or condition3:

    # too much:
    if (condition1 and condition2):

    ```

* You may use spaces to align two similar lines, but it is not recommended.

    ```python
    # discouraged:
    firstItem  = getFirst()
    secondItem = getSecond()

    # why??:
    firstItem = getFirst  ()
    secondItem = getSecond()
    ```

* Don't put an if block's definition on the same line as the condition unless it contains no logic.
    ```python

    # fine:
    if is_prime: continue

    # bad:
    if very_long_var_name is not some_other_var: do_this_stuff() or do_this_other_stuff()

    ```

* End files with a newline.
* Don't have trailing whitespace in lines.




