# Annotation Validation
I know a lot of pythoneers will scream at this... because the idea is `it's better to ask for forgiveness` and I'm not about that life. I prefer validating arguments before executing code!
If I expected numbers... I want numbers darnit! Or... what happens if a payment system accepted incorrect inputs?!?!?!??!?! Cost a customer money!!! Nope... I refuse to accept this
idea of asking for forgiveness when we can avoid these mishaps by checking arguments!

Python has a lovely system called `annotations` which in my opinion is literally a `type hint` from TypeScript. All this does is tell you, the developer, what the expected input types and
return types should be. Keyword... `should` be. At runtime these annotations are tossed aside, ignored, overlooked. Well... how about we use a decorator to fix that problem!

To create such a decorator we will need the `inspect` module (that's builtin). No need to install anything!

```python
from functools import wraps
import inspect

def validate_annotations(func):
    @wraps(func)
    def wrapper_func(*args, **kwargs):
        
        # this will get all the information we will need from our function
        # from the names of positional arguments, to annotations on each argument (if applicable)
        info = inspect.getfullargspec(func) 

        errors = [] # cache a summary of errors that will be output at the end (if applicable)

        for x in range(len(args)):
            # this is a parallel array topic. Our positional argument array should never be more than what our function has
            # otherwise... that's a different error in python
            key = info.args[x] # we need to figure out what the parameter name is for the current index/argument passed in
            
            # does an annotation exist for this parameter? Does the type given not match what we're execpting?
            if key in info.annotations and type(args[x]) != info.annotations[key]:
                errors.append(f"Positional arg <{x}> expected a value type of `{info.annotations[key].__name__}` but got `{type(args[x]).__name__}` instead")
            
        for key, value in kwargs.items():
            # we already know the name because it's a key word argument
            if key in info.annotations and type(value) != info.annotations[key]:
                errors.append(f"KW arg <{key}> expected a value type of `{info.annotations[key].__name__}` but got `{type(value).__name__}` instead")

        # if we have ANY errors at this point we will throw an exception and print out the issues 
        if errors: # aka not none, and has a length greater than 0
            raise ValueError(f"`{func.__name__}` has validation errors:\n{errors}")
        
        result = func(*args, **kwargs)
        
        # return will be the name of an annotation specifying the return type
        if "return" in info.annotations and type(result) != info.annotations["return"]:
            raise ValueError(f"`{func.__name__}` expected a return type of `{info.annotations['return'].__name__}` but got `{type(result).__name__}` instead")

        return result
    return wrapper_func
    
@validate_annotations
def add(a: int, b: int) -> int:
    return a + b

add("123", 2) # throws error, does not get ran
add(2,3) # returns 5
```

Now whenever this is attached to a method, if incorrect argument types are passed in the method will NOT RUN. Instead, an exception is thrown! Furthermore, if an invalid return type 
is given it'll throw an exception and stop any further execution. 

[Previous Section](./log-execution-time.md)
