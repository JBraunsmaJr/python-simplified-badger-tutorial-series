# Layer
This will be added to the bottom of our `terrain.py` file.

Our layer system will be simple. We'll define a name, height limit, and color!

```python
class Layer:
    def __init__(self, name: str, color: tuple, height: float):
        self.name = name
        self.color = color
        self.height = height

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        # we want to clamp our height range between
        # the range we normalized in our terrain generator
        self._height = clamp(value, 0, 1)
```

Anddddd that's it. A simple data structure for holding this information

---
[Previous Section](terrain_generator.md)  |  [Next Section](terrain.md)