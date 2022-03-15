# Decorators
Every language calls this something different. In C#, 
they're known as `Attributes`, or in Java they're called `Annotations`.

In Python a decorator is used to extend something without
actually modifying the function itself. 

Lets start off with some boilerplate code. Right now we have a 
simple function performing addition and returning the result.
```python
def add(a: int, b: int) -> int:
    return a + b

add(2,3)
```

What if... for whatever reason we wanted to print/log 
the parameters utilized in this function? 

```python
def add(a: int, b: int) -> int:
    print(a, b)
    return a + b

add(2,3)

# outputs: 2 3
```

That's one way to do it... right? However, what if we want to do this for every function? Do we copy that 
print method for each function? 

```python
def add(a: int, b: int) -> int:
    print(a,b)
    return a + b

def sub(a: int, b: int) -> int:
    print(a,b)
    return a - b

add(2,3)
sub(3,2)
```

To be honest... our print statements aren't all that useful because we don't know what those
values are associated with. How do you know 2 and 3 were used for the addition function? One way is to add
the function name in the print output... let's dive into decorators.

```python
from functools import wraps

def log(func): # this function name is what we'll use as our decorator
    @wraps(func)
    def wrapper_func(*args, **kwargs): # the function we are 'decorating' -- its args/kwargs are passed into here
        output = ""
        
        # Takes each positional arguments and puts it into a formatted output as position: value
        for x in range(len(args)):
            output += f"\tPositional Arg {x}: {args[x]}\n"
        
        # Takes each keyword argument and puts it into a formatted output as key: value
        for key, value in kwargs.items():
            output += f"\t{key}: {value}\n"
        
        print(f"Executing '{func.__name__}' with:\n{output}")
        func(*args, **kwargs) # this executes the function we're 'decorating'
        print("-"*25)
    return wrapper_func
```

In action, we can use `@log` to add this extended behavior!

```python
@log
def add(a: int, b: int) -> int:
    return a + b
```

```
Executing 'add' with:
	Positional Arg 0: 1
	Positional Arg 1: 2

-------------------------
```

Another example of `@log` in action
```python
@log
def create_user(name: str, age: int) -> dict:
    return {
        "name": name,
        "age": age
    }

create_user("badger 2-3", 29)
create_user(age=29, name="Badger 2-3")
```

```
Executing 'create_user' with:
	Positional Arg 0: badger 2-3
	Positional Arg 1: 29

-------------------------
Executing 'create_user' with:
	age: 29
	name: Badger 2-3

-------------------------
```

-----
# Log Execution Time

We can take the decorator approach and calculate how long it took to execute
our decorated function!

```python
from functools import wraps
from time import time
def log_time(func):
    @wraps(func)
    def wrapper_func(*args, **kwargs):
        start = time()
        func(*args, **kwargs)
        print(f"'{func.__name__}' took %s seconds" %((time()-start)*1000))
    return wrapper_func

@log_time
def add(a: int, b: int) -> int:
    return a + b

add(123,123)
```

```
'add' took 0.0016689300537109375 seconds
```