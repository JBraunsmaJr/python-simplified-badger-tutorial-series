# Text Element
No user interface is complete without some form of text!!!!!

So for a text element we need to define a few things.

```yml
font_size: A number indicating the size of our text
font: The font to use when displaying our text. 
label: The text to show to our users
suffix: Any value that shall appear after our label... optional
```

If a font is not provided we'll use whatever pygame's default font is

```python
class TextElement(UIElement):
    def __init__(self,
                 text: str,
                 suffix: str = None,
                 font=None,
                 font_size: int = 25,
                 **kwargs
                 ):
        # our position will be updated automatically
        # when we put these inside other elements
        # so unless you want to do something different here
        # by my guest. Otherwise, these default values
        # don't matter
        super().__init__(x=0, y=0, width=0, height=0, **kwargs)
        self.font_size = font_size
        self.font = font if font is not None else pygame.font.get_default_font()
        self.label =text
        self.suffix = suffix
        self.__renderer = pygame.font.Font(self.font, self.font_size)

    # In the event we want our label
    # to update with some sort of suffix value
    # we have a helper method here for appending the
    # suffix when applicable
    def __build_text(self) -> str:
        if self.suffix is not None:
            return f"{self.label}: {self.suffix}"
        return self.label

    def draw(self, screen):
        item = self.__renderer.render(self.__build_text(),
                                      True,
                                      self.fore_color)
        # draws our text item to screen
        # based on our rect value in the parent class 
        # which, as noted earlier, is updated automatically
        # when used inside another UI element
        screen.blit(item, self._rect)
```

----
[Previous Section](ui_group.md)  |  [Next Section](ui_button.md)