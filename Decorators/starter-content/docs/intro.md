# Decorators
Every language calls this something different. In C#, they're known as `Attributes`, or in Java they're called `Annotations`.

In Python a decorator is used to extend something without actually modifying the function itself. Furthermore, you can think of a decorator as a sort of middle-man.

To start off, here is some boilerplate code

```python
def add(a: int, b: int) -> int:
    return a + b

print(add(2,3))
```

What if.. for whatever reason we wanted to print/log the parameters were passed into this function? Your first instinct was probably to add a print statement, wasn't it?

```python
def add(a: int, b: int) -> int:
    print("add", a, b)
    return a + b
```

Cool, but do you REALLY want to copy this code all over the place? No! What if I told you we could add a decorator (that we create) which does exactly what we want without actually modifying
this code?

[Next](./logging-decorator.md)