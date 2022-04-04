# Button
I don't think I've ever seen a UI that doesn't have a button! So lets dive in

```python
class Button(UIElement):
    def __init__(self,
                 x: int,
                 y: int,
                 width: int,
                 height: int,
                 label: TextElement,
                 **kwargs):
        super().__init__(x, y, width, height, **kwargs)
        self._label = label
        self.__update_label_pos()
```

As noted in [Text Element](text_element.md) we need the ability to update our label
positions.

```python
def __update_label_pos(self):
    """
    Ensure that our label is in the correct spot
    """
    # the 10 is an arbitrary padding number
    # that you can adjust if needed
    # or event turn into a parameter of sorts....
    self._label.update_position(self.x + self.width + 10, self.y)
```

We need to update 2 methods to ensure things are drawn and updated correctly

```python
def draw(self, screen):
    # in this case we want to ADD onto our parents functionality
    # - not change it entirely
    super().draw(screen)
    self._label.draw(screen)

def update_position(self, x, y):
    # again, we want to ADD functionality here.
    super().update_position(x, y)
    self.__update_label_pos()
```