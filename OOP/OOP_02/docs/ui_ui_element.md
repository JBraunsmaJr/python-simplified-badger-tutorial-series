# User Interface

###Create a `ui.py` file. This is going to be the home for **all** of our ui elements for this tutorial


We'll only scratch the surface on how user-interfaces are built.

What is the most basic functionality of a UI element?

```yaml
- Position to draw
- Size of element
- Color of element
- Hover color
- Mouse detection (if mouse is on the element)
- Click detection (for release AND pressed)
- Callback support for what should happen on a click event
```

This sounds like a lot but, we'll go over each thing as we build it.

First, lets create the constructor and class....

```python
import pygame

class UIElement:
    def __init__(self, x: int,
                 y: int,
                 width: int,
                 height: int,
                 fore_color: tuple = (0,0,0),
                 background_color: tuple = (255,255,255),
                 hover_color: tuple = (10,10,10),
                 callback=None,
                 **kwargs):
        
        # Pygame has a rect which makes it easier for us
        # to do collisions later, but helps us define position
        # and size as well
        self._rect = pygame.Rect(x, y, width, height)
        
        # AKA text color
        self.fore_color = fore_color
        
        # color drawn in the background
        self.background_color = background_color
        
        # color to drawn when hovering
        self.hover_color = hover_color
        
        # thing to call when this element has been clicked
        self.callback = callback
        
        # helps us cache/track if the element is being hovered on by mouse
        self._hovering = False
```

If you were wondering what `**kwargs` does, or means it stands for `keyword arguments`.
AKA when you specify an argument by name like `functionname(a=123)`. The kwargs
is a dictionary where the key value is the argument name, and the value is the one you passed in.

The `**` means to splat the sucker in there as comma separated values.

```python
dictionary = {
    "test": 123,
    "other": "yes"
}

def testmethod(test, other):
    print(test, other)

testmethod(**dictionary)
# translates to
testmethod(test=123, other="yes")

# outputs
# 123 yes
```

Now we should create some getter/setters to help us. Setters are the more important aspect
of this tutorial as it helps us validate incoming values! Otherwise, we could run into
some exceptions if we accepted just ANY value.

```python
# this makes it so we can go self.callback and retrieve the backing field
# a backing field is the value we don't expose directly to devs
@property
def callback(self):
    return self._callback

@callback.setter
def callback(self, value):
    self._callback = value

@property
def x(self):
    return self._rect.x

@property
def y(self):
    return self._rect.y

@property
def width(self):
    return self._rect.w

@property
def height(self):
    return self._rect.h
```

Those are all the basic getter/setters we'll need for a basic UI element. 

Now we need to implement the basic functions that can be called for rendering, and handling
click events.

Additionally, we might want to support repositioning of our elements down the road! 

```python
def update_position(self, x, y):
    """
    Update position based on new x and y coordinates
    """
    self._rect = pygame.Rect(x, y, self.width, self.height)
```

## Mouse In Bounds
We need the ability to determine if a user is currently hovering over our element. This will
help us dictate whether this is the intended element to interact with

Luckily, as previously mentioned, pygame has some built-in functions to assist
us with collision. The `x` and `y` arguments are the mouse coordinates.

```python
def mouse_in_bounds(self, x, y) -> bool:
    # update our local state so we can use this value later
    # during the draw method
    self._hovering = self._rect.collidepoint(x, y)
    return self._hovering
```


## Draw

```python
def draw(self, screen):
    # we want to draw the appropriate color based on state
    draw_color = self.hover_color if self._hovering else self.background_color
    pygame.draw.rect(screen, draw_color, self._rect)
```

## Click Events
We need some basic methods to call based on certain events. For instance, for click pressed
and click released.

The difference is - while a key is pressed the pressed method gets called. This is horrible
if we only want something to happen ONE time.

For the scenario we want something to occur ONE time we will use the released method.

```python
def on_mouse_release(self, screen, mouse_x, mouse_y):
    # default implementation will call our `callback` method
    # if provided
    if self.callback is not None and callable(self.callback):
        self.callback()

# no default implementation provided for this...
# children will have to override this
def on_mouse_pressed(self, screen, mouse_x, mouse_y):
    pass
```

----
[Previous Section](pre_req.md)  |  [Next Section](ui_group.md)