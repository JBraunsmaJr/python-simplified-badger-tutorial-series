# Terrain

Time to create something that will be represented in the game.

We shall consume `kwargs` since things are going to get wild

```python
class Terrain:
    def __init__(self, **kwargs):
        self.generator = kwargs.pop("generator", 
                                    TerrainGenerator(world_dimensions=kwargs.pop("world_dimensions", (100,100))))
        self.tilesize = kwargs.pop("tilesize", 16)
        self.layers = kwargs.pop("layers", [
            Layer("Deep Water", COLOR_DEEP_WATER, DEFAULT_HEIGHT_DEEP_WATER),
            Layer("Water", COLOR_WATER, DEFAULT_HEIGHT_WATER),
            Layer("Shallow Water", COLOR_SHALLOW_WATER, DEFAULT_HEIGHT_SHALLOW_WATER),
            Layer("Beach", COLOR_BEACH, DEFAULT_HEIGHT_BEACH),
            Layer("Grass", COLOR_GRASS, DEFAULT_HEIGHT_GRASS),
            Layer("Sparse Grass", COLOR_SPARSE_GRASS, DEFAULT_HEIGHT_SPARSE_GRASS),
            Layer("Mountain", COLOR_MOUNTAIN, DEFAULT_HEIGHT_MOUNTAIN),
            Layer("High Mountain", COLOR_HIGH_MOUNTAIN, DEFAULT_HEIGHT_HIGH_MOUNTAIN),
            Layer("Mountain Top", COLOR_MOUNTAIN_SNOW, DEFAULT_HEIGHT_MOUNTAIN_TOP)
        ])
        self.regenerate()
        
    def regenerate(self):
        self.generator.generate_world()    
```

## Layer Color
As we iterate over each tile we need to figure out the appropriate color for a given elevation.

This approach does assume that the layer array is in order from
low to high
```python
def __get_color(self, elevation: float) -> tuple:
    for layer in self.layers:
        if elevation <= layer.height:
            return layer.color
    # if we cannot find an appropriate layer
    # we need to give something as a default
    return COLOR_DEEP_WATER # this can be whatever
```

## Render
```python
def render(self):
    width, height = self.generator.world_dimensions
    display = pygame.display.get_surface()
    for x in range(width):
        for y in range(height):
            elevation = self.generator.world[x][y]
            color = self.__get_color(elevation)
            pygame.draw.rect(display, color, (
                x * self.tilesize,
                y * self.tilesize,
                self.tilesize,
                self.tilesize
            ))
```
----
[Previous Section](Layer.md)  |  [Next Section](game.md)