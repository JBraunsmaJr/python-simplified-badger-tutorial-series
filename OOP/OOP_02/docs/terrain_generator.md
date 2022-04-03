# Terrain Generator
This is where the fun part begins!

Create a file called `terrain.py`. This will be the home to our terrain based stuff.

## Imports
```python
import pygame.display
from config import *
import noise
from np.magic import np
```

## Clamp
We will want a helper function for `clamping` values between a min and max value. This is
useful for when we allow user-defined inputs and don't want them to exceed certain limits.

```python
def clamp(value: float, minimum: float, maximum: float) -> float:
    if value < minimum:
        return minimum
    if value > maximum:
        return maximum
    return value
```

## Terrain Generator
Now onto the complicated part of our app. Rather than specifying a lot of 
arguments in the constructor we'll use `**kwargs` and snag values from there.

Many of these arguments will make no sense right now. Once the UI is hooked up, and 
you can play around with these values you'll see how they influence terrain generation

```python
class TerrainGenerator:
    def __init__(self, **kwargs):
        self.seed = kwargs.pop("seed", 1234)
        self.octaves = kwargs.pop("octaves", 5)
        self.persistence = kwargs.pop("persistence", 0.5)
        self.lacunarity = kwargs.pop("lacunarity", 2)
        self.scale = kwargs.pop("scale", 25)
        self._world_dimensions = kwargs.pop("world_dimensions", (100,100))
        self.world = None
```

Right now we haven't defined the set methods that will also be hooked up to our UI. However,
the `kwargs.pop` method basically says "Does this key exist in here?" If it does it will take the value and
remove it from the `kwargs` dictionary. Otherwise, if it does not exist the default value will be given (the second argument)

```python
test_dict = {
    "one": 123,
    "two": 321
}

default_value = test_dict.pop("three", 3) # default is given
# length of test_dict is still 2
two_value = test_dict.pop("two", 2)
# length is now 1, two_value equals 321 (because it existed in dict)
```

## getter methods
We primarily care about the setter methods but to get there we need the getter
setup!

```python
@property
def persistence(self):
    return self._persistence

@property
def lacunarity(self):
    return self._lacunarity

@property
def scale(self):
    return self._scale

@property
def octaves(self):
    return self._octaves

@property
def world_dimensions(self):
    return self._world_dimensions
```

## Setter methods

We will create a combination of @name.setter methods along with
actual methods. These `actual` methods will be used by our user interface because 
referencing a @name.setter method doesn't work the way you'd think... 

```python
def set_persistence(self, value):
    self.persistence = value

def set_octaves(self, value):
    self.octaves = value

def set_scale(self, value):
    self.scale = value

def set_lacunarity(self, value):
    self.lacunarity = value

def set_map_width(self, value):
    self._world_dimensions = (max(1, value), self._world_dimensions[1])

def set_map_height(self, value):
    self._world_dimensions = (self._world_dimensions[0], max(1, value))

@persistence.setter
def persistence(self, value):
    self._persistence = clamp(value, 0 ,1)

@lacunarity.setter
def lacunarity(self, value):
    self._lacunarity = max(1, value)

@scale.setter
def scale(self, value):
    self._scale = max(value, 0.01)

@octaves.setter
def octaves(self, value):
        self._octaves = max(value, 1)
```

## Normalization
Our perlin noise will be all over the place. We need to standardize a range between 0 and 1
so we can reliably use our layer system!

In Python, it is a pain to use 2d arrays so for now we'll use this method
to take in a row at a time and normalize it

```python
def __normalize(self, arr: list, minimum=0, maximum=1):
    norm_arr = []
    # calculate our target range
    diff = maximum - minimum
    # get the range of our array
    diff_arr = max(arr) - min(arr)
    for i in arr:
        # can look up normalization calcuations online...
        temp = (((i-min(arr)) * diff) / diff_arr) + minimum
        norm_arr.append(temp)
    return norm_arr
```

## Generate world
Now the fun part is to generate our world

```python
def generate_world(self):
    # zero out our world
    self.world = np.zeroes(self._world_dimensions)
    # deconstruct our dimensions
    map_width, map_height = self._world_dimensions
    
    for x in range(map_width):
        for y in range(map_height):
            self.world[x][y] = noise.pnoise2(x/self.scale,
                                             y/self.scale,
                                             octaves=int(self.scale),
                                             persistence=self.persistence,
                                             lacunarity=self.lacunarity,
                                             base=self.seed)
    temp = []
    for row in self.world:
        norm = self.__normalize(row)
        temp.append(row)
    self.world = temp
    return self.world
```

---
[Previous Section](config.md)  |  [Next Section](Layer.md)