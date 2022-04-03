# UI Group
We're going to, technically, create a layout class to assist us with rendering
a list of `UIElement` as well as handle events.

Out of all the things we'll be making this will be by far the simplest!

This is a container, slightly different from our `UIElement`
```python
class UIGroup:
    def __init__(self, x: int, y: int,
                 padding: int = 16):
        self._x = x
        self._y = y
        self._padding = padding
        self.controls: list = []
```

We need the ability to add a control

```python
def add_control(self, control: UIElement):
    cx = self._x
    total_height = 0
    
    # we want to add the new element to the BOTTOM
    # of our layout group here
    # so to do this we need to calculate the height of each element
    # and add padding
    for c in self.controls:
        total_height += c.height
    cy = self._y + total_height + (len(self.controls) * self._padding)
    
    # we want to update the UI element's position to
    # whatever it should be in our layout group
    control.update_position(cx, cy)
    
    # add control to our list for later use
    self.controls.append(control)
```

We need methods to help us handle mouse events and drawing

## Mouse Events
```python
def handle_mouse(self, display, mouse, current_click, mouse_released):
    """
    :param display: surface we're using
    :param mouse: Tuple for mouse coordinates
    :param current_click: Tuple representing LMB, MMB, RMB
    :param mouse_released: Bool value indicating if mouse button was released
    """
    for control in self.controls:
        if control.mouse_in_bounds(*mouse):
            if mouse_released:
                control.mouse_on_release(display, *mouse)
            elif current_click[0]: # Left Mouse Button Clicked
                control.mouse_on_pressed(display, *mouse)
```

## Draw
```python
def draw(self, screen):
    for control in self.controls:
        control.draw(screen)
```

----
[Previous Section](ui_ui_element.md)  |  [Next Section](text_element.md)