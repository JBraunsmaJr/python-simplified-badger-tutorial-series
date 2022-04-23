# Logging Decorator
To create a decorator we shall utilize a builtin module called `functools`.

```python
from functools import wraps  # this is funny enough, a decorator we'll use to make a decorator
```

We need to come up with a name... for this example I'll call it `debug` because why not? We'll start off by creating a method called `debug` which will have
a parameter called `func`. This is because as a decorator, we act as a middle-man in the call stack. 

When you have a decorator attached to a method your method doesn't actually get ran like you'd think! It is up to the middle-man to do whatever needs to be done!

So lets create this decorator line by line and see how it works

```python
def debug(func): # this is the function we're attached to / trying to call (func)
    @wraps(func) # this allows us to get some information about the called function, capturing the arguments that were passed
    def wrapper_func(*args, **kwargs):
        # *args -- means positional arguments. This is an array of arguments that were passed in where the developer didn't specify a parameter name
        # **kwargs -- means key word arguments. This is where the developer specified which argument goes to which parameter ( a=2, b=3 )
        return "something happened here"
    return wrapper_func # notice how we do not have parenthesis. This is returning a REFERENCE to our WRAPPER FUNC.

@debug # this is the name of our method above
def add(a: int, b: int) -> int:
    return a + b

print(add(2,3)) # at this point we get a reference to that wrapper func from the decorator, we're passing in 2 and 3 as positional arguments
```

You will notice we only see `something happened here` in our terminal!!!! Why? Because we were not very good at executing `func` on behalf of the developer! We totally ignored
what they wanted! So how do we do that?

```python
def debug(func):
    @wraps(func)
    def wrapper_func(*args, **kwargs):
        func(*args, **kwargs) # this will execute the method our developer intended to run. However, when you run this note how `None` gets returned.
    return wrapper_func 
```
Again, we were not very good at being the middleman here. At a minimum we should `at least` return the output of whatever `func` provides us! Worth noting that `every` function/method
out there has a return type of `None` when the keyword `return` isn't used. In other languages such as `C#`, `Java` or `C++` this is called a return type of `void`. AKA... nothing.

```python
def debug(func):
    @wraps(func)
    def wrapper_func(*args, **kwargs):
        return func(*args, **kwargs) 
    return wrapper_func 
```

BAM... now things are working like we intended. So we can build off from here!

Our goal is to print out all the arguments in a nicely formatted fashion right? So we'll need a variable to help us store that info.

```python
def debug(func):
    @wraps(func)
    def wrapper_func(*args, **kwargs):
        output = ""
        
        for x in range(len(args)):
            output += f"\tPositional Arg {x}: {args[x]}\n"
            
        for key, value in kwargs.items():
            output += f"\t{key}: {value}\n"
            
        print(f"Executing `{func.__name__}` with:\n{output}")
        result = func(*args, **kwargs)
        print(f"Return: {result}")
        print("-"*25)
        return result
    return wrapper_func 
```

Notice, we are able to use the dunder (double underscore) name on our function reference! This is how you can output the name of the function that was called! So 
in this example it'll print `add` because we're calling the `add` function.

Example output

```python
add(1, 2)
```
```txt
Executing 'add' with:
	Positional Arg 0: 1
	Positional Arg 1: 2

Return: 3
-------------------------
```

[Previous Section](./intro.md) | [Next Section](./log-execution-time.md)