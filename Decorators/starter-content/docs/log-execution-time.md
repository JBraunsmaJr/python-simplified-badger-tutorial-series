# Timer Decorator
Want to time how long a method took to execute? LETS GO

The previous section goes into how to make a decorator and use it so we'll skip into the good stuff here! All we need to do is capture the time before and after executing and
calculate the difference

```python
from functools import wraps
from time import time

def log_time(func):
    @wraps(func)
    def wrapper_func(*args, **kwargs):
        start = time()
        result = func(*args, **kwargs)
        print(f"`{func.__name__}` took %s seconds" %((time()-start)*1000))
        return result
    return wrapper_func

@log_time
def add(a: int, b: int) -> int:
    return a + b

add(123,123)
```

```
'add' took 0.0016689300537109375 seconds
```

Worth noting that when things are super fast I have noticed that it'll print 0 seconds instead.... if you have a better solution go ahead and try it out!


[Previous Section](./logging-decorator.md) | [Next Section](./Annotation-Validator.md)