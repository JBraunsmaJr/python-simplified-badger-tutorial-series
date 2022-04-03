# Slider

This will be the most complicated portion of our user interface

Our slider needs:
```yml
label: (TextElement)
default_value: a value our slider starts off with by default
normalize_range: tuple indicating min and max value for slider
value_type: should our value be a float or int
```

```python
class Slider(UIElement):
    def __init__(self,
                 x: int,
                 y: int,
                 width: int,
                 height: int,
                 label: TextElement,
                 default_value=None,
                 normalize_range: tuple = (0,100),
                 value_type: type = float,
                 **kwargs):
        super().__init__(x, y, width, height, **kwargs)
        self._label = label
        self._normalize_range = normalize_range
        self._value_type = value_type
        self._circle_x = x  # this represents where our circle is on the slider
        
        self.__update_label_pos()
        if default_value is None:
            self._value = normalize_range[0]
        else:
            self._value = default_value

    # same functionality as our button
    def __update_label_pos(self):
        self._label.update_position(self.x + self.width + 10, self.y)

    def update_position(self, x, y):
        super().update_position(x,y)
        self.__update_label_pos()
        self._circle_x = x
```

## Draw
To showcase overriding our parent function completely

```python
def draw(self, screen):
    # draw our rectangle
    pygame.draw.rect(screen, (255,255,255), self._rect)
    #draw our circle that the user interacts with
    pygame.draw.circle(screen, (255, 240, 255),
                       (self._circle_x, (self.height / 2 + self.y)),
                       self.height * 1.5)
    # draw our label at the end
    self._label.draw(screen)
```

## Value
Of course we will want a way to retrieve the value the slider is currently at!

```python
@property
def value(self):
    return self._value
```

We also want a few things to happen whenever our value changes. This is 
where having a setter method comes in handy

```python
@value.setter
def value(self, val):
    # we convert our incoming value into whatever
    # we specified at the beginning. int/float
    self._value = self._value_type(val)
    
    # we are updating our suffix to be whatever this value ios
    self._label.suffix = self._value
    
    # we want to send our updated value
    # to whoever wants to know...
    if self.callback:
        self.callback(self.value)
```

We want the UI to update our value as we slide the circle around. To do this
we will want another method. This will also help us normalize the value to be
within the range we specified at the beginning!

```python
def update_value(self, x):
    # x represents the X value of our circle
    if x < self._rect.x:
        # set the value to our minimum
        self.value = self._normalize_range[0]
    elif x > self._rect.x + self._rect.w:
        self.value = self._normalize_range[1]
    else:
        # We get a percentage of where our value is at based on its width
        # and then multiply by our maximum limit
        # to get a value in our range
        val = (x - self._rect.x) / float(self._rect.w) * self._normalize_range[1]
        self.value = val
```

## Mouse Position
Our interaction point is now a circle which is different than our parent class's 
implementation.

```python
def mouse_in_bounds(self, x, y) -> bool:
    # if you're not good at math this will be confusing
    # but we're essentially checking to see if our mouse coordinates
    # are within our circle
    return ((x - self._circle_x) * (x - self._circle_x) + (y - (self._rect.y + self._rect.h / 2)) * 
            (y - (self._rect.y + self._rect.h / 2))) \
                <= (self._rect.h * 1.5) * (self._rect.h * 1.5)
```

## Events
We want to override the release method because we don't want to call our `callback` when
the user releases the mouse on our slider

```python
def mouse_on_release(self, screen, x, y):
    pass
```

We also need to adjust our pressed event because we need to update the position
of our circle! As well as update our value with the corresponding circle position

```python
def mouse_on_pressed(self, screen, x, y):
    # we must limit the slider in how far left/down it can go!
    # otherwise weird things might happennnnnn
    if x < self._rect.x:
        self._circle_x = self._rect.x
    elif x > self._rect.x + self._rect.w:
        self._circle_x = self._rect.x + self._rect.w
    else:
        self._circle_x = x
    
    self.update_value(x)
    self.draw(screen)
```

----
[Previous Section](ui_button.md)  |  [Next Section](config.md)