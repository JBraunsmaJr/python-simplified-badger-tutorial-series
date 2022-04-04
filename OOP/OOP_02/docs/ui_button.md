# Button
Thanks to inheritance this class will be relatively small!

We need the ability to specify the label ([Text Element](text_element.md)). Along with
the position and dimensions for our button.

Any extra arguments can be passed up the chain using `kwargs`

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

    def __update_label_pos(self):
        """
        Ensure that our label is in the correct spot at creation
        """
        self._label.update_position(self.x, self.y)

    def draw(self, screen):
        super().draw(screen)
        self._label.draw(screen)

    def update_position(self, x, y):
        super().update_position(x, y)
        # we need to update our label position as well to keep them inline
        self.__update_label_pos()
```

That's it!

----
[Previous Section](text_element.md)  |  [Next Section](slider.md)