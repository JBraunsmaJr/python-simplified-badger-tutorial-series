# Game.py

Finally, we're at the point of piecing all the things together!

## Imports
```python
import pygame
from terrain import Terrain
from ui import Slider, UIGroup, Button, TextElement
from config import TILESIZE, SCREEN_WIDTH, SCREEN_HEIGHT
```

## Terrain
Instantiate our terrain object

```python
terrain = Terrain(tilesize=TILESIZE)
```

## Pygame
Initialize our py game
```python
pygame.init()
display = pygame.display.setmode((SCREEN_WIDTH, SCREEN_HEIGHT))
clcok = pygame.time.Clock()

current_click = []
mouse_released = False
```

## UI Controls
We want to create the UI elements that will help us modify our generator settings!

Notice how our callback arguments do NOT have the parenthesis next to them
This allows us to pass a reference to that method and invoke it later using

```callback()```

This is common practice with UI design. It would be a nightmare if we created a special 
type of slider or button for every little setting! Down below we reuse our [Slider](slider.md) and [TextElement](text_element.md) classes for
different things

Also the position of our controls doesn't really matter, as you know when we add
a control in [UI Group](ui_group.md) the position updates anyhow...
```python
ui_map_control_group = UIGroup(100,100)
ui_map_control_group.add_control(Slider(100, 100, 100, 10,
                                        normalize_range=(0.01, 1),
                                        value_type=float,
                                        label=TextElement("Persistence"),
                                        font_color=(0,0,0),
                                        callback=terrain.generator.set_persistence))

ui_map_control_group.add_control(Slider(0,0,100,10,
                                        normalize_range=(1,10),
                                        value_type=int,
                                        label=TextElement(text="Octaves"),
                                        font_color=(0,0,0),
                                        callback=terrain.generator.set_octaves))

ui_map_control_group.add_control(Slider(0,0,100,10,
                                        label=TextElement(text="Lacunarity"),
                                        value_type=int,
                                        font_color=(0,0,0),
                                        normalize_range=(1,50),
                                        callback=terrain.generator.set_lacunarity))

ui_map_control_group.add_control(Slider(0,0,100,10,
                                        label=TextElement(text="Scale"),
                                        value_type=float,
                                        font_color=(0,0,0),
                                        normalize_range=(0.1, 120),
                                        callback=terrain.generator.set_scale))

ui_map_control_group.add_control(Slider(0,0,100,10,
                                        label=TextElement(text="Map Width"),
                                        value_type=int,
                                        font_color=(0,0,0),
                                        normalize_range=(1,120),
                                        callback=terrain.generator.map_width))

ui_map_control_group.add_control(Slider(0,0,100,10,
                                        label=TextElement(text="Map Height"),
                                        value_type=int,
                                        font_color=(0,0,0),
                                        normalize_range=(1,120),
                                        callback=terrain.generator.map_height))

ui_map_control_group.add_control(Button(0,0,100,26,
                                        label=TextElement(text="Generate",
                                                          font_color=(255, 255, 255)),
                                        background_color=(0, 0, 0),
                                        hover_color=(25,25,25),
                                        callback=terrain.regenerate))
```

# Loop

```python
while True:
    # reset buffer (otherwise what was drawn last frame will stay there)
    display.fill((0, 0, 0))
    
    clock.tick(60)  # limit to 60 frames per second
    mouse_released = False  # update our bool which indicates if we released mouse

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_released = True
    
    terrain.render()
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    ui_map_control_group.draw(display)
    ui_map_control_group.handle_mouse(display, mouse, click, mouse_released)
    
    # update our display
    pygame.display.update()
```