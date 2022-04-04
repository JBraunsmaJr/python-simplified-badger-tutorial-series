# Config.py
Anytime we have a value that might change, or that we may want to configure/change later...
a `config.py` file isn't a bad idea!

In this case we'll store all of our colors and default heights that will be used
for colorizing our terrain!

Pygame uses a tuple for colors. If you want to create custom colors, or more layers feel
free to do so. I just googled a color picker and found a few colors I liked...

Rembmer... config-based values should be all uppercased to help us differentiate between
normal variables

```python
# TILESIZE
TILESIZE = 16

# COLORATION FOR MAP
COLOR_DEEP_WATER = (38, 32, 153)
COLOR_WATER = (68, 62, 201)
COLOR_SHALLOW_WATER = (75, 151, 201)
COLOR_BEACH = (229, 216, 117)
COLOR_GRASS = (32, 153, 98)
COLOR_SPARSE_GRASS = (84, 183, 97)
COLOR_MOUNTAIN = (132, 145, 134)
COLOR_HIGH_MOUNTAIN = (101, 104, 101)
COLOR_MOUNTAIN_SNOW = (245, 240, 240)

# HEIGHTS FOR LAYER
DEFAULT_HEIGHT_DEEP_WATER = 0.1
DEFAULT_HEIGHT_WATER = 0.2
DEFAULT_HEIGHT_SHALLOW_WATER = 0.3
DEFAULT_HEIGHT_BEACH = 0.4
DEFAULT_HEIGHT_GRASS = 0.45
DEFAULT_HEIGHT_SPARSE_GRASS = 0.6
DEFAULT_HEIGHT_MOUNTAIN = 0.8
DEFAULT_HEIGHT_HIGH_MOUNTAIN = 0.9
DEFAULT_HEIGHT_MOUNTAIN_TOP = 1.0
```

---
[Previous Section](slider.md)  |  [Next Section](terrain_generator.md)