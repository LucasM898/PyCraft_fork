from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import lit_with_shadows_shader
from ursina import Slider
from perlin_noise import PerlinNoise
from ursina.collider import BoxCollider
from ursina.texture_importer import load_texture
from ursina import InputField
from ursina import invoke
import random
import json
import os
import math
import importlib
import importlib.util
import sys
from pathlib import Path
from datetime import datetime
import time
script_dir = Path(__file__).parent.parent
print(f'The relative path is {script_dir}')
current_datetime = datetime.now()
app = Ursina(borderless=False, title='PyCraft', icon='PyCraft/pycraftlogo.ico')
Entity.default_shader = lit_with_shadows_shader
sun = DirectionalLight(parent=scene, y=10, z=10, shadows=True)
sun.look_at(Vec3(0,0,0))

game_version = '3.3'
world_data = []
hearts = []
hungers = []
debugOpen = False
cinematicMode = False
window.fullscreen = False
seedvalue = None
fov_slider = None
saved_world_name = None
holding_block = False
replacingslot = False
pause_menu_open = False
play_menu_open = False
block_class_mapping = {}
paused = False
spawnpoint = Vec3(*[0,0,0])
isanimating = False

Text.default_font = "PyCraft/Textures/Fonts/mc.ttf"
vignette = Entity(
        parent=camera.ui,
        model='quad',
        scale=(2, 1, 1),
        color=color.rgba(250,0,0,0),
        texture = "PyCraft/Textures/damage",
        position=(0,0,-3),  
        visible=True,
        blend_mode='transparent',
        )

class Cloud(Entity):
    def __init__(self, position=(0,0,0), size=(30,3,5), **kwargs):
        super().__init__(**kwargs)
        self.size = size
        self.position = position

        for x in range(size[0]):
            for y in range(size[1]):
                for z in range(size[2]):
                    if random.random() > 0.7:
                        cube = Entity(
                            model='cube',
                            color=color.rgba(1,1,1,0.5),
                            scale=size,
                            position=(x,y,z),
                            parent=self,
                        )



# Voxel Classes
# -------------

class Voxel(Button):
    block_texture='PyCraft/Textures/cobblestone.png'
    block_icon = 'PyCraft/Textures/cobblestoneblock.png'
    block_color = color.hsv(0, 0, .9)
    block_model = 'cube'
    def __init__(self, position=(0,0,0)):
        base_color = color.hsv(0, 0, 0.9)
        super().__init__(parent=scene,
            position=position,
            model='cube',
            origin_y=.5,
            texture='PyCraft/Textures/cobblestone.png',
            color=base_color,
            blockclass='stone',
            isblock = True,
        )
        r = min(base_color.r + 0.1, 1.0)
        g = min(base_color.g + 0.1, 1.0)
        b = min(base_color.b + 0.1, 1.0)
        self.highlight_color = color.rgb(r, g, b)
block_class_mapping['Voxel'] = Voxel
class IronOreVoxel(Button):
    block_texture='PyCraft/Textures/iron_ore.png'
    block_icon = 'PyCraft/Textures/ironoreblock.png'
    block_color = color.hsv(0, 0, .9)
    block_model = 'cube'
    def __init__(self, position=(0,0,0)):
        base_color = color.hsv(0, 0, 0.9)
        super().__init__(parent=scene,
            position=position,
            model='cube',
            origin_y=.5,
            texture='PyCraft/Textures/iron_ore.png',
            color=base_color,
            blockclass='ore',
            isblock = True
        )
        r = min(base_color.r + 0.1, 1.0)
        g = min(base_color.g + 0.1, 1.0)
        b = min(base_color.b + 0.1, 1.0)
        self.highlight_color = color.rgb(r, g, b)
block_class_mapping['IronOreVoxel'] = IronOreVoxel
class CoalOreVoxel(Button):
    block_texture='PyCraft/Textures/coal_ore.png'
    block_icon = 'PyCraft/Textures/coaloreblock.png'
    block_color = color.hsv(0, 0, .9)
    block_model = 'cube'
    def __init__(self, position=(0,0,0)):
        base_color = color.hsv(0, 0, 0.9)
        super().__init__(parent=scene,
            position=position,
            model='cube',
            origin_y=.5,
            texture='PyCraft/Textures/coal_ore.png',
            color=base_color,
            blockclass='ore',
            isblock = True
        )
        r = min(base_color.r + 0.1, 1.0)
        g = min(base_color.g + 0.1, 1.0)
        b = min(base_color.b + 0.1, 1.0)
        self.highlight_color = color.rgb(r, g, b)
block_class_mapping['CoalOreVoxel'] = CoalOreVoxel
class OakPlanksVoxel(Button):
    block_texture='PyCraft/Textures/oak_planks.png'
    block_icon = 'PyCraft/Textures/oakplanksblock.png'
    block_color = color.hsv(0, 0, .9)
    block_model = 'cube'
    def __init__(self, position=(0,0,0)):
        base_color = color.hsv(0, 0, .9)
        super().__init__(parent=scene,
            position=position,
            model='cube',
            origin_y=.5,
            texture='PyCraft/Textures/oak_planks.png',
            color=base_color,
            isblock = True
        )
        r = min(base_color.r + 0.1, 1.0)
        g = min(base_color.g + 0.1, 1.0)
        b = min(base_color.b + 0.1, 1.0)
        self.highlight_color = color.rgb(r, g, b)
block_class_mapping['OakPlanksVoxel'] = OakPlanksVoxel
class OakSlabVoxel(Button):
    block_texture='PyCraft/Textures/oak_planks.png'
    block_icon = 'PyCraft/Textures/oakplanksblock.png'
    block_color = color.hsv(0, 0, .9)
    block_model = 'cube'
    def __init__(self, position=(0,0,0)):
        base_color = color.hsv(0, 0, .9)
        super().__init__(parent=scene,
            position=position,
            model='cube',
            origin_y=.5,
            texture='PyCraft/Textures/oak_planks.png',
            color=base_color,
            scale = (1,0.5,1),
            isblock = True
        )
        r = min(base_color.r + 0.1, 1.0)
        g = min(base_color.g + 0.1, 1.0)
        b = min(base_color.b + 0.1, 1.0)
        self.highlight_color = color.rgb(r, g, b)
block_class_mapping['OakSlabVoxel'] = OakSlabVoxel
class OakLogVoxel(Button):
    block_texture='PyCraft/Textures/oaklogatlas.png'
    block_icon = 'PyCraft/Textures/oaklogblock.png'
    block_color = color.hsv(0, 0, .9)
    block_model = 'PyCraft/Textures/atlasblock.obj'
    hand_scale = (0.25, 0.25, 0.25)
    yorg = 1
    def __init__(self, position=(0,0,0)):
        base_color = color.hsv(0, 0, .9)
        super().__init__(parent=scene,
            position=position,
            model='PyCraft/Textures/atlasblock.obj',
            origin_y=2,
            scale=0.5,
            texture='PyCraft/Textures/oaklogatlas.png',
            color=base_color,
            isblock = True
        )
        r = min(base_color.r + 0.1, 1.0)
        g = min(base_color.g + 0.1, 1.0)
        b = min(base_color.b + 0.1, 1.0)
        self.highlight_color = color.rgb(r, g, b)
block_class_mapping['OakLogVoxel'] = OakLogVoxel
class TreeLeavesVoxel(Button):
    block_texture='PyCraft/Textures/treeleaves2.png'
    block_icon = 'PyCraft/Textures/leavesicon.png'
    block_color = color.hsv(0, 0, .9)
    block_model = 'cube'
    def __init__(self, position=(0,0,0)):
        base_color = color.hsv(0, 0, .9)
        super().__init__(parent=scene,
            position=position,
            model='cube',
            origin_y=.5,
            texture='PyCraft/Textures/treeleaves2.png',
            color=base_color,
            isblock = True
        )
        r = min(base_color.r + 0.1, 1.0)
        g = min(base_color.g + 0.1, 1.0)
        b = min(base_color.b + 0.1, 1.0)
        self.highlight_color = color.rgb(r, g, b)
block_class_mapping['TreeLeavesVoxel'] = TreeLeavesVoxel
class SakuraLeaves(Button):
    block_texture='PyCraft/Textures/treeleaves.png'
    block_icon = 'PyCraft/Textures/sakuraleavesicon.png'
    block_color = color.hsv(0, 0, .9)
    block_model = 'cube'
    def __init__(self, position=(0,0,0)):
        base_color = color.hsv(0, 0, .9)
        super().__init__(parent=scene,
            position=position,
            model='cube',
            origin_y=.5,
            texture='PyCraft/Textures/treeleaves.png',
            color=base_color,
            isblock = True
        )
        r = min(base_color.r + 0.1, 1.0)
        g = min(base_color.g + 0.1, 1.0)
        b = min(base_color.b + 0.1, 1.0)
        self.highlight_color = color.rgb(r, g, b)
block_class_mapping['SakuraLeaves'] = SakuraLeaves
class Fire(Button):
    block_texture='PyCraft/Textures/fireatlas.png'
    block_icon = 'PyCraft/Textures/grassblock.png'
    block_model = 'PyCraft/Textures/atlasblock.obj'
    block_color = color.hsv(0, 0, 0.9)
    hand_scale = (0.25, 0.25, 0.25)
    yorg = 1
    def __init__(self, position=(0,0,0)):
        base_color = color.hsv(0, 0, 0.9)
        super().__init__(parent=scene,
            position=position,
            model='PyCraft/Textures/atlasblock.obj',
            origin_y=2,
            texture='PyCraft/Textures/fireatlas.png',
            scale=0.5,
            color=base_color,
            highlight_color=color.cyan,
            isblock = True
        )
        self.is_trigger = True

        r = min(base_color.r + 0.1, 1.0)
        g = min(base_color.g + 0.1, 1.0)
        b = min(base_color.b + 0.1, 1.0)
        self.highlight_color = color.rgb(r, g, b)
block_class_mapping['Fire'] = Fire
class GlassVoxel(Button):
    block_texture='PyCraft/Textures/glass.png'
    block_icon = 'PyCraft/Textures/glassblock.png'
    block_color = color.hsv(0, 0, .9)
    block_model = 'cube'
    def __init__(self, position=(0,0,0)):
        base_color = color.hsv(0, 0, .9)
        super().__init__(parent=scene,
            position=position,
            model='cube',
            origin_y=.5,
            texture='PyCraft/Textures/glass.png',
            color=base_color,
            isblock = True
        )
        r = min(base_color.r + 0.1, 1.0)
        g = min(base_color.g + 0.1, 1.0)
        b = min(base_color.b + 0.1, 1.0)
        self.highlight_color = color.rgb(r, g, b)
block_class_mapping['GlassVoxel'] = GlassVoxel
class GroundVoxel(Button):
    block_texture='PyCraft/Textures/grassatlas.png'
    block_icon = 'PyCraft/Textures/grassblock.png'
    block_model = 'PyCraft/Textures/atlasblock.obj'
    block_color = color.hsv(0, 0, 0.9)
    hand_scale = (0.25, 0.25, 0.25)
    yorg = 1
    def __init__(self, position=(0,0,0)):
        base_color = color.hsv(0, 0, 0.9)
        super().__init__(parent=scene,
            position=position,
            model='PyCraft/Textures/atlasblock.obj',
            origin_y=2,
            texture='PyCraft/Textures/grassatlas.png',
            scale=0.5,
            color=base_color,
            highlight_color=color.cyan,
            isblock = True
        )

        r = min(base_color.r + 0.1, 1.0)
        g = min(base_color.g + 0.1, 1.0)
        b = min(base_color.b + 0.1, 1.0)
        self.highlight_color = color.rgb(r, g, b)
block_class_mapping['GroundVoxel'] = GroundVoxel
class BrownVoxel(Button):
    block_texture = 'PyCraft/Textures/default_dirt.png'
    block_icon = 'PyCraft/Textures/dirtblock.png'
    block_color = color.hsv(0, 0, 0.9)
    block_model = 'cube'
    def __init__(self, position=(0,0,0)):
        base_color = color.hsv(0, 0, 0.8)
        super().__init__(parent=scene,
            position=position,
            model='cube',
            origin_y=.5,
            texture='PyCraft/Textures/default_dirt.png',
            color=base_color,
            highlight_color=color.cyan,
            collider='box',
            isblock = True
        )
        r = min(base_color.r + 0.1, 1.0)
        g = min(base_color.g + 0.1, 1.0)
        b = min(base_color.b + 0.1, 1.0)
        self.highlight_color = color.rgb(r, g, b)
block_class_mapping['BrownVoxel'] = BrownVoxel
class WhiteWoolVoxel(Button):
    block_texture='PyCraft/Textures/white_wool.png'
    block_icon = 'PyCraft/Textures/whitewoolblock.png'
    block_color = color.hsv(0, 0, .9)
    block_model = 'cube'
    def __init__(self, position=(0,0,0)):
        base_color = color.hsv(0, 0, .9)
        super().__init__(parent=scene,
            position=position,
            model='cube',
            origin_y=.5,
            texture='PyCraft/Textures/white_wool.png',
            color=base_color,
            isblock = True
        )
        r = min(base_color.r + 0.1, 1.0)
        g = min(base_color.g + 0.1, 1.0)
        b = min(base_color.b + 0.1, 1.0)
        self.highlight_color = color.rgb(r, g, b)
block_class_mapping['WhiteWoolVoxel'] = WhiteWoolVoxel
class ObsidianVoxel(Button):
    block_texture='PyCraft/Textures/obsidian.png'
    block_icon = 'PyCraft/Textures/obsidianicon.png'
    block_color = color.hsv(0, 0, .9)
    block_model = 'cube'
    def __init__(self, position=(0,0,0)):
        base_color = color.hsv(0, 0, .9)
        super().__init__(parent=scene,
            position=position,
            model='cube',
            origin_y=.5,
            texture='PyCraft/Textures/obsidian.png',
            color=base_color,
            blockclass='obsidian',
            isblock = True
        )
        r = min(base_color.r + 0.1, 1.0)
        g = min(base_color.g + 0.1, 1.0)
        b = min(base_color.b + 0.1, 1.0)
        self.highlight_color = color.rgb(r, g, b)
block_class_mapping['ObsidianVoxel'] = ObsidianVoxel
class BlackWoolVoxel(Button):
    block_texture='PyCraft/Textures/black_wool.png'
    block_icon = 'PyCraft/Textures/blackwoolblock.png'
    block_color = color.hsv(0, 0, .9)
    block_model = 'cube'
    def __init__(self, position=(0,0,0)):
        base_color = color.hsv(0, 0, .9)
        super().__init__(parent=scene,
            position=position,
            model='cube',
            origin_y=.5,
            texture='PyCraft/Textures/black_wool.png',
            color=base_color,
            isblock = True
        )
        r = min(base_color.r + 0.1, 1.0)
        g = min(base_color.g + 0.1, 1.0)
        b = min(base_color.b + 0.1, 1.0)
        self.highlight_color = color.rgb(r, g, b)
block_class_mapping['BlackWoolVoxel'] = BlackWoolVoxel
class RedWoolVoxel(Button):
    block_texture='PyCraft/Textures/red_wool.png'
    block_icon = 'PyCraft/Textures/redwoolblock.png'
    block_color = color.hsv(0, 0, .9)
    block_model = 'cube'
    def __init__(self, position=(0,0,0)):
        base_color = color.hsv(0, 0, .9)
        super().__init__(parent=scene,
            position=position,
            model='cube',
            origin_y=.5,
            texture='PyCraft/Textures/red_wool.png',
            color=base_color,
            isblock = True
        )
        r = min(base_color.r + 0.1, 1.0)
        g = min(base_color.g + 0.1, 1.0)
        b = min(base_color.b + 0.1, 1.0)
        self.highlight_color = color.rgb(r, g, b)
block_class_mapping['RedWoolVoxel'] = RedWoolVoxel
class DiamondBlock(Button):
    block_texture='PyCraft/Textures/diamondblock.png'
    block_icon = 'PyCraft/Textures/diamondblockicon.png'
    block_color = color.hsv(0, 0, .9)
    block_model = 'cube'
    def __init__(self, position=(0,0,0)):
        base_color = color.hsv(0, 0, .9)
        super().__init__(parent=scene,
            position=position,
            model='cube',
            origin_y=.5,
            texture='PyCraft/Textures/diamondblock.png',
            color=base_color,
            isblock = True
        )
        r = min(base_color.r + 0.1, 1.0)
        g = min(base_color.g + 0.1, 1.0)
        b = min(base_color.b + 0.1, 1.0)
        self.highlight_color = color.rgb(r, g, b)
block_class_mapping['DiamondBlock'] = DiamondBlock
class SlimeVoxel(Button):
    block_texture='PyCraft/Textures/slime.png'
    block_icon = 'PyCraft/Textures/slimeblock.png'
    block_color = color.hsv(0, 0, .9)
    block_model = 'cube'
    def __init__(self, position=(0,0,0)):
        base_color = color.hsv(0, 0, .9)
        super().__init__(parent=scene,
            position=position,
            model='cube',
            origin_y=.5,
            texture='PyCraft/Textures/slime.png',
            color=base_color,
            isblock = True
        )
        r = min(base_color.r + 0.1, 1.0)
        g = min(base_color.g + 0.1, 1.0)
        b = min(base_color.b + 0.1, 1.0)
        self.highlight_color = color.rgb(r, g, b)
block_class_mapping['SlimeVoxel'] = SlimeVoxel
class SandVoxel(Button):
    block_texture='PyCraft/Textures/sand.png'
    block_icon = 'PyCraft/Textures/sandblock.png'
    block_color = color.hsv(0, 0, .8)
    block_model = 'cube'
    def __init__(self, position=(0,0,0)):
        base_color = color.hsv(0, 0, .8)
        super().__init__(parent=scene,
            position=position,
            model='cube',
            origin_y=.5,
            texture='PyCraft/Textures/sand.png',
            color=base_color,
            isblock = True
        )
        r = min(base_color.r + 0.1, 1.0)
        g = min(base_color.g + 0.1, 1.0)
        b = min(base_color.b + 0.1, 1.0)
        self.highlight_color = color.rgb(r, g, b)
        self.falling = False
        self.destroyable = True
        invoke(self.start_physics, delay=0.1)

    def start_physics(self):
        self.falling = True

    def update(self):
        ray = raycast(self.position + Vec3(0, -0.125, 0), Vec3(0, -1, 0), distance=1, ignore=(self,))
        if not ray.hit:
            self.falling = True
        else:
            self.falling = False
        
        if self.falling:
            self.position += Vec3(0, -0.1, 0) * time.dt * 60
            self.destroyable = False
            if raycast(self.position + Vec3(0, -0.125, 0), Vec3(0, -1, 0), distance=1, ignore=(self,)).hit:
                self.falling = False
                self.destroyable = True
                self.position = Vec3(self.position.x, round(self.position.y), self.position.z)
block_class_mapping['SandVoxel'] = SandVoxel
class GravelVoxel(Button):
    block_texture='PyCraft/Textures/gravel.png'
    block_icon = 'PyCraft/Textures/gravelblock.png'
    block_color = color.hsv(0, 0, .8)
    block_model = 'cube'
    def __init__(self, position=(0,0,0)):
        base_color = color.hsv(0, 0, .8)
        super().__init__(parent=scene,
            position=position,
            model='cube',
            origin_y=.5,
            texture='PyCraft/Textures/gravel.png',
            color=base_color,
            isblock = True
        )
        r = min(base_color.r + 0.1, 1.0)
        g = min(base_color.g + 0.1, 1.0)
        b = min(base_color.b + 0.1, 1.0)
        self.highlight_color = color.rgb(r, g, b)
        self.falling = False
        self.destroyable = True
        invoke(self.start_physics, delay=0.1)

    def start_physics(self):
        self.falling = True

    def update(self):
        ray = raycast(self.position + Vec3(0, -0.125, 0), Vec3(0, -1, 0), distance=1, ignore=(self,))
        if not ray.hit:
            self.falling = True
        else:
            self.falling = False
        
        if self.falling:
            self.position += Vec3(0, -0.1, 0) * time.dt * 60
            self.destroyable = False
            if raycast(self.position + Vec3(0, -0.125, 0), Vec3(0, -1, 0), distance=1, ignore=(self,)).hit:
                self.falling = False
                self.destroyable = True
                self.position = Vec3(self.position.x, round(self.position.y), self.position.z)
block_class_mapping['GravelVoxel'] = GravelVoxel
class CraftingTableVoxel(Button):
    block_texture='PyCraft/Textures/craftingtableatlas.png'
    block_icon = 'PyCraft/Textures/craftingtable.png'
    block_model = 'PyCraft/Textures/atlasblock.obj'
    block_color = color.hsv(0, 0, 0.9)
    hand_scale = (0.25, 0.25, 0.25)
    yorg = 1
    def __init__(self, position=(0,0,0)):
        base_color = color.hsv(0, 0, 0.9)
        super().__init__(parent=scene,
            position=position,
            model='PyCraft/Textures/atlasblock.obj',
            origin_y=2,
            texture='PyCraft/Textures/craftingtableatlas.png',
            scale=0.5,
            color=base_color,
            highlight_color=color.cyan,
            isblock = True
        )

        r = min(base_color.r + 0.1, 1.0)
        g = min(base_color.g + 0.1, 1.0)
        b = min(base_color.b + 0.1, 1.0)
        self.highlight_color = color.rgb(r, g, b)
block_class_mapping['CraftingTableVoxel'] = CraftingTableVoxel
class DoorVoxel(Button):
    def __init__(self, position=(0,0,0)):
        base_color = color.hsv(30, 0.5, 0.7)
        super().__init__(parent=scene,
            position=position,
            model='cube',
            scale = (1,2,0.25),
            origin_y=.5,
            texture='PyCraft/Textures/oak_door.png',
            color=base_color,
            highlight_color=color.cyan,
            collider='box'
        )
        r = min(base_color.r + 0.1, 1.0)
        g = min(base_color.g + 0.1, 1.0)
        b = min(base_color.b + 0.1, 1.0)
        self.highlight_color = color.rgb(r, g, b)

class Bedrock(Button):
    block_texture='PyCraft/Textures/bedrocktexture.png'
    block_icon = 'PyCraft/Textures/bedrockblock.png'
    block_color = color.hsv(0, 0, 1)
    block_model = 'cube'
    def __init__(self, position=(0,0,0)):
        base_color = color.hsv(0, 0, 1)
        super().__init__(parent=scene,
            position=position,
            model='cube',
            origin_y=.5,
            texture='PyCraft/Textures/bedrocktexture.png',
            color=base_color,
            highlight_color=color.cyan,
            isblock = True
        )
        r = min(base_color.r + 0.1, 1.0)
        g = min(base_color.g + 0.1, 1.0)
        b = min(base_color.b + 0.1, 1.0)
        self.highlight_color = color.rgb(r, g, b)
        self.destroyable = False
block_class_mapping['Bedrock'] = Bedrock

class DroppedBlock(Entity):
    def __init__(self, position, texture, block_class, **kwargs):
        super().__init__(
            parent=scene,
            position=position - Vec3(0, 0.5, 0),
            model='cube',
            texture=texture,
            scale=0.25,
            rotation=Vec3(0,0,0),
            **kwargs
        )
        self.block_class = block_class
        self.model = block_class_mapping[self.block_class.__name__].block_model
        self.scale = 0.25 if f'{self.model}'[-4:] == 'cube' else 0.125
        self.spin_speed = random.uniform(20,40)
        self.hover_offset = -0.5
        self.hover_speed = random.uniform(1, 2)
        self.original_y = position.y - 0.5
        self.animating = False
        self.pickingup = False
    
    def update(self):
        self.rotation_y += self.spin_speed * time.dt
        if not self.pickingup:
            self.y = self.original_y + math.sin(time.time() * self.hover_speed) * 0.1
        if distance(self.position, player.position) < 2 and not self.animating:
            self.pick_up()
    
    def pick_up(self):
        self.animating = True
        target_position = player.position - Vec3(0, 0.5, 0)
        for i in slots:
            if not i.equipped or i.equipped == block_class_mapping[self.block_class.__name__]:
                self.pickingup = True
                self.position = lerp(self.position, target_position, 0.1)
                break
            self.pickingup = False
        if distance(self.position, player.position) < 1:
            self.searching = True
            for i in slots:
                if i.equipped == block_class_mapping[self.block_class.__name__] and i.amount < 64:
                    i.amount += 1
                    destroy(self)
                    self.searching = False
                    break
            if self.searching:
                for i in slots:
                    if not i.equipped:
                        i.hand_color = block_class_mapping[self.block_class.__name__].block_color
                        i.texture = block_class_mapping[self.block_class.__name__].block_icon
                        i.equipped = block_class_mapping[self.block_class.__name__]
                        i.amount += 1
                        i.visible = True
                        self.searching = False
                        update_equipped_slot(slotselected)
                        destroy(self)
                        break
        self.animating = False

class WoodPickaxe(Entity):
    block_texture=None
    block_icon = 'PyCraft/Textures/woodenpickaxeicon.png'
    block_color = color.hsv(0, 0, .9)
    block_model = 'PyCraft/Textures/Pickaxes/wood.glb'
    defaultrotation = (180,80,145)
    animationrotation = (180, 80, 205)
    yorg = 0.75
    classaffect = ['stone', 'ore']
    istool = True

class StonePickaxe(Entity):
    block_texture=None
    block_icon = 'PyCraft/Textures/stonepickaxeicon.png'
    block_color = color.hsv(0, 0, .9)
    block_model = 'PyCraft/Textures/Pickaxes/stone.glb'
    defaultrotation = (180,80,145)
    animationrotation = (180, 80, 205)
    yorg = 0.75
    classaffect = ['stone', 'ore']
    istool = True

class IronPickaxe(Entity):
    block_texture=None
    block_icon = 'PyCraft/Textures/ironpickaxeicon.png'
    block_color = color.hsv(0, 0, .9)
    block_model = 'PyCraft/Textures/Pickaxes/iron.glb'
    defaultrotation = (180,80,145)
    animationrotation = (180, 80, 205)
    yorg = 0.75
    classaffect = ['stone', 'ore']
    istool = True

class GoldPickaxe(Entity):
    block_texture=None
    block_icon = 'PyCraft/Textures/goldpickaxeicon.png'
    block_color = color.hsv(0, 0, .9)
    block_model = 'PyCraft/Textures/Pickaxes/gold.glb'
    defaultrotation = (180,80,145)
    animationrotation = (180, 80, 205)
    yorg = 0.75
    classaffect = ['stone', 'ore']
    istool = True

class DiamondPickaxe(Entity):
    block_texture=None
    block_icon = 'PyCraft/Textures/diamondpickaxeicon.png'
    block_color = color.hsv(0, 0, .9)
    block_model = 'PyCraft/Textures/Pickaxes/diamond.glb'
    defaultrotation = (180,80,145)
    animationrotation = (180, 80, 205)
    yorg = 0.75
    classaffect = ['stone', 'ore', 'obsidian']
    istool = True

class Cookie(Entity):
    block_texture='PyCraft/Textures/cookieicon.png'
    block_icon = 'PyCraft/Textures/cookieicon.png'
    block_color = color.hsv(0, 0, .9)
    block_model = 'quad'
    defaultrotation = (0,35,10)
    animationrotation = (55, 105, -50)
    yorg = 0.00001
    classaffect = ['stone', 'ore']
    istool = True

class WoodSword(Entity):
    block_texture=None
    block_icon = 'PyCraft/Textures/woodenpickaxeicon.png'
    block_color = color.hsv(0, 0, .9)
    block_model = 'PyCraft/Textures/Swords/wood.glb'
    defaultrotation = (220,180,90)
    animationrotation = (180, 80, 205)
    yorg = 0.05
    hand_scale = 0.025
    classaffect = []
    istool = True

class FlintAndSteel(Entity):
    block_texture=None
    block_icon = 'PyCraft/Textures/flintandsteelicon.png'
    block_color = color.hsv(0, 0, .9)
    block_model = 'PyCraft/Textures/flintandsteel.glb'
    defaultrotation = (-90,230,200)
    animationrotation = (-70, 200, 200)
    yorg = 0.75
    classaffect = []
    istool = True

#------------

# Animals

class Cow(Entity):
    def __init__(self, position=(0, 0, 0), model='PyCraft/Textures/cow.glb', texture=None, speed=1, **kwargs):
        super().__init__(
            parent=scene,
            position=position,
            model=model,
            texture=texture,
            scale=0.05,
            **kwargs
        )
        self.speed = speed
        self.target_position = None
        self.wandering_timer = time.time()
        self.gravity = 9.8
        self.grounded = False

    def update(self):
        if time.time() - self.wandering_timer > 2:
            self.wandering_timer = time.time()
            rand1 = random.uniform(-5, 5)
            rand2 = random.uniform(-5, 5)
            self.target_position = self.position + Vec3(
                rand1,
                0,
                rand2
            )
            self.rotation = Vec3(0, math.degrees(math.atan2(rand1, rand2)) + 180, 0)

        if self.target_position:
            direction = (self.target_position - self.position).normalized()
            self.position += direction * self.speed * time.dt

            if distance(self.position, self.target_position) < 0.1:
                self.target_position = None

        ray = raycast(self.position + Vec3(0, 1, 0), Vec3(0, -1, 0), distance=2, ignore=(self,))
        if ray.hit:
            self.grounded = True
            self.position = Vec3(self.position.x, ray.world_point.y + 0.9, self.position.z)
        else:
            self.grounded = False
        
        if not self.grounded:
            self.position -= Vec3(0, self.gravity * time.dt, 0)


worldgenerationvoxels = {
    'surfacevoxel': GroundVoxel,
    'minvoxel': Bedrock,
    'undersurfacevoxel': BrownVoxel,
    'deepvoxel': Voxel,
}

recipes = {
    (OakLogVoxel, OakLogVoxel, OakLogVoxel, OakLogVoxel): CraftingTableVoxel,

}

inventory_crafting_grid = [None, None, None, None]
current_crafting_result = None

block_break_times = {
    'Voxel': 4.0,
    'GroundVoxel': 0.8,
    'BrownVoxel': 0.5,
    'OakPlanksVoxel': 0.9,
    'IronOreVoxel': 7.5,
    'CoalOreVoxel': 5.0,
    'OakLogVoxel': 1.0,
    'TreeLeavesVoxel': 0.3,
    'GlassVoxel': 0.2,
    'WhiteWoolVoxel': 0.4,
    'BlackWoolVoxel': 0.4,
    'RedWoolVoxel': 0.4,
    'ObsidianVoxel': 50.0,
    'Bedrock': float('inf')  # essentially unbreakable,
}

mining_tools = {
    WoodPickaxe: 0.375,
    StonePickaxe: 0.1875,
    IronPickaxe: 0.125,
    GoldPickaxe: 0.0625,
    DiamondPickaxe: 0.1,
    None: 1,
}

block_breaking_stages = [
    'PyCraft/Textures/breaking1.png',
    'PyCraft/Textures/breaking2.png',
    'PyCraft/Textures/breaking3.png',
    'PyCraft/Textures/breaking4.png',
    'PyCraft/Textures/breaking5.png',
    'PyCraft/Textures/breaking6.png'
]

currently_breaking_block = None
block_break_start_time = None
block_initial_health = None
mouse_held = False

inventory_opened = False
inventory_blocks_pg1 = [
    {'voxel_class': Voxel, 'texture': Voxel.block_icon, 'color': color.hsv(0,0,0.9), 'name': 'Cobblestone'},
    {'voxel_class': BrownVoxel, 'texture': BrownVoxel.block_icon, 'color': color.hsv(0, 0, 0.8), 'name': 'Dirt'},
    {'voxel_class': GroundVoxel, 'texture': GroundVoxel.block_icon, 'color': color.hsv(0, 0, 0.9), 'name': 'Grass'},
    {'voxel_class': OakPlanksVoxel, 'texture': OakPlanksVoxel.block_icon, 'color': color.hsv(0,0,0.9), 'name': 'Oak Planks'},
    {'voxel_class': GlassVoxel, 'texture': GlassVoxel.block_icon, 'color': color.hsv(0,0,0.9), 'name': 'Glass'},
    {'voxel_class': IronOreVoxel, 'texture': IronOreVoxel.block_icon, 'color': color.hsv(0,0,0.9), 'name': 'Iron Ore'},
    {'voxel_class': CoalOreVoxel, 'texture': CoalOreVoxel.block_icon, 'color': color.hsv(0,0,0.9), 'name': 'Coal Ore'},
    {'voxel_class': Bedrock, 'texture': Bedrock.block_icon, 'color': color.hsv(0,0,1), 'name': 'Bedrock'},
    {'voxel_class': ObsidianVoxel, 'texture': ObsidianVoxel.block_icon, 'color': color.hsv(0,0,0.9), 'name': 'Obsidian'},

]
inventory_blocks_pg2 = [
    {'voxel_class': WhiteWoolVoxel, 'texture': WhiteWoolVoxel.block_icon, 'color': color.hsv(0,0,0.9), 'name': 'White Wool'},
    {'voxel_class': BlackWoolVoxel, 'texture': BlackWoolVoxel.block_icon, 'color': color.hsv(0,0,0.9), 'name': 'Black Wool'},
    {'voxel_class': RedWoolVoxel, 'texture': RedWoolVoxel.block_icon, 'color': color.hsv(0,0,0.9), 'name': 'Red Wool'},

]

inventory_blocks_pg3 = [
    {'voxel_class': WoodPickaxe, 'texture': WoodPickaxe.block_icon, 'color': color.hsv(0,0,0.9), 'name': 'Wooden Pickaxe'},
    {'voxel_class': StonePickaxe, 'texture': StonePickaxe.block_icon, 'color': color.hsv(0,0,0.9), 'name': 'Stone Pickaxe'},
    {'voxel_class': IronPickaxe, 'texture': IronPickaxe.block_icon, 'color': color.hsv(0,0,0.9), 'name': 'Iron Pickaxe'},
    {'voxel_class': GoldPickaxe, 'texture': GoldPickaxe.block_icon, 'color': color.hsv(0,0,0.9), 'name': 'Gold Pickaxe'},
    {'voxel_class': DiamondPickaxe, 'texture': DiamondPickaxe.block_icon, 'color': color.hsv(0,0,0.9), 'name': 'Diamond Pickaxe'},
    {'voxel_class': Cookie, 'texture': Cookie.block_icon, 'color': color.hsv(0,0,0.9), 'name': 'Cookie'},
    {'voxel_class': FlintAndSteel, 'texture': FlintAndSteel.block_icon, 'color': color.hsv(0,0,0.9), 'name': 'Flint and Steel'},
]

inventory_blocks_pg4 = [
    {'voxel_class': CraftingTableVoxel, 'texture': CraftingTableVoxel.block_icon, 'color': color.hsv(0,0,0.9), 'name': 'Crafting Table'},
    {'voxel_class': SandVoxel, 'texture': SandVoxel.block_icon, 'color': color.hsv(0,0,0.9), 'name': 'Sand'},
    {'voxel_class': GravelVoxel, 'texture': GravelVoxel.block_icon, 'color': color.hsv(0,0,0.9), 'name': 'Gravel'},
    {'voxel_class': SlimeVoxel, 'texture': SlimeVoxel.block_icon, 'color': color.hsv(0,0,0.9), 'name': 'Slime'},
    {'voxel_class': DiamondBlock, 'texture': DiamondBlock.block_icon, 'color': color.hsv(0,0,0.9), 'name': 'DiamondBlock'},
    {'voxel_class': OakSlabVoxel, 'texture': OakSlabVoxel.block_icon, 'color': color.hsv(0,0,0.9), 'name': 'Oak Slab'},
]

pages = {
    1: inventory_blocks_pg1,
    2: inventory_blocks_pg2,
    3: inventory_blocks_pg3,
    4: inventory_blocks_pg4,
}
currentpagedata = {
    'page': inventory_blocks_pg1,
    'pagenumber': '1',
    'pagelabel': 'Base Blocks',
    }
pagelabels = {
    '1': 'Base Blocks',
    '2': 'Wools',
    '3': 'Tools',
    '4': 'Miscellaneous',
}


game_api = {
    'inventory_blocks_pg1': inventory_blocks_pg1,
    'inventory_blocks_pg2': inventory_blocks_pg2,
    'block_class_mapping': block_class_mapping,
    'pages': pages,
    'pagelabels': pagelabels,
    'worldgenerationvoxels': worldgenerationvoxels,

}



clouds = []

animals = []

def spawn_animals(num=5):
    for _ in range(num):
        position = Vec3(
            random.randint(-10,10),
            1,
            random.randint(-10,10)
        )
        animal = Cow(position=position, model='PyCraft/Textures/cow.glb', texture=None)
        animals.append(animal)

def generate_clouds(number_of_clouds=10):
    for _ in range(number_of_clouds):
        x = random.randint(-50, 50)
        z = random.randint(-50,50)
        y = 20
        width = random.randint(6, 12)
        depth = random.randint(4, 8)
        height = 1
        cloud = Cloud(position=(x,y,z), size=(width, height, depth))
        clouds.append(cloud)

generate_clouds()

def load_mod_states(mods_folder=f'{script_dir}/PyCraft/mods'):
    config_path = os.path.join(mods_folder, 'mods_config.json')
    mod_states = {}

    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            mod_states = json.load(f)
    
    current_mod_files = [f for f in os.listdir(mods_folder) if f.endswith('.py') and f != 'mods_config.json']
    current_mod_names = [f[:-3] for f in current_mod_files]

    updated_mod_states = {}
    for mod_name in current_mod_names:
        if mod_name in mod_states:
            updated_mod_states[mod_name] = mod_states[mod_name]
        else:
            updated_mod_states[mod_name] = False

    mod_states = updated_mod_states

    with open(config_path, 'w') as f:
        json.dump(mod_states, f)

    return mod_states

def save_mod_states(mod_states, mods_folder=f'{script_dir}/PyCraft/mods'):
    config_path = os.path.join(mods_folder, 'mods_config.json')
    with open(config_path, 'w') as f:
        json.dump(mod_states, f)

world_mods = []
def load_mods(mod_states, mods_folder=f'{script_dir}/PyCraft/mods', game_api=None):
    global world_mods
    for filename in os.listdir(mods_folder):
        if filename.endswith('.py'):
            mod_name = filename[:-3]
            if mod_states.get(mod_name, False):
                file_path = os.path.join(mods_folder, filename)
                spec = importlib.util.spec_from_file_location(mod_name, file_path)
                mod = importlib.util.module_from_spec(spec)
                sys.modules[mod_name] = mod
                try:
                    spec.loader.exec_module(mod)
                except Exception as e:
                    print(f"Failed to load mod '{mod_name}': {e}")
                    continue

                if hasattr(mod, 'initialize') and hasattr(mod, 'deinitialize') and callable(mod.initialize) and callable(mod.deinitialize):
                    try:
                        mod.initialize(game_api)
                        world_mods.append(mod_name)
                    except Exception as e:
                        print(f"Error initializing mod '{mod_name}': {e}")
                else:
                    if not hasattr(mod, 'initialize'):
                        print(f"Mod {mod_name} does not have an 'initialize' function.")
                    if not hasattr(mod, 'deinitialize'):
                        print(f"Mod {mod_name} does not have a 'deinitialize' function.")

mods_folder = f'{script_dir}\PyCraft\mods'

mod_states = load_mod_states(mods_folder)

def generate_tree(x, y, z):
    tree_type = random.randint(1,2)
    if tree_type == 1:
        leaves = TreeLeavesVoxel
        leavestype = 'TreeLeavesVoxel'
    elif tree_type == 2:
        leaves = SakuraLeaves
        leavestype = 'SakuraLeaves'
    voxel = OakLogVoxel(position=(x,y+1,z))
    world_data.append({'position': [x, y+1, z], 'block_type': 'OakLogVoxel'})
    voxel = OakLogVoxel(position=(x,y+2,z))
    world_data.append({'position': [x, y+2, z], 'block_type': 'OakLogVoxel'})
    voxel = OakLogVoxel(position=(x,y+3,z))
    world_data.append({'position': [x, y+3, z], 'block_type': 'OakLogVoxel'})
    voxel = leaves(position=(x,y+3,z+1))
    world_data.append({'position': [x, y+3, z+1], 'block_type': leavestype})
    voxel = leaves(position=(x+1,y+3,z+1))
    world_data.append({'position': [x+1, y+3, z+1], 'block_type': leavestype})
    voxel = leaves(position=(x-1,y+3,z+1))
    world_data.append({'position': [x-1, y+3, z+1], 'block_type': leavestype})
    voxel = leaves(position=(x,y+3,z-1))
    world_data.append({'position': [x, y+3, z-1], 'block_type': leavestype})
    voxel = leaves(position=(x+1,y+3,z-1))
    world_data.append({'position': [x+1, y+3, z-1], 'block_type': leavestype})
    voxel = leaves(position=(x-1,y+3,z-1))
    world_data.append({'position': [x-1, y+3, z-1], 'block_type': leavestype})
    voxel = leaves(position=(x+1,y+3,z))
    world_data.append({'position': [x+1, y+3, z], 'block_type': leavestype})
    voxel = leaves(position=(x-1,y+3,z))
    world_data.append({'position': [x-1, y+3, z], 'block_type': leavestype})
    voxel = leaves(position=(x,y+4,z+1))
    world_data.append({'position': [x, y+4, z+1], 'block_type': leavestype})
    voxel = leaves(position=(x+1,y+4,z+1))
    world_data.append({'position': [x+1, y+4, z+1], 'block_type': leavestype})
    voxel = leaves(position=(x-1,y+4,z+1))
    world_data.append({'position': [x-1, y+4, z+1], 'block_type': leavestype})
    voxel = leaves(position=(x,y+4,z-1))
    world_data.append({'position': [x, y+4, z-1], 'block_type': leavestype})
    voxel = leaves(position=(x+1,y+4,z-1))
    world_data.append({'position': [x+1, y+4, z-1], 'block_type': leavestype})
    voxel = leaves(position=(x-1,y+4,z-1))
    world_data.append({'position': [x-1, y+4, z-1], 'block_type': leavestype})
    voxel = leaves(position=(x+1,y+4,z))
    world_data.append({'position': [x+1, y+4, z], 'block_type': leavestype})
    voxel = leaves(position=(x-1,y+4,z))
    world_data.append({'position': [x-1, y+4, z], 'block_type': leavestype})
    voxel = leaves(position=(x,y+5,z))
    world_data.append({'position': [x, y+5, z], 'block_type': leavestype})

def generate_world(worldseed, worldsize, worlddepth):
    global worlddimensions, min_y, seedvalue, worldver, inventory_blocks_pg1, inventory_blocks_pg2
    load_mods(mod_states, mods_folder, game_api)
    clear_world()
    worldver = game_version
    try:
        worldseed = int(worldseed)
    except:
        print('Invalid seed. Generating random seed')
        worldseed = random.randint(1,1000000)
    noise = PerlinNoise (octaves=3, seed=worldseed)
    seedvalue = worldseed
    min_y = -worlddepth
    worlddimensions = worldsize #World dimensions are twice this number 
    for z in range(-worlddimensions,worlddimensions):
        for x in range(-worlddimensions,worlddimensions):
            surface_y = noise([x * .02,z * .02])
            surface_y = math.floor(surface_y*7.5)
            for y in range(min_y, surface_y + 1):
                position = (x, y, z)
                if y == surface_y:
                    voxel = worldgenerationvoxels['surfacevoxel'](position=position)
                    block_type = (type(voxel).__name__)
                    treegenerator = random.randint(0,65)
                    if treegenerator == 5:
                        generate_tree(x,y,z)
                elif y == min_y:
                    voxel = worldgenerationvoxels['minvoxel'](position=position)
                    block_type = (type(voxel).__name__)
                elif y > surface_y - 3:
                    voxel = worldgenerationvoxels['undersurfacevoxel'](position=position)
                    block_type = (type(voxel).__name__)
                else:
                    oregenerator = random.randint(0,20)
                    if oregenerator == 5 and y < surface_y - 10:
                        voxel = IronOreVoxel(position=position)
                        block_type = 'IronOreVoxel'
                    elif oregenerator == 15:
                        voxel = CoalOreVoxel(position=position)
                        block_type = 'CoalOreVoxel'
                    else:
                        voxel = worldgenerationvoxels['deepvoxel'](position=position)
                        block_type = (type(voxel).__name__)
                world_data.append({'position': [x, y, z], 'block_type': block_type})
    build_barriers(worlddimensions, min_y)
    spawn_animals(10)
    player.position = Vec3(*[0,0,0])
    destroy_play_menu()
    build_hotbar()
    update_equipped_slot(slot1)
    mouse.locked = True

def build_barriers(dimensions, miny):
    global worlddimensions, min_y
    worlddimensions = dimensions
    min_y = miny
    wall_thickness = 1
    wall_height = 200
    voxel_size = 1

    min_xz = -dimensions
    max_xz = dimensions - 1
    terrain_min_xz = min_xz - voxel_size / 2
    terrain_max_xz = max_xz + voxel_size / 2
    terrain_width_xz = terrain_max_xz - terrain_min_xz

    north_wall = Entity(
        model = 'cube',
        scale = (terrain_width_xz, wall_height, wall_thickness),
        position = (
            (terrain_min_xz + terrain_max_xz) / 2,
            wall_height / 2 + miny,
            terrain_max_xz + wall_thickness / 2,
        ),
        collider = 'box',
        visible = False,
        destroyable = False,
        wall = True
    )
    south_wall = Entity(
        model = 'cube',
        scale = (terrain_width_xz, wall_height, wall_thickness),
        position = (
            (terrain_min_xz + terrain_max_xz) / 2,
            wall_height / 2 + miny,
            terrain_min_xz - wall_thickness / 2,
        ),
        collider = 'box',
        visible = False,
        destroyable = False,
        wall = True
    )
    east_wall = Entity(
        model = 'cube',
        scale = (wall_thickness, wall_height, terrain_width_xz),
        position=(
            terrain_max_xz + wall_thickness / 2,
            wall_height / 2 + miny,
            (terrain_min_xz + terrain_max_xz) / 2
        ),
        collider = 'box',
        visible = False,
        destroyable = False,
        wall = True
    )
    west_wall = Entity(
        model = 'cube',
        scale = (wall_thickness, wall_height, terrain_width_xz),
        position=(
            terrain_min_xz + wall_thickness / 2 - 1,
            wall_height / 2 + miny,
            (terrain_min_xz + terrain_max_xz) / 2
        ),
        collider = 'box',
        visible = False,
        destroyable = False,
        wall = True
    )




def build_hotbar():
    global hotbar, selector, slot1, slot2, slot3, slot4, slot5, slot6, slot7, slot8, slot9, slotselected, hearts, slots, slot1amount, slot2amount, slot3amount, slot4amount, slot5amount, slot6amount, slot7amount, slot8amount, slot9amount
    hotbar = Entity(
    parent=camera.ui,
    model='quad',
    texture = 'PyCraft/Textures/hotbar.png',
    scale=(0.5, 0.055),
    position=(0,-0.45,1),
    visible=True  
    )
    selector = Button( 
                    color=color.rgb(0.2, 0.2, 0.2), 
                    position=(-0.225, -0.45, 0), 
                    scale=(0.045, 0.045),
                    currentslot = 'slot1',
                    visible=True
                    )
    slot1 = Button( 
                    color=color.hsv(0, 0, .9),
                    texture='PyCraft/Textures/cobblestoneblock.png',
                    position=(-0.225, -0.45, -1), 
                    scale=(0.045, 0.045),
                    hand_color = color.hsv(0, 0, .9),
                    on_click = lambda: equip_block(slot1) if holding_block else swap_block(slot1),
                    equipped=Voxel if creative else False,
                    amount = 0,
                    visible = True if creative else False
                    )
    slot1amount = Text(
        parent=camera.ui,
        font="PyCraft/Textures/Fonts/mc.ttf", 
        text=str(slot1.amount),   
        origin=(0, 0),      
        scale=1,            
        color=color.white,   
        position=(-0.215, -0.463, -2),
        visible=True           
    )   
    slot2 = Button( 
                    color=color.hsv(0, 0, .9),
                    texture='PyCraft/Textures/dirtblock.png',
                    position=(-0.168, -0.45, -1), 
                    scale=(0.045, 0.045),
                    hand_color = color.hsv(30, 0.5, 0.7),
                    on_click = lambda: equip_block(slot2) if holding_block else swap_block(slot2),
                    equipped=BrownVoxel if creative else False,
                    amount = 0,
                    visible = True if creative else False
                    )
    slot2amount = Text(
        parent=camera.ui,
        font="PyCraft/Textures/Fonts/mc.ttf", 
        text=str(slot2.amount),   
        origin=(0, 0),      
        scale=1,            
        color=color.white,   
        position=(-0.16, -0.463, -2),
        visible=True           
    )
    slot3 = Button( 
                    color=color.hsv(0, 0, 0.9),
                    position=(-0.114, -0.45, -1), 
                    scale=(0.045, 0.045),
                    hand_color = color.hsv(30, 0.4, 0.8),
                    on_click = lambda: equip_block(slot3) if holding_block else swap_block(slot3),
                    visible=False,
                    amount = 0,
                    equipped=False
                    )
    slot3amount = Text(
        parent=camera.ui,
        font="PyCraft/Textures/Fonts/mc.ttf", 
        text=str(slot3.amount),   
        origin=(0, 0),      
        scale=1,            
        color=color.white,   
        position=(-0.105, -0.463, -2),
        visible=True           
    )
    slot4 = Button( 
                    color=color.hsv(0, 0, 1),
                    position=(-0.057, -0.45, -1), 
                    scale=(0.045, 0.045),
                    hand_color = color.hsv(0,0,.9),
                    on_click = lambda: equip_block(slot4) if holding_block else swap_block(slot4),
                    equipped='gun' if creative else False,
                    amount = 0,
                    visible = True if creative else False
                    )
    slot4amount = Text(
        parent=camera.ui,
        font="PyCraft/Textures/Fonts/mc.ttf", 
        text=str(slot4.amount),   
        origin=(0, 0),      
        scale=1,            
        color=color.white,   
        position=(-0.05, -0.463, -2),
        visible=True           
    )
    slot5 = Button( 
                    color=color.hsv(0, 0, .9),
                    texture='PyCraft/Textures/oakplanksblock.png',
                    position=(0, -0.45, -1), 
                    scale=(0.045, 0.045),
                    hand_color = color.hsv(0,0,.9),
                    on_click = lambda: equip_block(slot5) if holding_block else swap_block(slot5),
                    equipped=OakPlanksVoxel if creative else False,
                    amount = 0,
                    visible = True if creative else False
                    )
    slot5amount = Text(
        parent=camera.ui,
        font="PyCraft/Textures/Fonts/mc.ttf", 
        text=str(slot5.amount),   
        origin=(0, 0),      
        scale=1,            
        color=color.white,   
        position=(0.0075, -0.463, -2),
        visible=True           
    )
    slot6 = Button( 
                    color=color.hsv(0, 0, .9),
                    texture='PyCraft/Textures/glassblock.png',
                    position=(0.055, -0.45, -1), 
                    scale=(0.045, 0.045),
                    hand_color = color.hsv(0,0,.9),
                    on_click = lambda: equip_block(slot6) if holding_block else swap_block(slot6),
                    equipped=GlassVoxel if creative else False,
                    amount = 0,
                    visible = True if creative else False
                    )
    slot6amount = Text(
        parent=camera.ui,
        font="PyCraft/Textures/Fonts/mc.ttf", 
        text=str(slot6.amount),   
        origin=(0, 0),      
        scale=1,            
        color=color.white,   
        position=(0.065, -0.463, -2),
        visible=True           
    )
    slot7 = Button( 
                    color=color.hsv(0, 0, .9),
                    texture='PyCraft/Textures/dirtblock.png',
                    position=(0.110, -0.45, -1), 
                    scale=(0.045, 0.045),
                    hand_color = color.hsv(0,0,.9),
                    on_click = lambda: equip_block(slot7) if holding_block else swap_block(slot7),
                    equipped=None,
                    amount = 0,
                    visible=False
                    )
    slot7amount = Text(
        parent=camera.ui,
        font="PyCraft/Textures/Fonts/mc.ttf", 
        text=str(slot7.amount),   
        origin=(0, 0),      
        scale=1,            
        color=color.white,   
        position=(0.12, -0.463, -2),
        visible=True           
    )
    slot8 = Button( 
                    color=color.hsv(0, 0, .9),
                    texture='PyCraft/Textures/dirtblock.png',
                    position=(0.165, -0.45, -1), 
                    scale=(0.045, 0.045), 
                    hand_color = color.hsv(0,0,.9),
                    on_click = lambda: equip_block(slot8) if holding_block else swap_block(slot8),
                    equipped=None,
                    amount = 0,
                    visible=False
                    )
    slot8amount = Text(
        parent=camera.ui,
        font="PyCraft/Textures/Fonts/mc.ttf", 
        text=str(slot8.amount),   
        origin=(0, 0),      
        scale=1,            
        color=color.white,   
        position=(0.175, -0.463, -2),
        visible=True           
    )
    slot9 = Button( 
                    color=color.hsv(0, 0, .9),
                    texture='PyCraft/Textures/dirtblock.png',
                    position=(0.22, -0.45, -1), 
                    scale=(0.045, 0.045),
                    hand_color = color.hsv(0,0,.9),
                    on_click = lambda: equip_block(slot9) if holding_block else swap_block(slot9), 
                    equipped=None,
                    amount = 0,
                    visible=False
                    )
    slot9amount = Text(
        parent=camera.ui,
        font="PyCraft/Textures/Fonts/mc.ttf", 
        text=str(slot9.amount),   
        origin=(0, 0),      
        scale=1,            
        color=color.white,   
        position=(0.23, -0.463, -2),
        visible=True           
    )
    slots = [slot1, slot2, slot3, slot4, slot5, slot6, slot7, slot8, slot9]
    spacing = -0.0235
    if not creative:
        for i in range(10):
            heart = Button(
                color=color.hsv(0, 0, .9),
                texture='PyCraft/Textures/fullheart.png',
                position=(-0.03 + i * spacing, -0.4, -1),
                scale=(0.023, 0.023),
            )
            hearts.append(heart)
        for i in range(10):
            hunger = Button(
                color=color.hsv(0, 0, .9),
                texture='PyCraft/Textures/hungerfull.png',
                position=(0.235 + i * spacing, -0.4, -1),
                scale=(0.032, 0.033),
            )
            hungers.append(hunger)
    slotselected = slot1

hand = Entity(model='cube',texture='PyCraft/Textures/cobblestone.png', color=color.hsv(0,0,0.9), scale=(0.5,0.5,0.5), rotation=(0,0,0), position=(0,0,0), parent=camera)

def update_hand_position():
    if selected == 'ak':
        hand.position = (0.5, -0.5, 2)
    else:
        hand.position = (0.5, -0.5, 1)

def clear_world():
    for entity in scene.entities[:]:
        if isinstance(entity, Button) and entity != player and hasattr(entity, 'isblock') and not hasattr(entity, 'wall'):
            destroy(entity)

def rebuild_world_from_data():

    for block in world_data:
        position = block['position']
        block_type = block['block_type']
        x, y, z = position
        position = Vec3(x,y,z)

        block_class = block_class_mapping.get(block_type)
        if block_class:
            block_class(position=position)


        

def save_world(filename=f'{script_dir}\\PyCraft\\Worlds\\world_save.json'):
    global worlddimensions, min_y, saved_world_name
    saved_world_name = filename[43:]
    print(saved_world_name)
    save_data = {
        'world_data': world_data,
        'player_position': [player.position.x, player.position.y, player.position.z],
        'world_size': [worlddimensions, min_y],
        'world_version': game_version,
        'last_save_date': f'{current_datetime.date()}',
        'creative': creative,
        'health': health,
        'hotbar': [slot.equipped.__name__ if slot.equipped and isinstance(slot.equipped, type) else slot.equipped if slot.equipped else None for slot in slots],
        'hotbaramounts': [slot.amount for slot in slots]
    }
    if world_mods != []:
        save_data['world_mods'] = world_mods
    if seedvalue != None:
        save_data['world_seed'] = seedvalue
    with open(filename, 'w') as f:
        json.dump(save_data, f)

def outdated_check(filename):
    with open(filename, 'r') as f:
        save_data = json.load(f)
    worldver = save_data.get('world_version', 'Unknown')
    if worldver != game_version:
        outdated_popup(filename, worldver)
        return
    else:
        load_world(filename)

def load_world(filename, olderworld=False):
    global world_data, worlddimensions, worldver, seedvalue, saved_world_name, inventory_blocks_pg1, inventory_blocks_pg2, slots, last_y_position, creative, health
    saved_world_name = filename[43:]
    with open(filename, 'r') as f:
        save_data = json.load(f)
    world_data = save_data['world_data']
    player_position = save_data.get('player_position', [0,0,0])
    worldver = save_data.get('world_version', 'Unknown')
    seedvalue = save_data.get('world_seed', 'Unknown')
    neededmods = save_data.get('world_mods', None)
    iscreative = save_data.get('creative', 'Unknown')
    loadedhealth = save_data.get('health', 100)
    health = loadedhealth
    if iscreative and not iscreative == 'Unknown':
        creative = True
    elif iscreative == 'Unknown':
        print('Gamemode not found in save file, defaulting to survival.')
        creative = False
    elif not iscreative:
        creative = False
    missingmods = []
    if neededmods:
        for mod in neededmods:
            if not mod in mod_states or not mod_states[mod]:
                missingmods.append(mod)
    if missingmods != []:
        print(f"World '{filename}' requires mods: {missingmods}")
        if olderworld:
            open_play_menu()
        return
    try:
        worldproperties = save_data['world_size']
    except:
        print(f'ERROR: World {filename} is corrupt')
        if olderworld:
            open_play_menu()
        return
    load_mods(mod_states, mods_folder, game_api)
    destroy_play_menu()
    build_barriers(worldproperties[0], worldproperties[1])
    clear_world()
    rebuild_world_from_data()
    build_hotbar()
    hotbar_state = save_data.get('hotbar', [])
    for slot, equipped_name in zip(slots, hotbar_state):
        if equipped_name:
            if equipped_name in block_class_mapping:
                slot.equipped = block_class_mapping[equipped_name]
                slot.hand_color = block_class_mapping[equipped_name].block_color  
                slot.visible = True
                slot.texture = block_class_mapping[equipped_name].block_icon
            else:
                slot.equipped = equipped_name  
        else:
            slot.equipped = None
            slot.visible = False
    hotbar_amounts = save_data.get('hotbaramounts', [])
    for slot, amount in zip(slots, hotbar_amounts):
        if amount:
            slot.amount = amount
        else:
            if slot.equipped:
                slot.amount = 1
            else:
                slot.amount = 0
    last_y_position = None
    player.position = Vec3(*player_position)
    mouse.locked = True
    if not creative:
        update_hearts()
    update_equipped_slot(slotselected)

def get_world_timesaved(filename):
    with open(filename, 'r') as f:
        save_data = json.load(f)
    lasttimesave = save_data.get('last_save_date', 'Unknown')
    return lasttimesave

settings_opened = False
def toggle_mouse_lock():
    global settings_opened, pause_menu_open, paused
    if mouse.locked:
        mouse.locked = False
        mouse.visible = True
        pause_menu.visible = True
        build_pause_menu()
        pause_menu_open = True
        paused = True
    else:
        mouse.locked = True
        mouse.visible = False
        pause_menu.visible = False
        if settings_opened:
            close_settings()
        destroy_pause_menu()
        pause_menu_open = False
        paused = False
pause_menu = Entity(
    parent=camera.ui,
    model='quad',
    scale=(2, 2, 1),
    color=color.rgba(0,0,0, 0.5),
    position=(0,0,-3),  
    visible=False  
)
def toggle_fullscreen():
    window.fullscreen = not window.fullscreen
    fullscreen_button.text = 'Fullscreen: Disabled' if not window.fullscreen else 'Fullscreen: Enabled'

def open_settings():
    global settings_label, back_button, fullscreen_button, settings_opened, fov_slider, gamemode_button, creative
    settings_opened = True
    destroy_pause_menu()
    settings_label = Entity(
    parent=pause_menu,
    model='quad',
    texture = 'PyCraft/Textures/settingslabel.png',
    scale=(0.35, 0.15),
    position=(0, 0.15, -1),
    visible=True  
    )   
    fullscreen_button = Button(
        parent=pause_menu,
        font="PyCraft/Textures/Fonts/mc.ttf",
        text='Fullscreen: Disabled' if not window.fullscreen else 'Fullscreen: Enabled',
        color=color.light_gray,
        texture="PyCraft/Textures/buttontexture.png",
        highlight_color=color.rgb(0.745, 0.729, 1),
        scale=(0.2, 0.025),  # Size of the button
        position=(0, 0),  # Position on the screen
        on_click = lambda: toggle_fullscreen()
    )

    gamemode_button = Button(
        parent=pause_menu,
        font="PyCraft/Textures/Fonts/mc.ttf",
        text='Gamemode: Survival' if not creative else 'Gamemode: Creative',
        color=color.light_gray,
        texture="PyCraft/Textures/buttontexture.png",
        highlight_color=color.rgb(0.745, 0.729, 1),
        scale=(0.2, 0.025),  # Size of the button
        position=(0, -0.05),  # Position on the screen
        on_click = lambda: toggle_gamemode()
    )
mob_spawning_enabled = True
block_drops_enabled = True

def toggle_mob_spawning():
    global mob_spawning_enabled
    mob_spawning_enabled = not mob_spawning_enabled
    if not mob_spawning_enabled:
        clear_mobs()
    print(f"Mob Spawning: {'Enabled' if mob_spawning_enabled else 'Disabled'}")

def toggle_block_drops():
    global block_drops_enabled
    block_drops_enabled = not block_drops_enabled
    if not block_drops_enabled:
        clear_block_drops()
    print(f"Block Drops: {'Enabled' if block_drops_enabled else 'Disabled'}")

def clear_mobs():
    for entity in scene.entities[:]:
        if hasattr(entity, 'is_mob') and entity.is_mob:
            destroy(entity)
    print("All mobs cleared.")

def clear_block_drops():
    for entity in scene.entities[:]:
        if hasattr(entity, 'is_block_drop') and entity.is_block_drop:
            destroy(entity)
    print("All block drops cleared.")


    fov_slider = Slider(
        min=60, max=120, default=camera.fov,
        parent=pause_menu,
        font="PyCraft/Textures/Fonts/mc.ttf",
        text='FOV',
        color=color.gray,
        step=1,
        position = (-0.099, 0.05),
        scale = (0.4, 0.5),
        dynamic=True,
    )

    def set_fov():
        camera.fov = fov_slider.value
        print(camera.fov)

    fov_slider.on_value_changed = set_fov

    back_button = Button(
        parent=pause_menu,
        font="PyCraft/Textures/Fonts/mc.ttf",
        text='Back',
        color=color.light_gray,
        texture="PyCraft/Textures/buttontexture.png",
        highlight_color=color.rgb(0.745, 0.729, 1),
        scale=(0.2, 0.025),  # Size of the button
        position=(0, -0.1),  # Position on the screen
        on_click = lambda: close_settings()
    )

def close_settings():
    global settings_opened
    destroy(back_button)
    destroy(settings_label)
    destroy(fullscreen_button)
    destroy(fov_slider)
    destroy(gamemode_button)
    build_pause_menu()
    settings_opened = False

def toggle_gamemode():
    global hearts, hungers, gamemode_button, creative
    if creative:
        spacing = -0.0235
        for i in range(10):
            heart = Button(
                color=color.hsv(0, 0, .9),
                texture='PyCraft/Textures/fullheart.png',
                position=(-0.03 + i * spacing, -0.4, -1),
                scale=(0.023, 0.023),
            )
            hearts.append(heart)
        for i in range(10):
            hunger = Button(
                color=color.hsv(0, 0, .9),
                texture='PyCraft/Textures/hungerfull.png',
                position=(0.235 + i * spacing, -0.4, -1),
                scale=(0.032, 0.033),
            )
            hungers.append(hunger)
        creative = False
        gamemode_button.text = 'Gamemode: Survival'
    else:
        for heart in hearts:
            destroy(heart)
        for hunger in hungers:
            destroy(hunger)
        creative = True
        gamemode_button.text = 'Gamemode: Creative'

def destroy_pause_menu():
    global save_field_open, confirm_save_button
    if save_field_open:
        destroy(save_name_field)
        destroy(confirm_save_button)
        save_field_open = False
    destroy(resume_button)
    destroy(quit_button)
    destroy(settings_button)
    destroy(pause_label)
    destroy(save_button)
    destroy(load_button)

def build_pause_menu():
    global resume_button, quit_button, pause_label, settings_button, save_button, load_button, gen_button, save_field_open, confirm_save_button, saved_world_name
    save_field_open = False
    resume_button = Button(
        parent=pause_menu,
        font="PyCraft/Textures/Fonts/mc.ttf",
        text='Resume',
        color=color.light_gray,
        texture="PyCraft/Textures/buttontexture.png",
        highlight_color=color.rgb(0.745, 0.729, 1),
        scale=(0.2, 0.025),  # Size of the button
        position=(0, 0, -1),  # Position on the screen
        on_click = lambda: toggle_mouse_lock()
    )
    if saved_world_name != None:
        save_button = Button(
        parent=pause_menu,
        font="PyCraft/Textures/Fonts/mc.ttf",
        text='Save World',
        color=color.light_gray,
        texture="PyCraft/Textures/buttontexture.png",
        highlight_color=color.rgb(0.745, 0.729, 1),
        scale=(0.2, 0.025),
        position=(0, -0.1, -1),  
        on_click = lambda: save_world(f'{script_dir}\\PyCraft\\Worlds\\{saved_world_name}')
        )
    else:
        save_button = Button(
            parent=pause_menu,
            font="PyCraft/Textures/Fonts/mc.ttf",
            text='Save World',
            color=color.light_gray,
            texture="PyCraft/Textures/buttontexture.png",
            highlight_color=color.rgb(0.745, 0.729, 1),
            scale=(0.2, 0.025),
            position=(0, -0.1, -1),  
            on_click = lambda: toggle_save_field()
        )
        def toggle_save_field():
            global save_field_open, save_name_field,confirm_save_button
            if save_field_open:
                destroy(save_name_field)
                destroy(confirm_save_button)
                save_field_open = False
            else:
                save_name_field = InputField(
                    parent=pause_menu,
                    default_value='World Name',
                    scale=(0.15, 0.02), 
                    position=(0.15, -0.1, -1)
                    )
                confirm_save_button = Button(
                    parent=pause_menu,
                    font="PyCraft/Textures/Fonts/mc.ttf",
                    text='Confirm',
                    color=color.light_gray,
                    texture="PyCraft/Textures/buttontexture.png",
                    highlight_color=color.rgb(0.745, 0.729, 1),
                    scale=(0.2, 0.025),
                    position=(0.3, -0.1, -1),  
                    on_click = lambda: save_world(f'{script_dir}\\PyCraft\\Worlds\\{save_name_field.text}.json')
                )
                save_field_open = True

    load_button = Button(
        parent=pause_menu,
        font="PyCraft/Textures/Fonts/mc.ttf",
        text='Load World',
        color=color.light_gray,
        texture="PyCraft/Textures/buttontexture.png",
        highlight_color=color.rgb(0.745, 0.729, 1),
        scale=(0.2, 0.025), 
        position=(0, -0.2, -1),  
        on_click = lambda: load_world()
    )


    quit_button = Button(
        parent=pause_menu,
        font="PyCraft/Textures/Fonts/mc.ttf",
        text='Quit',
        color=color.light_gray,
        texture="PyCraft/Textures/buttontexture.png",
        highlight_color=color.rgb(0.745, 0.729, 1),
        scale=(0.2, 0.025), 
        position=(0, -0.15, -1),  
        on_click = application.quit
    )
    settings_button = Button(
        parent=pause_menu,
        font="PyCraft/Textures/Fonts/mc.ttf",
        text='Settings',
        color=color.light_gray,
        texture="PyCraft/Textures/buttontexture.png",
        highlight_color=color.rgb(0.745, 0.729, 1),
        scale=(0.2, 0.025), 
        position=(0, -0.05, -1),  
        on_click = lambda: open_settings()
    )
    pause_label = Entity(
    parent=pause_menu,
    model='quad',
    texture = 'PyCraft/Textures/pausedlabel.png',
    scale=(0.35, 0.15),
    position=(0, 0.15, -1),
    visible=True  
    )   

def leavetomenu():
    destroy_pause_menu()
    build_main_menu()

multiplayer_menu_open = False
menu_settings_open = False
def build_main_menu():
    global mainbackground,title_screen_open,titletext,tiptext,singleplayer_button,multiplayer_button,menu_quit_button,main_menu_open, mod_menu_button, multiplayer_menu_open, menu_settings_button, menu_settings_open, version_text
    if play_menu_open:
        destroy_play_menu()
    if multiplayer_menu_open:
        multiplayer_menu_open = False
        destroy(comingsoon)
        destroy(returntomenu_button)
        destroy(mainbackground)
    if menu_settings_open:
        menu_settings_open = False
        destroy(settings_text)
        destroy(returntomenu_button)
        destroy(mainbackground)
        destroy(fullscreen_button)
    quips = ["Minecraft, but worse!", "Created by Mabindy!", "Minecraft.. in Python!?", f"Version {game_version}", "Minecraft, but really small!", "Added Herobrine", "Removed Herobrine", "You couldn't afford real Minecraft?", "Minecraft, with a gun.. for some reason", "O_O"]
    main_menu_open = True
    title_screen_open = True
    mainbackground = Entity(
    parent=camera.ui,
    model='quad',
    texture = 'PyCraft/Textures/wallpaper.png',
    scale=(1.8, 1, -1),  
    visible=True  
    )
    titletext = Entity(
    parent=camera.ui,
    model='quad',
    texture = 'PyCraft/Textures/titlelogo.png',
    scale=(0.75, 0.3),
    position=(0,0.25),
    visible=True  
    )
    tiptext = Text(
    parent=camera.ui,
    font="PyCraft/Textures/Fonts/mc.ttf",
    text=quips[random.randint(0,len(quips)-1)],   
    origin=(0, 0),      
    scale=1.5,
    rotation_z = -20,            
    color=color.yellow,   
    position=(0.25, 0.2),            
    )
    version_text = Text(
    parent=camera.ui,
    font="PyCraft/Textures/Fonts/mc.ttf",
    text=f'Version {game_version}',   
    origin=(0, 0),      
    scale=1,            
    color=color.white,   
    position=(-0.8, -0.48),            
    )
    singleplayer_button = Button(
        parent=camera.ui,
        font="PyCraft/Textures/Fonts/mc.ttf",
        text='Singleplayer',
        color=color.light_gray,
        scale=(0.5, 0.05),
        texture="PyCraft/Textures/buttontexture.png",
        highlight_color=color.rgb(0.745, 0.729, 1),
        position=(0, 0),  
        on_click = lambda: open_play_menu()
    )
    multiplayer_button = Button(
        parent=camera.ui,
        font="PyCraft/Textures/Fonts/mc.ttf",
        text='Multiplayer',
        color=color.light_gray,
        scale=(0.5, 0.05),
        texture="PyCraft/Textures/buttontexture.png",
        highlight_color=color.rgb(0.745, 0.729, 1),
        position=(0, -0.1),  
        on_click = lambda: open_multiplayer_menu()
    )
    menu_settings_button = Button(
        parent=camera.ui,
        font="PyCraft/Textures/Fonts/mc.ttf",
        text='Settings',
        color=color.light_gray,
        scale=(0.5, 0.05),
        texture="PyCraft/Textures/buttontexture.png",
        highlight_color=color.rgb(0.745, 0.729, 1),
        position=(0, -0.2),  
        on_click = lambda: open_menu_settings()
    )
    mod_menu_button = Button(
        parent=camera.ui,
        font="PyCraft/Textures/Fonts/mc.ttf",
        text='Mods',
        color=color.light_gray,
        scale=(0.225, 0.05),
        texture="PyCraft/Textures/buttontexture.png",
        highlight_color=color.rgb(0.745, 0.729, 1),
        position=(-0.1375, -0.3),  
        on_click = lambda: open_mod_menu()
    )
    menu_quit_button = Button(
        parent=camera.ui,
        font="PyCraft/Textures/Fonts/mc.ttf",
        text='Quit',
        color=color.light_gray,
        scale=(0.225, 0.05),
        texture="PyCraft/Textures/buttontexture.png",
        highlight_color=color.rgb(0.745, 0.729, 1),
        position=(0.1375, -0.3),  
        on_click = application.quit
    )

def destroy_main_menu():
    global title_screen_open
    destroy(titletext)
    destroy(singleplayer_button)
    destroy(multiplayer_button)
    destroy(menu_quit_button)
    destroy(mod_menu_button)
    destroy(tiptext)
    destroy(menu_settings_button)
    destroy(version_text)
    title_screen_open = False

def open_menu_settings():
    global menu_settings_open, comingsoon, returntomenu_button, settings_text, fullscreen_button
    destroy_main_menu()
    menu_settings_open = True
    settings_text = Entity(
    parent=camera.ui,
    model='quad',
    texture = 'PyCraft/Textures/settingslabel.png',
    scale=(0.75, 0.3),
    position=(0,0.25),
    visible=True  
    )
    fullscreen_button = Button(
        parent=camera.ui,
        font="PyCraft/Textures/Fonts/mc.ttf",
        text='Fullscreen: Disabled' if not window.fullscreen else 'Fullscreen: Enabled',
        color=color.light_gray,
        texture="PyCraft/Textures/buttontexture.png",
        highlight_color=color.rgb(0.745, 0.729, 1),
        scale=(0.5, 0.05),
        position=(0, 0), 
        on_click = lambda: toggle_fullscreen()
    )
    returntomenu_button = Button(
        parent=camera.ui,
        font="PyCraft/Textures/Fonts/mc.ttf",
        text='Back',
        color=color.light_gray,
        texture="PyCraft/Textures/buttontexture.png",
        highlight_color=color.rgb(0.745, 0.729, 1),
        scale=(0.5, 0.05),
        position=(0, -0.15, -1),  
        on_click = lambda: build_main_menu()
    )

def open_mod_menu():
    global mod_buttons, back_to_main_menu_button, mod_states, mod_labels
    destroy_main_menu()
    mod_labels = []
    mod_buttons = []
    mods_folder = f'{script_dir}/PyCraft/mods'
    mod_states = load_mod_states(mods_folder)

    for i, mod_name in enumerate(mod_states.keys()):
        mod_label = Text(
            parent = camera.ui,
            text = mod_name,
            position = (-0.1, 0.4 - i * 0.05),
            scale = 1.5,
            color = color.white
        )
        mod_labels.append(mod_label)

        mod_button = Button(
            parent = camera.ui,
            text = 'Enabled' if mod_states[mod_name] else 'Disabled',
            color=color.green if mod_states[mod_name] else color.red,
            scale = (0.15, 0.04),
            position = (0.22, 0.383 - i * 0.05),
            on_click = lambda m=mod_name: toggle_mod_state(m)
        )
        mod_buttons.append(mod_button)
    back_to_main_menu_button = Button(
        parent = camera.ui,
        text = 'Back',
        color = color.light_gray,
        texture="PyCraft/Textures/buttontexture.png",
        highlight_color=color.rgb(0.745, 0.729, 1),
        scale = (0.25, 0.04),
        position = (0, -0.4),
        on_click = lambda: back_to_main_menu()
    )

def toggle_mod_state(mod_name):
    global mod_states
    mods_folder = f'{script_dir}/PyCraft/mods'
    mod_states[mod_name] = not mod_states[mod_name]
    save_mod_states(mod_states, mods_folder)

    for i, name in enumerate(mod_states.keys()):
        if name == mod_name:
            mod_buttons[i].text = 'Enabled' if mod_states[mod_name] else 'Disabled'
            mod_buttons[i].color = color.green if mod_states[mod_name] else color.red
            break

def back_to_main_menu():
    for label in mod_labels:
        destroy(label)
    for button in mod_buttons:
        destroy(button)
    destroy(back_to_main_menu_button)
    destroy(mainbackground)
    build_main_menu()

def open_multiplayer_menu():
    global multiplayer_menu_open, comingsoon, returntomenu_button
    destroy_main_menu()
    multiplayer_menu_open = True
    comingsoon = Text(
    parent=camera.ui,
    font="PyCraft/Textures/Fonts/mc.ttf",
    text='Coming in the future!',   
    origin=(0, 0),      
    scale=2,            
    color=color.white,   
    position=(0, 0),            
    )
    returntomenu_button = Button(
        parent=camera.ui,
        font="PyCraft/Textures/Fonts/mc.ttf",
        text='Back',
        color=color.light_gray,
        texture="PyCraft/Textures/buttontexture.png",
        highlight_color=color.rgb(0.745, 0.729, 1),
        scale=(0.5, 0.05),
        position=(0, -0.15, -1),  
        on_click = lambda: build_main_menu()
    )


creative = False
def open_play_menu():
    global file_buttons, createworld_button, worldseedinput, play_menu_open, returntomenu_button, creative, mode_select_button, world_size, world_dimensions_button, world_depth_button, world_depth
    destroy_main_menu()
    play_menu_open = True
    folder_path = f'{script_dir}\\PyCraft\\Worlds'
    files = os.listdir(folder_path)
    scroll_container = Entity(parent=camera.ui, position = (0,0.3), scale=(1,1), visible=True)
    scroll_offset = 0
    file_buttons = []
    world_size = 10
    world_depth = 4
    for i, file_name in enumerate(files):
        filepath = f'{script_dir}/PyCraft/Worlds/{file_name}'
        worldfilebutton = Button(
            parent=scroll_container,
            font="PyCraft/Textures/Fonts/mc.ttf",
            text=file_name[:-5],
            color=color.light_gray,
            texture="PyCraft/Textures/buttontexture.png",
            highlight_color=color.rgb(0.745, 0.729, 1),
            scale=(0.25,0.05),
            position=(-0.25, (-i * 0.06) + 0.1, -2),
            on_click = lambda file_name=file_name: outdated_check(f'{script_dir}\\PyCraft\\Worlds\\{file_name}')
        )
        world_date = Text(
            parent=scroll_container,
            font="PyCraft/Textures/Fonts/mc.ttf",
            text= get_world_timesaved(filepath),
            scale=(1,1),
            position=(-0.05, (-i * 0.06) + 0.11, -2)
        )
        worlddeletebutton = Button(
            parent=scroll_container,
            font="PyCraft/Textures/Fonts/mc.ttf",
            text='Delete',
            color=color.rgb(1, 0.28, 0.28),
            texture="PyCraft/Textures/buttontexture.png",
            highlight_color=color.rgb(0.745, 0.729, 1),
            scale=(0.15,0.05),
            position=(0.25, (-i * 0.06) + 0.1, -2),
            on_click = lambda file_name=file_name: delete_world(f'{script_dir}/PyCraft/Worlds/{file_name}')
        )
        file_buttons.append(worldfilebutton)
        file_buttons.append(worlddeletebutton)
        file_buttons.append(world_date)
    worldselectbackground = Entity(
            parent=scroll_container,
            model='quad',
            color=color.rgba(0, 0, 0, 0.7),
            scale=(0.80,0.5),
            position=(0, -0.1, -1.8)
        )
    file_buttons.append(worldselectbackground)
    createworld_button = Button(
        parent=camera.ui,
        font="PyCraft/Textures/Fonts/mc.ttf",
        text='Create World',
        color=color.light_gray,
        texture="PyCraft/Textures/buttontexture.png",
        highlight_color=color.rgb(0.745, 0.729, 1),
        scale=(0.25, 0.04),
        position=(0, -0.15, -1),  
        on_click = lambda: generate_world(worldseedinput.text, int(world_size/2), world_depth)
    )
    mode_select_button = Button(
        parent=camera.ui,
        font="PyCraft/Textures/Fonts/mc.ttf",
        text='Mode: Creative' if creative else 'Mode: Survival',
        color=color.light_gray,
        texture="PyCraft/Textures/buttontexture.png",
        highlight_color=color.rgb(0.745, 0.729, 1),
        scale=(0.2, 0.04),
        position=(0.275, -0.15, -1),  
        on_click = lambda: toggle_mode()
    )
    world_dimensions_button = Button(
        parent=camera.ui,
        font="PyCraft/Textures/Fonts/mc.ttf",
        text='World Size: 10x10',
        color=color.light_gray,
        texture="PyCraft/Textures/buttontexture.png",
        highlight_color=color.rgb(0.745, 0.729, 1),
        scale=(0.23, 0.04),
        position=(0.275, -0.2, -1),  
        on_click = lambda: toggle_world_size()
    )
    world_depth_button = Button(
        parent=camera.ui,
        font="PyCraft/Textures/Fonts/mc.ttf",
        text='World Depth: 4',
        color=color.light_gray,
        texture="PyCraft/Textures/buttontexture.png",
        highlight_color=color.rgb(0.745, 0.729, 1),
        scale=(0.23, 0.04),
        position=(0.275, -0.25, -1),  
        on_click = lambda: toggle_world_depth()
    )
    worldseedinput = InputField(
        default_value='Seed',
        scale=(0.2, 0.05), 
        position=(0, -0.2, -1)
        )
    def limit_text():
        if len(worldseedinput.text) > 5:
            worldseedinput.text = worldseedinput.text[:7]
    worldseedinput.on_value_changed = limit_text
    returntomenu_button = Button(
        parent=camera.ui,
        font="PyCraft/Textures/Fonts/mc.ttf",
        text='Back',
        color=color.light_gray,
        texture="PyCraft/Textures/buttontexture.png",
        highlight_color=color.rgb(0.745, 0.729, 1),
        scale=(0.25, 0.04),
        position=(-0.3, -0.15, -1),  
        on_click = lambda: build_main_menu()
    )

def toggle_mode():
    global creative
    creative = not creative
    mode_select_button.text = 'Mode: Creative' if creative else 'Mode: Survival'

def toggle_world_size():
    global world_dimensions_button, world_size
    if world_dimensions_button.text == 'World Size: 10x10':
        world_size = 12
        world_dimensions_button.text = 'World Size: 12x12'
    elif world_dimensions_button.text == 'World Size: 12x12':
        world_size = 16
        world_dimensions_button.text = 'World Size: 16x16'
    elif world_dimensions_button.text == 'World Size: 16x16':
        world_size = 20
        world_dimensions_button.text = 'World Size: 20x20'
    elif world_dimensions_button.text == 'World Size: 20x20':
        world_size = 8
        world_dimensions_button.text = 'World Size: 8x8'
    else:
        world_size = 10
        world_dimensions_button.text = 'World Size: 10x10'
def toggle_world_depth():
    global world_depth_button, world_depth
    if world_depth_button.text == 'World Depth: 4':
        world_depth = 6
        world_depth_button.text = 'World Depth: 6'
    elif world_depth_button.text == 'World Depth: 6':
        world_depth = 8
        world_depth_button.text = 'World Depth: 8'
    elif world_depth_button.text == 'World Depth: 8':
        world_depth = 10
        world_depth_button.text = 'World Depth: 10'
    elif world_depth_button.text == 'World Depth: 10':
        world_depth = 4
        world_depth_button.text = 'World Depth: 4'
def destroy_play_menu():
    global file_buttons, main_menu_open
    destroy(mainbackground)
    destroy(createworld_button)
    destroy(worldseedinput)
    destroy(returntomenu_button)
    destroy(mode_select_button)
    destroy(world_depth_button)
    destroy(world_dimensions_button)
    for i in file_buttons:
        destroy(i)
    file_buttons = []
    play_menu_open = False
    main_menu_open = False
def delete_world(filepath):
    global file_buttons
    os.remove(filepath)
    for i in file_buttons:
        destroy(i)
    destroy(createworld_button)
    destroy(worldseedinput)
    destroy(returntomenu_button)
    destroy(mode_select_button)
    destroy(world_dimensions_button)
    destroy(world_depth_button)
    
    open_play_menu()
def outdated_popup(filename, worldversion):
    global file_buttons, outdated_version_text, goback_button, continue_button, more_info_text
    for i in file_buttons:
        destroy(i)
    
    destroy(createworld_button)
    destroy(worldseedinput)
    destroy(returntomenu_button)
    destroy(mode_select_button)
    destroy(world_dimensions_button)
    destroy(world_depth_button)
    outdated_version_text = Text(
    parent=camera.ui,
    font="PyCraft/Textures/Fonts/mc.ttf",
    text=f'This world was created on an older version of PyCraft. Continue?',   
    origin=(0, 0),      
    scale=1.3,            
    color=color.white,   
    position=(0, 0.1),            
    )
    more_info_text = Text(
    parent=camera.ui,
    font="PyCraft/Textures/Fonts/mc.ttf",
    text=f'(World Version: {worldversion}, Game Version: {game_version})',   
    origin=(0, 0),      
    scale=0.8,            
    color=color.white,   
    position=(0, 0.07),            
    )
    goback_button = Button(
        parent=camera.ui,
        font="PyCraft/Textures/Fonts/mc.ttf",
        text='Back',
        color=color.light_gray,
        scale=(0.225, 0.05),
        texture="PyCraft/Textures/buttontexture.png",
        highlight_color=color.rgb(0.745, 0.729, 1),
        position=(-0.1375, 0),  
        on_click = lambda: destroy_outdated()
    )
    continue_button = Button(
        parent=camera.ui,
        font="PyCraft/Textures/Fonts/mc.ttf",
        text='Continue',
        color=color.light_gray,
        scale=(0.225, 0.05),
        texture="PyCraft/Textures/buttontexture.png",
        highlight_color=color.rgb(0.745, 0.729, 1),
        position=(0.1375, 0),  
        on_click = lambda: destroy_outdated(True, filename)
    )
def destroy_outdated(continued=False, filename=None):
    destroy(continue_button)
    destroy(goback_button)
    destroy(outdated_version_text)
    destroy(more_info_text)
    if continued:
        load_world(filename, True)
    else:
        open_play_menu()
def toggle_inventory():
    global inventory_opened
    if creative:
        if inventory_opened:
            close_inventory()
        else:
            open_inventory(currentpagedata['page'], currentpagedata['pagenumber'], currentpagedata['pagelabel'])
    else:
        if inventory_opened:
            close_survival_inventory()
        else:
            open_survival_inventory()

def open_survival_inventory():
    global inventory_opened, survival_inventory_panel, cs1, cs2, cs3, cs4, result_slot, crafting_slots
    inventory_opened = True
    mouse.locked = False
    mouse.visible = True

    survival_inventory_panel = Entity(
        parent=camera.ui,
        model='quad',
        texture = 'PyCraft/Textures/survivalinventory.png',
        scale=(0.5,0.45),
        color=color.hsv(0,0,0.9),
        position = (0,0,1)
    )
    cs1 = Button( 
                    color=color.hsv(0, 0, .9),
                    texture=None,
                    parent=survival_inventory_panel,
                    position=(0.1, 0.344, -1), 
                    scale=(0.09, 0.1),
                    hand_color = color.hsv(0, 0, .9),
                    visible = True
                    )
    cs2 = Button( 
                    color=color.hsv(0, 0, .9),
                    texture=None,
                    parent=survival_inventory_panel,
                    position=(0.2035, 0.344, -1), 
                    scale=(0.09, 0.1),
                    hand_color = color.hsv(0, 0, .9),
                    visible = True
                    )
    cs3 = Button( 
                    color=color.hsv(0, 0, .9),
                    texture=None,
                    parent=survival_inventory_panel,
                    position=(0.1, 0.238, -1), 
                    scale=(0.09, 0.1),
                    hand_color = color.hsv(0, 0, .9),
                    visible = True
                    )
    cs4 = Button( 
                    color=color.hsv(0, 0, .9),
                    texture=None,
                    parent=survival_inventory_panel,
                    position=(0.2035, 0.238, -1), 
                    scale=(0.09, 0.1),
                    hand_color = color.hsv(0, 0, .9),
                    visible = True
                    ) 
    result_slot = Button( 
                    color=color.hsv(0, 0, .9),
                    texture=None,
                    parent=survival_inventory_panel,
                    position=(0.42, 0.283, -1), 
                    scale=(0.09, 0.1),
                    hand_color = color.hsv(0, 0, .9),
                    visible = True
                    ) 
    
def close_survival_inventory():
    global inventory_opened, holding_block
    inventory_opened = False
    mouse.locked = True
    mouse.visible = False
    if holding_block:
        holding_block = False
        destroy(block_drag)
        destroy(block_drag_amount)
    destroy(survival_inventory_panel)




def open_inventory(pg, pgn, pgl):
    global inventory_opened, inventory_panel, block_buttons, page_number, next_arrow, previous_arrow, page_label
    inventory_opened = True
    mouse.locked = False
    mouse.visible = True


    inventory_panel = Entity(
        parent=camera.ui,
        model='quad',
        texture = 'PyCraft/Textures/inventory.png',
        scale=(0.4,0.25),
        color=color.hsv(0,0,0.9),
        position = (0,0,1)
    )

    block_buttons = []
    num_columns = 9
    num_rows = math.ceil(len(pg) / num_columns)
    button_scale = (0.1,0.18)
    spacing = 0.108

    row_y_positions = [0.265, 0.175, 0.085]

    for index,block in enumerate(pg):
        col = index % num_columns
        row = index // num_columns

        position = Vec3(
            -0.43 + col * spacing,
            row_y_positions[row] - row * spacing,
            -1
        )

        block_button = Button(
            parent=inventory_panel,
            model='quad',
            texture=block['texture'],
            scale=button_scale,
            position=position,
            color=color.white,
            on_click=lambda b=block: hold_block(b)
        )
        block_buttons.append(block_button)

    page_number = Text(
    parent=inventory_panel,
    font="PyCraft/Textures/Fonts/mc.ttf",  
    text=pgn,   
    origin=(0, 0),      
    scale=(3,5),            
    color=color.black,   
    position=(0, -0.39, -1),            
    )
    page_label = Text(
    parent=inventory_panel,
    font="PyCraft/Textures/Fonts/mc.ttf",  
    text=pgl,
    origin=(0, 0),      
    scale=(2,4),            
    color=color.black,   
    position=(0.3, 0.42, -1),            
    )
    next_arrow = Button(
            parent=inventory_panel,
            texture='PyCraft/Textures/nextarrow.png',
            color=color.gray,
            scale=(0.09, 0.15),
            position=(0.429, -0.375, -1),
            on_click = lambda: next_inventory_page()
        )
    previous_arrow = Button(
            parent=inventory_panel,
            texture='PyCraft/Textures/backarrow.png',
            color=color.gray,
            scale=(0.09, 0.15),
            position=(-0.429, -0.375, -1),
            on_click = lambda: previous_inventory_page()
        )
def next_inventory_page():
    global page_number, currentpagedata, page_label
    if int(page_number.text) + 1 in pages:
        clear_inventory_page()
        build_new_page(pages.get(int(page_number.text) + 1))
        currentpagedata['page'] = pages.get(int(page_number.text) + 1)
        page_number.text = str(int(page_number.text) + 1)
        page_label.text = pagelabels[page_number.text]
        currentpagedata['pagenumber'] = page_number.text
        currentpagedata['pagelabel'] = pagelabels[page_number.text]
def previous_inventory_page():
    global page_number, currentpagedata, page_label
    if int(page_number.text) - 1 in pages:
        clear_inventory_page()
        build_new_page(pages.get(int(page_number.text) - 1))
        currentpagedata['page'] = pages.get(int(page_number.text) - 1)
        page_number.text = str(int(page_number.text) - 1)
        page_label.text = pagelabels[page_number.text]
        currentpagedata['pagenumber'] = page_number.text
        currentpagedata['pagelabel'] = pagelabels[page_number.text]
def hold_block(block):
    global selectedvoxel,selected,hand,defrot,holding_block,block_drag,block_held, block_drag_amount
    if holding_block:
        destroy(block_drag)
        destroy(block_drag_amount)
    holding_block = True
    block_drag = Entity(
            parent=camera.ui,
            model='quad',
            texture=block['texture'],
            blockcolor = block['color'],
            amount = 1,
            scale=(0.05,0.05),
            color=color.white,
        )
    block_drag_amount = Text(
        parent=camera.ui,
        font="PyCraft/Textures/Fonts/mc.ttf",
        text=str(block_drag.amount),
        origin=(0, 0),
        scale=1,
        color=color.white,
        )
    block_held = block['voxel_class']
def equip_block(slot):
    global selectedvoxel,selected,hand,defrot,holding_block,block_drag,block_held,slot1,slot2,slot3,slot4,slot5,slot6,slot7,slot8,slot9, replacingslot
    if holding_block and not replacingslot:
        slot.texture=block_drag.texture
        if slot.equipped == block_held:
            if slot.amount < 64:
                slot.amount += 1
        else:
            slot.amount = 1
        slot.equipped=block_held
        slot.hand_color=block_drag.blockcolor
        slot.visible = True

        destroy(block_drag)
        destroy(block_drag_amount)
        holding_block = False
        if slot == slotselected:
            update_equipped_slot(slot)
    if holding_block and replacingslot:
        replacingslot.texture = slot.texture
        replacingslot.equipped = slot.equipped
        replacingslot.hand_color = slot.hand_color
        replacingslot.visible = slot.visible
        replacingslot.amount = slot.amount
        slot.texture=block_drag.texture
        slot.equipped=block_held
        slot.hand_color=block_drag.blockcolor
        slot.amount = block_drag.amount if hasattr(block_drag, 'amount') else 1
        slot.visible = True
        destroy(block_drag)
        destroy(block_drag_amount)
        if slot == slotselected or replacingslot == slotselected:
            update_equipped_slot(slotselected)
        replacingslot = False
        holding_block = False

def swap_block(slot):
    global selectedvoxel,selected,hand,defrot,holding_block,block_drag,block_held,slot1,slot2,slot3,slot4,slot5,slot6,slot7,slot8,slot9, replacingslot, block_drag_amount
    if slot.equipped:
        block_drag = Entity(
            parent=camera.ui,
            model='quad',
            texture=slot.texture,
            blockcolor = slot.hand_color,
            scale=(0.05,0.05),
            amount=slot.amount,
            color=color.white,
        )
        block_drag_amount = Text(
        parent=camera.ui,
        font="PyCraft/Textures/Fonts/mc.ttf",
        text=str(block_drag.amount),
        origin=(0, 0),
        scale=1,
        color=color.white,
        )
        slot.amount = 0
        replacingslot = slot
        slot.visible = False
        block_held = slot.equipped
        holding_block = True
        slot.equipped = None
        if slot == slotselected:
            update_equipped_slot(slot)
def close_inventory():
    global inventory_opened, inventory_panel, block_buttons, holding_block
    inventory_opened = False
    mouse.locked = True
    mouse.visible = False
    if holding_block:
        holding_block = False
        destroy(block_drag)
        destroy(block_drag_amount)
    destroy(inventory_panel)
    for btn in block_buttons:
        destroy(btn)
    block_buttons = []

def clear_inventory_page():
    global block_buttons
    for btn in block_buttons:
        destroy(btn)
    block_buttons = []
def build_new_page(pg):
    global block_buttons
    block_buttons = []
    num_columns = 9
    num_rows = math.ceil(len(pg) / num_columns)
    button_scale = (0.1,0.18)
    spacing = 0.108

    row_y_positions = [0.265, 0.175, 0.085]

    for index,block in enumerate(pg):
        col = index % num_columns
        row = index // num_columns

        position = Vec3(
            -0.43 + col * spacing,
            row_y_positions[row] - row * spacing,
            -1
        )

        block_button = Button(
            parent=inventory_panel,
            model='quad',
            texture=block['texture'],
            scale=button_scale,
            position=position,
            color=color.white,
            on_click=lambda b=block: hold_block(b)
        )
        block_buttons.append(block_button)
def update_equipped_slot(s):
    global selectedvoxel, selector, hand, defrot, selected, slotselected
    if s.equipped and s.equipped != 'gun':
        selectedvoxel = s.equipped
        block_texture = selectedvoxel.block_texture
        block_model = selectedvoxel.block_model
        selected = 'block'
    elif s.equipped == 'gun':
        selectedvoxel = None
        selected = 'ak'
    else:
        selectedvoxel = None
        block_texture = None
        selected = 'openhand'
    slotselected = s
    if selectedvoxel:
        update_hand_properties(hand, model=block_model, texture=block_texture, color=s.hand_color, scale=(0.5,0.5,0.5) if block_model == 'cube' else selectedvoxel.hand_scale if hasattr(selectedvoxel, 'hand_scale') else (0.5, 0.5, 0.5), origin_y=selectedvoxel.yorg if hasattr(selectedvoxel, 'yorg') else 0 if block_model == 'cube' else 1, rotation=selectedvoxel.defaultrotation if hasattr(selectedvoxel, 'defaultrotation') else (0,0,0), position=(0,0,0))
    elif not selectedvoxel and selected == 'ak':
        update_hand_properties(hand, model="PyCraft/Textures/ak.obj", scale=(0.5,0.5,0.5), position=(0,0,0), rotation=(180,0,180))
    else:
        update_hand_properties(hand, model='cube', color=color.hsv(30, 0.4, 0.8), scale=(0.2,0.7,0.2), rotation=(45,0,0), position=(0,0,0), texture=None)
    defrot = hand.rotation
    destroy(selector)
    selector = Button( 
        color=color.rgb(0.2, 0.2, 0.2), 
        position=(s.position.x, s.position.y, 0), 
        scale=(0.045, 0.045),
        visible=True
        )
    
def update_hand_properties(hand, model=None, texture=None, color=None, scale=None, rotation=None, position=None, origin_y=None):
    """
    Updates the properties of the hand entity without destroying and recreating it.

    Args:
        hand (Entity): The hand entity to update.
        model (str, optional): The model of the hand.
        texture (str, optional): The texture of the hand.
        color (Color, optional): The color of the hand.
        scale (tuple, optional): The scale of the hand.
        rotation (tuple, optional): The rotation of the hand.
        position (tuple, optional): The position of the hand.
    """
    if model:
        hand.model = model
    hand.texture = texture
    if color:
        hand.color = color
    if scale:
        hand.scale = scale
    if rotation:
        hand.rotation = rotation
    if position:
        hand.position = position
    if origin_y:
        hand.origin_y = origin_y
    invoke(reset_hand_position, delay=0.4)
def reset_hand_position():
    hand.rotation = defrot
def build_death_screen():
    global death_background, death_label, respawn_button, death_quit_button
    mouse.locked = False
    death_background = Entity(
    parent=camera.ui,
    model='quad',
    scale=(2, 2, 1),
    color=color.rgba(0,0,0, 0.5),
    position=(0,0,-3),  
    visible=True  
    )
    death_label = Text(
        parent=death_background,
        font="PyCraft/Textures/Fonts/mc.ttf",  
        text='You Died!',   
        origin=(0, 0),      
        scale=2,            
        color=color.white,   
        position=(0, 0.1),            
    ) 
    respawn_button = Button(
        parent=death_background,
        font="PyCraft/Textures/Fonts/mc.ttf",
        text='Respawn',
        color=color.light_gray,
        texture="PyCraft/Textures/buttontexture.png",
        highlight_color=color.rgb(0.745, 0.729, 1),
        scale=(0.15, 0.02),  # Size of the button
        position=(0, 0),  # Position on the screen
        on_click = lambda: destroy_death_screen()
    )
    death_quit_button = Button(
        parent=death_background,
        font="PyCraft/Textures/Fonts/mc.ttf",
        text='Quit',
        color=color.light_gray,
        texture="PyCraft/Textures/buttontexture.png",
        highlight_color=color.rgb(0.745, 0.729, 1),
        scale=(0.15, 0.02),  # Size of the button
        position=(0, -0.05),  # Position on the screen
        on_click = application.quit
    )

def destroy_death_screen():
    global last_y_position, health
    mouse.locked = True
    destroy(death_label)
    destroy(respawn_button)
    destroy(death_quit_button)
    destroy(death_background)
    for heart in hearts:
        heart.texture = 'PyCraft/Textures/fullheart'
    for slot in slots:
        slot.equipped = None
        slot.visible = False
    health = 100
    last_y_position = None
    player.position = Vec3(*[0,0,0])
    update_equipped_slot(slot1)

mining_animation_running = False
mining_speed = 0.1
original_hand_rotation = (90,0,0)
swing_angle = 45
swing_sequence = None



build_main_menu()
defrot = (0,0,0)
steve_model = Entity(
                        parent=scene,
                        position=(500,500,500),
                        model='PyCraft/Textures/stevemodel.glb',
                        scale=0.05,
                        origin_y=0.5,
                        collider=None,
                    )

selectedvoxel = Voxel
selected = ''
def input(key):
    global selectedvoxel, selector, hand, defrot, selected, world_data, blockcopied, slotselected, currently_breaking_block, block_break_start_time, mouse_held
    if key == 'escape' and not main_menu_open and not inventory_opened:
            toggle_mouse_lock()
    if key == 'e' and not main_menu_open and not pause_menu_open:
        toggle_inventory()
        return
    if mouse.locked:
        if creative:
            if key == 'left mouse down':

                if selected == 'ak':
                        hand.animate_rotation((160, 0, 180), duration=0.1, curve=curve.in_out_expo)
                                
                        invoke(hand.animate_rotation, defrot, duration=0.1, curve=curve.in_out_expo, delay=0.1)
                else:
                    hand.rotation = defrot
                    hand.animate_rotation(selectedvoxel.animationrotation if hasattr(selectedvoxel, 'animationrotation') else (110, -30, 0), duration=0.2, curve=curve.in_out_quad)
                    invoke(hand.animate_rotation, defrot, duration=0.2, curve=curve.in_out_quad, delay=0.2)
                    if mouse.hovered_entity and mouse.hovered_entity != player:
                        if hasattr(mouse.hovered_entity, 'destroyable') and not mouse.hovered_entity.destroyable:
                            pass
                        else:
                            position = mouse.hovered_entity.position
                            destroy(mouse.hovered_entity)
                            block_class = type(mouse.hovered_entity)
                            texture = mouse.hovered_entity.texture
                            if not 'Fire' in f"{block_class}":
                                DroppedBlock(position=position, texture=texture, block_class=block_class)
                                
                            for block in world_data:
                                if block['position'] == [position.x, position.y, position.z]:
                                    world_data.remove(block)
                                    break
                            
        else:
            if key == 'left mouse down':
                if mouse.hovered_entity and hasattr(mouse.hovered_entity, 'isblock') and mouse.hovered_entity.isblock:
                    if hasattr(mouse.hovered_entity, 'destroyable') and mouse.hovered_entity.destroyable == False:
                        return
                    currently_breaking_block = mouse.hovered_entity
                    currently_breaking_block.original_texture = currently_breaking_block.texture
                    block_break_start_time = time.time()
                    mouse_held = True
                    global overlay_entity, mining_animation_running

                    overlay_entity = Entity(
                        parent=scene,
                        position=(currently_breaking_block.position.x, currently_breaking_block.position.y + 0.001, currently_breaking_block.position.z),
                        model='cube',
                        scale=currently_breaking_block.scale * 1.005 if f'{currently_breaking_block.model}'[-4:] == 'cube' else (currently_breaking_block.scale * 2) * 1.005,
                        rotation=currently_breaking_block.rotation,
                        texture=block_breaking_stages[0],
                        origin_y=0.5,
                        color=color.white,
                        collider=None,
                        always_on_top=False,
                        z=currently_breaking_block.z - 0.001,
                        transparent=True
                    )
            if key == 'left mouse up' and currently_breaking_block:
                currently_breaking_block.texture = currently_breaking_block.original_texture
                currently_breaking_block = None
                block_break_start_time = None
                mouse_held = False
                if overlay_entity:
                    destroy(overlay_entity)
                    overlay_entity = None

        
        if key == 'middle mouse down' and creative and mouse.hovered_entity and not hasattr(mouse.hovered_entity, 'wall'):
            global blockcopied
            voxcolor = mouse.hovered_entity.color
            blockcopied = mouse.hovered_entity.__class__.__name__
            blocktexture =mouse.hovered_entity.texture
            blockicon = mouse.hovered_entity.block_icon
            blockmodel = mouse.hovered_entity.block_model
            
            slotselected.hand_color = voxcolor
            slotselected.texture = blockicon
            slotselected.equipped = block_class_mapping[mouse.hovered_entity.__class__.__name__]
            slotselected.visible = True
            selectedvoxel = block_class_mapping[mouse.hovered_entity.__class__.__name__]
            selected = 'voxel'
            defrot = (0,0,0)
            update_hand_properties(hand, model=blockmodel, texture=blocktexture, color=color.rgb(voxcolor.r, voxcolor.g, voxcolor.b), scale=(0.5,0.5,0.5) if blockmodel == 'cube' else (0.25, 0.25, 0.25), origin_y=0 if blockmodel == 'cube' else 1, rotation=(0,0,0), position=(0,0,0))
        if key == 'right mouse down':
            hit_info = raycast(camera.world_position, camera.forward, distance=7, ignore=(player,))
            if hit_info.hit and selectedvoxel and not hasattr(hit_info.entity, 'wall') and not hasattr(selectedvoxel, 'istool'):
                new_position = hit_info.entity.position + hit_info.normal
                if selectedvoxel == FlintAndSteel:
                    Fire(position=new_position)
                selectedvoxel(position=new_position)
                block_type = selectedvoxel.__name__
                if block_type == 'CopiedVoxel':
                    block_type = blockcopied
                world_data.append({'position': [new_position.x, new_position.y, new_position.z], 'block_type': block_type})
                if not creative:
                    slotselected.amount -= 1
                hand.rotation = defrot

                hand.animate_rotation((110, -30, 0), duration=0.2, curve=curve.in_out_quad)
                        
                invoke(hand.animate_rotation, defrot, duration=0.2, curve=curve.in_out_quad, delay=0.2)
            elif hit_info.hit and selectedvoxel and not hasattr(hit_info.entity, 'wall') and hasattr(selectedvoxel, 'istool'):
                if selectedvoxel == FlintAndSteel:
                    Fire(position=hit_info.entity.position + hit_info.normal)
        if key == 'f3':
            global debugOpen, worldversion, seedlabel, modslist, coordslabel
            loaded_mods = [i for i in mod_states if mod_states[i]]
            if debugOpen:
                destroy(worldversion)
                destroy(seedlabel)
                destroy(modslist)
                destroy(coordslabel)
                debugOpen = False
            else:
                worldversion = Text(
                parent=camera.ui,
                font="PyCraft/Textures/Fonts/mc.ttf",  
                text=f'World Version: {worldver}',   
                origin=(0, 0),      
                scale=1,            
                color=color.white,   
                position=(-0.75, 0.47),            
                )
                seedlabel = Text(
                parent=camera.ui,
                font="PyCraft/Textures/Fonts/mc.ttf",  
                text=f'Seed: {seedvalue}',   
                origin=(0, 0),      
                scale=1,            
                color=color.white,   
                position=(-0.75, 0.43),            
                )
                coordslabel = Text(
                parent=camera.ui,
                font="PyCraft/Textures/Fonts/mc.ttf",  
                text=f'Coordinates: X:{int(player.position.x)} Y:{int(player.position.y)} Z:{int(player.position.z)}',   
                origin=(0, 0),      
                scale=1,            
                color=color.white,   
                position=(-0.72, 0.35),            
                )
                modslist = Text(
                parent=camera.ui,
                font="PyCraft/Textures/Fonts/mc.ttf",  
                text=f'Mods: {loaded_mods}',   
                origin=(0, 0),      
                scale=1,            
                color=color.white,   
                position=(-0.5, 0.39),            
                )
                debugOpen = True
        if key == 'f1':
            global cinematicMode
            if not cinematicMode:
                cinematicMode = True
                hotbar.visible = False
                selector.visible = False
                for i in slots:
                    i.visible = False
                player.cursor.visible = False
                hand.visible = False
            else:
                cinematicMode = False
                hotbar.visible = True
                selector.visible = True
                for i in slots:
                    i.visible = True
                player.cursor.visible = True
                hand.visible = True
                
        if key == '1':
            if slot1.equipped and slot1.equipped != 'gun':
                selectedvoxel = slot1.equipped
                block_texture = selectedvoxel.block_texture
                block_model = selectedvoxel.block_model
                selected = 'block'
            elif slot1.equipped == 'gun':
                selectedvoxel = None
                selected = 'ak'
            else:
                selectedvoxel = None
                block_texture = None
                selected = 'openhand'
            slotselected = slot1
            if selectedvoxel:
                update_hand_properties(hand, model=block_model, texture=block_texture, color=slotselected.hand_color, scale=(0.5,0.5,0.5) if block_model == 'cube' else selectedvoxel.hand_scale if hasattr(selectedvoxel, 'hand_scale') else (0.5, 0.5, 0.5), origin_y=selectedvoxel.yorg if hasattr(selectedvoxel, 'yorg') else 0 if block_model == 'cube' else 1, rotation=selectedvoxel.defaultrotation if hasattr(selectedvoxel, 'defaultrotation') else (0,0,0), position=(0,0,0))
            elif not selectedvoxel and selected == 'ak':
                update_hand_properties(hand, model="PyCraft/Textures/ak.obj", scale=(0.5,0.5,0.5), position=(0,0,0), rotation=(180,0,180))
            else:
                update_hand_properties(hand, model='cube', color=color.hsv(30, 0.4, 0.8), scale=(0.2,0.7,0.2), rotation=(45,0,0), position=(0,0,0))
            defrot = hand.rotation
            destroy(selector)
            selector = Button( 
                color=color.rgb(0.2, 0.2, 0.2), 
                position=(slot1.position.x, slot1.position.y, 0), 
                scale=(0.045, 0.045),
                visible=True
                )
        if key == '2':
            if slot2.equipped and slot2.equipped != 'gun':
                selectedvoxel = slot2.equipped
                block_texture = selectedvoxel.block_texture
                block_model = selectedvoxel.block_model
                selected = 'block'
            elif slot2.equipped == 'gun':
                selectedvoxel = None
                selected = 'ak'
            else:
                selectedvoxel = None
                block_texture = None
                selected = 'openhand'
            slotselected = slot2
            if selectedvoxel:
                update_hand_properties(hand, model=block_model, texture=block_texture, color=slotselected.hand_color, scale=(0.5,0.5,0.5) if block_model == 'cube' else selectedvoxel.hand_scale if hasattr(selectedvoxel, 'hand_scale') else (0.5, 0.5, 0.5), origin_y=selectedvoxel.yorg if hasattr(selectedvoxel, 'yorg') else 0 if block_model == 'cube' else 1, rotation=selectedvoxel.defaultrotation if hasattr(selectedvoxel, 'defaultrotation') else (0,0,0), position=(0,0,0))
            elif not selectedvoxel and selected == 'ak':
                update_hand_properties(hand, model="PyCraft/Textures/ak.obj", scale=(0.5,0.5,0.5), position=(0,0,0), rotation=(180,0,180))
            else:
                update_hand_properties(hand, model='cube', color=color.hsv(30, 0.4, 0.8), scale=(0.2,0.7,0.2), rotation=(45,0,0), position=(0,0,0))
            defrot = hand.rotation
            destroy(selector)
            selector = Button( 
                color=color.rgb(0.2, 0.2, 0.2), 
                position=(slot2.position.x, slot2.position.y, 0), 
                scale=(0.045, 0.045),
                visible=True
                )
        if key == '3':
            if slot3.equipped and slot3.equipped != 'gun':
                selectedvoxel = slot3.equipped
                block_texture = selectedvoxel.block_texture
                block_model = selectedvoxel.block_model
                selected = 'block'
            elif slot3.equipped == 'gun':
                selectedvoxel = None
                selected = 'ak'
            else:
                selectedvoxel = None
                block_texture = None
                selected = 'openhand'
            slotselected = slot3
            if selectedvoxel:
                update_hand_properties(hand, model=block_model, texture=block_texture, color=slotselected.hand_color, scale=(0.5,0.5,0.5) if block_model == 'cube' else selectedvoxel.hand_scale if hasattr(selectedvoxel, 'hand_scale') else (0.5, 0.5, 0.5), origin_y=selectedvoxel.yorg if hasattr(selectedvoxel, 'yorg') else 0 if block_model == 'cube' else 1, rotation=selectedvoxel.defaultrotation if hasattr(selectedvoxel, 'defaultrotation') else (0,0,0), position=(0,0,0))
            elif not selectedvoxel and selected == 'ak':
                update_hand_properties(hand, model="PyCraft/Textures/ak.obj", scale=(0.5,0.5,0.5), position=(0,0,0), rotation=(180,0,180))
            else:
                update_hand_properties(hand, model='cube', color=color.hsv(30, 0.4, 0.8), scale=(0.2,0.7,0.2), rotation=(45,0,0), position=(0,0,0))
            destroy(selector)
            defrot = hand.rotation
            selector = Button( 
                color=color.rgb(0.2, 0.2, 0.2), 
                position=(slot3.position.x, slot3.position.y, 0), 
                scale=(0.045, 0.045),
                visible=True
                )
        if key == '4':
            if slot4.equipped and slot4.equipped != 'gun':
                selectedvoxel = slot4.equipped
                block_texture = selectedvoxel.block_texture
                block_model = selectedvoxel.block_model
                selected = 'block'
            elif slot4.equipped == 'gun':
                selectedvoxel = None
                selected = 'ak'
            else:
                selectedvoxel = None
                block_texture = None
                selected = 'openhand'
            destroy(selector)
            slotselected = slot4
            if selectedvoxel:
                update_hand_properties(hand, model=block_model, texture=block_texture, color=slotselected.hand_color, scale=(0.5,0.5,0.5) if block_model == 'cube' else selectedvoxel.hand_scale if hasattr(selectedvoxel, 'hand_scale') else (0.5, 0.5, 0.5), origin_y=selectedvoxel.yorg if hasattr(selectedvoxel, 'yorg') else 0 if block_model == 'cube' else 1, rotation=selectedvoxel.defaultrotation if hasattr(selectedvoxel, 'defaultrotation') else (0,0,0), position=(0,0,0))
            elif not selectedvoxel and selected == 'ak':
                update_hand_properties(hand, model="PyCraft/Textures/ak.obj", scale=(0.5,0.5,0.5), position=(0,0,0), rotation=(180,0,180))
            else:
                update_hand_properties(hand, model='cube', color=color.hsv(30, 0.4, 0.8), scale=(0.2,0.7,0.2), rotation=(45,0,0), position=(0,0,0))
            defrot = hand.rotation
            selector = Button( 
                color=color.rgb(0.2, 0.2, 0.2), 
                position=(slot4.position.x, slot4.position.y, 0), 
                scale=(0.045, 0.045),
                visible=True
                )
        if key == '5':
            if slot5.equipped and slot5.equipped != 'gun':
                selectedvoxel = slot5.equipped
                block_texture = selectedvoxel.block_texture
                block_model = selectedvoxel.block_model
                selected = 'block'
            elif slot5.equipped == 'gun':
                selectedvoxel = None
                selected = 'ak'
            else:
                selectedvoxel = None
                block_texture = None
                selected = 'openhand'
            slotselected = slot5
            if selectedvoxel:
                update_hand_properties(hand, model=block_model, texture=block_texture, color=slotselected.hand_color, scale=(0.5,0.5,0.5) if block_model == 'cube' else selectedvoxel.hand_scale if hasattr(selectedvoxel, 'hand_scale') else (0.5, 0.5, 0.5), origin_y=selectedvoxel.yorg if hasattr(selectedvoxel, 'yorg') else 0 if block_model == 'cube' else 1, rotation=selectedvoxel.defaultrotation if hasattr(selectedvoxel, 'defaultrotation') else (0,0,0), position=(0,0,0))
            elif not selectedvoxel and selected == 'ak':
                update_hand_properties(hand, model="PyCraft/Textures/ak.obj", scale=(0.5,0.5,0.5), position=(0,0,0), rotation=(180,0,180))
            else:
                update_hand_properties(hand, model='cube', color=color.hsv(30, 0.4, 0.8), scale=(0.2,0.7,0.2), rotation=(45,0,0), position=(0,0,0))
            defrot = hand.rotation
            destroy(selector)
            selector = Button( 
                color=color.rgb(0.2, 0.2, 0.2), 
                position=(slot5.position.x, slot5.position.y, 0), 
                scale=(0.045, 0.045),
                visible=True
                )
        if key == '6':
            if slot6.equipped and slot6.equipped != 'gun':
                selectedvoxel = slot6.equipped
                block_texture = selectedvoxel.block_texture
                block_model = selectedvoxel.block_model
                selected = 'block'
            elif slot6.equipped == 'gun':
                selectedvoxel = None
                selected = 'ak'
            else:
                selectedvoxel = None
                block_texture = None
                selected = 'openhand'
            slotselected = slot6
            if selectedvoxel:
                update_hand_properties(hand, model=block_model, texture=block_texture, color=slotselected.hand_color, scale=(0.5,0.5,0.5) if block_model == 'cube' else selectedvoxel.hand_scale if hasattr(selectedvoxel, 'hand_scale') else (0.5, 0.5, 0.5), origin_y=selectedvoxel.yorg if hasattr(selectedvoxel, 'yorg') else 0 if block_model == 'cube' else 1, rotation=selectedvoxel.defaultrotation if hasattr(selectedvoxel, 'defaultrotation') else (0,0,0), position=(0,0,0))
            elif not selectedvoxel and selected == 'ak':
                update_hand_properties(hand, model="PyCraft/Textures/ak.obj", scale=(0.5,0.5,0.5), position=(0,0,0), rotation=(180,0,180))
            else:
                update_hand_properties(hand, model='cube', color=color.hsv(30, 0.4, 0.8), scale=(0.2,0.7,0.2), rotation=(45,0,0), position=(0,0,0))
            defrot = hand.rotation
            destroy(selector)
            selector = Button( 
                color=color.rgb(0.2, 0.2, 0.2), 
                position=(slot6.position.x, slot6.position.y, 0), 
                scale=(0.045, 0.045),
                visible=True
                )
        if key == '7':
            if slot7.equipped and slot7.equipped != 'gun':
                selectedvoxel = slot7.equipped
                block_texture = selectedvoxel.block_texture
                block_model = selectedvoxel.block_model
                selected = 'block'
            elif slot7.equipped == 'gun':
                selectedvoxel = None
                selected = 'ak'
            else:
                selectedvoxel = None
                block_texture = None
                selected = 'openhand'
            slotselected = slot7
            if selectedvoxel:
                update_hand_properties(hand, model=block_model, texture=block_texture, color=slotselected.hand_color, scale=(0.5,0.5,0.5) if block_model == 'cube' else selectedvoxel.hand_scale if hasattr(selectedvoxel, 'hand_scale') else (0.5, 0.5, 0.5), origin_y=selectedvoxel.yorg if hasattr(selectedvoxel, 'yorg') else 0 if block_model == 'cube' else 1, rotation=selectedvoxel.defaultrotation if hasattr(selectedvoxel, 'defaultrotation') else (0,0,0), position=(0,0,0))
            elif not selectedvoxel and selected == 'ak':
                update_hand_properties(hand, model="PyCraft/Textures/ak.obj", scale=(0.5,0.5,0.5), position=(0,0,0), rotation=(180,0,180))
            else:
                update_hand_properties(hand, model='cube', color=color.hsv(30, 0.4, 0.8), scale=(0.2,0.7,0.2), rotation=(45,0,0), position=(0,0,0))
            defrot = hand.rotation
            destroy(selector)
            selector = Button( 
                color=color.rgb(0.2, 0.2, 0.2), 
                position=(slot7.position.x, slot7.position.y, 0), 
                scale=(0.045, 0.045),
                visible=True
                )
        if key == '8':
            if slot8.equipped and slot8.equipped != 'gun':
                selectedvoxel = slot8.equipped
                block_texture = selectedvoxel.block_texture
                block_model = selectedvoxel.block_model
                selected = 'block'
            elif slot8.equipped == 'gun':
                selectedvoxel = None
                selected = 'ak'
            else:
                selectedvoxel = None
                block_texture = None
                selected = 'openhand'
            slotselected = slot8
            if selectedvoxel:
                update_hand_properties(hand, model=block_model, texture=block_texture, color=slotselected.hand_color, scale=(0.5,0.5,0.5) if block_model == 'cube' else selectedvoxel.hand_scale if hasattr(selectedvoxel, 'hand_scale') else (0.5, 0.5, 0.5), origin_y=selectedvoxel.yorg if hasattr(selectedvoxel, 'yorg') else 0 if block_model == 'cube' else 1, rotation=selectedvoxel.defaultrotation if hasattr(selectedvoxel, 'defaultrotation') else (0,0,0), position=(0,0,0))
            elif not selectedvoxel and selected == 'ak':
                update_hand_properties(hand, model="PyCraft/Textures/ak.obj", scale=(0.5,0.5,0.5), position=(0,0,0), rotation=(180,0,180))
            else:
                update_hand_properties(hand, model='cube', color=color.hsv(30, 0.4, 0.8), scale=(0.2,0.7,0.2), rotation=(45,0,0), position=(0,0,0))
            defrot = hand.rotation
            destroy(selector)
            selector = Button( 
                color=color.rgb(0.2, 0.2, 0.2), 
                position=(slot8.position.x, slot8.position.y, 0), 
                scale=(0.045, 0.045),
                visible=True
                )
        if key == '9':
            if slot9.equipped and slot9.equipped != 'gun':
                selectedvoxel = slot9.equipped
                block_texture = selectedvoxel.block_texture
                block_model = selectedvoxel.block_model
                selected = 'block'
            elif slot9.equipped == 'gun':
                selectedvoxel = None
                selected = 'ak'
            else:
                selectedvoxel = None
                block_texture = None
                selected = 'openhand'
            slotselected = slot9
            if selectedvoxel:
                update_hand_properties(hand, model=block_model, texture=block_texture, color=slotselected.hand_color, scale=(0.5,0.5,0.5) if block_model == 'cube' else selectedvoxel.hand_scale if hasattr(selectedvoxel, 'hand_scale') else (0.5, 0.5, 0.5), origin_y=selectedvoxel.yorg if hasattr(selectedvoxel, 'yorg') else 0 if block_model == 'cube' else 1, rotation=selectedvoxel.defaultrotation if hasattr(selectedvoxel, 'defaultrotation') else (0,0,0), position=(0,0,0))
            elif not selectedvoxel and selected == 'ak':
                update_hand_properties(hand, model="PyCraft/Textures/ak.obj", scale=(0.5,0.5,0.5), position=(0,0,0), rotation=(180,0,180))
            else:
                update_hand_properties(hand, model='cube', color=color.hsv(30, 0.4, 0.8), scale=(0.2,0.7,0.2), rotation=(45,0,0), position=(0,0,0))
            defrot = hand.rotation
            destroy(selector)
            selector = Button( 
                color=color.rgb(0.2, 0.2, 0.2), 
                position=(slot9.position.x, slot9.position.y, 0), 
                scale=(0.045, 0.045),
                visible=True
                )
        if key == 'q':
            if slotselected.amount > 0:
                slotselected.amount -= 1


issprinting = False
iscrouching = False

from ursina import *

def flash_vignette():
    vignette.color = color.rgba(255, 0, 0, 1)
    vignette.animate_color(color.rgba(255, 0, 0, 0), duration=1.5, curve=curve.linear)


class CustomFirstPersonController(Entity):
    def __init__(self, **kwargs):
        self.cursor = Entity(parent=camera.ui, model='quad', color=color.pink, scale=.008, rotation_z=45)
        super().__init__()
        self.speed = 5
        self.height = 2
        self.camera_pivot = Entity(parent=self, y=self.height)

        camera.parent = self.camera_pivot
        camera.position = (0,0,0)
        camera.rotation = (0,0,0)
        camera.fov = 90
        mouse.locked = True
        self.mouse_sensitivity = Vec2(40, 40)

        self.gravity = 25
        self.gravity_enabled = True
        self.vertical_velocity = 0
        self.grounded = False
        self.jump_speed = 9  # Adjusted jump speed
        self.jumping = False

        self.last_space_press_time = 0
        self.space_press_count = 0
        self.double_press_threshold = 0.3

        self.traverse_target = scene     # by default, it will collide with everything. change this to change the raycasts' traverse targets.
        self.ignore_list = [self, ]
        self.on_destroy = self.on_disable

        for key, value in kwargs.items():
            setattr(self, key ,value)

        # make sure we don't fall through the ground if we start inside it
        if self.gravity:
            ray = raycast(self.world_position+(0,self.height,0), self.down, traverse_target=self.traverse_target, ignore=self.ignore_list)
            if ray.hit:
                self.y = ray.world_point.y



    def update(self):
        self.rotation_y += mouse.velocity[0] * self.mouse_sensitivity[1]

        self.camera_pivot.rotation_x -= mouse.velocity[1] * self.mouse_sensitivity[0]
        self.camera_pivot.rotation_x= clamp(self.camera_pivot.rotation_x, -90, 90)

        self.direction = Vec3(
            self.forward * (held_keys['w'] - held_keys['s'])
            + self.right * (held_keys['d'] - held_keys['a'])
            ).normalized()

        feet_ray = raycast(self.position+Vec3(0,0.5,0), self.direction, traverse_target=self.traverse_target, ignore=self.ignore_list, distance=.5, debug=False)
        head_ray = raycast(self.position+Vec3(0,self.height-.1,0), self.direction, traverse_target=self.traverse_target, ignore=self.ignore_list, distance=.5, debug=False)
        if not feet_ray.hit and not head_ray.hit:
            move_amount = self.direction * time.dt * self.speed

            if raycast(self.position+Vec3(-.0,1,0), Vec3(1,0,0), distance=.5, traverse_target=self.traverse_target, ignore=self.ignore_list).hit:
                move_amount[0] = min(move_amount[0], 0)
            if raycast(self.position+Vec3(-.0,1,0), Vec3(-1,0,0), distance=.5, traverse_target=self.traverse_target, ignore=self.ignore_list).hit:
                move_amount[0] = max(move_amount[0], 0)
            if raycast(self.position+Vec3(-.0,1,0), Vec3(0,0,1), distance=.5, traverse_target=self.traverse_target, ignore=self.ignore_list).hit:
                move_amount[2] = min(move_amount[2], 0)
            if raycast(self.position+Vec3(-.0,1,0), Vec3(0,0,-1), distance=.5, traverse_target=self.traverse_target, ignore=self.ignore_list).hit:
                move_amount[2] = max(move_amount[2], 0)
            self.position += move_amount

        if self.gravity and self.gravity_enabled:
            # Apply gravity
            self.vertical_velocity -= self.gravity * time.dt

            # Calculate potential movement
            delta_y = self.vertical_velocity * time.dt

            # Check for collision in the vertical movement
            direction = Vec3(0, math.copysign(1, delta_y), 0) if delta_y != 0 else Vec3(0,0,0)
            ray = raycast(self.position + Vec3(0, self.height / 2, 0), direction, distance=self.height / 2 + abs(delta_y), traverse_target=self.traverse_target, ignore=self.ignore_list)
            if ray.hit:
                if self.vertical_velocity < 0:
                    # Landing on ground
                    self.y = ray.world_point.y
                    self.vertical_velocity = 0
                    self.grounded = True
                elif self.vertical_velocity > 0:
                    # Hitting ceiling
                    self.y = ray.world_point.y - self.height
                    self.vertical_velocity = 0
            else:
                # No collision, proceed with movement
                self.y += delta_y
                self.grounded = False
        else:
            self.vertical_velocity = 0
            self.grounded = False

            vertical_movement = (held_keys['space'] - held_keys['left control']) * self.speed * time.dt
            self.y += vertical_movement
    def input(self, key):
        if key == 'space' and not creative:
            self.jump()
        if key == 'space' and creative:
            current_time = time.time()
            if current_time - self.last_space_press_time <= self.double_press_threshold:
                # Detected double press
                self.gravity_enabled = not self.gravity_enabled
                print(f"Gravity enabled: {self.gravity_enabled}")
                # Reset the space press count
                self.space_press_count = 0
                self.last_space_press_time = 0
            else:
                # First press, start counting
                self.last_space_press_time = current_time
                self.space_press_count = 1
                # Handle jump if gravity is enabled
                if self.gravity_enabled:
                    self.jump()

    def jump(self):
        if not self.grounded or not self.gravity_enabled:
            return
        self.vertical_velocity = self.jump_speed
        self.grounded = False

    def on_enable(self):
        mouse.locked = True
        self.cursor.enabled = True
        # restore parent and position/rotation from before disablem in case you moved the camera in the meantime.
        if hasattr(self, 'camera_pivot') and hasattr(self, '_original_camera_transform'):
            camera.parent = self.camera_pivot
            camera.transform = self._original_camera_transform

    def on_disable(self):
        mouse.locked = False
        self.cursor.enabled = False
        self._original_camera_transform = camera.transform  # store original position and rotation
        camera.world_parent = scene

transition_speed = 1/1200  # Adjust the speed of the color change. original time is 1/1200
light_to_dark = True  # Flag to determine the direction of transition
last_y_position = None
fall_start_y = None
is_falling = False
health = 100

def update_hearts():
    num_full_hearts = int(health / 10)
    remainder = health % 10

    for i in range(10):
        if i < num_full_hearts:
            hearts[::-1][i].texture = 'PyCraft/Textures/fullheart.png'
        elif i == num_full_hearts and remainder >= 5:
            hearts[::-1][i].texture = 'PyCraft/Textures/halfheart.png'
        else:
            hearts[::-1][i].texture = 'PyCraft/Textures/emptyheart.png'

def animatehand():
    hand.rotation = defrot

    hand.animate_rotation(selectedvoxel.animationrotation if hasattr(selectedvoxel, 'animationrotation') else (110, -30, 0), duration=0.2, curve=curve.in_out_quad)
                            
    invoke(hand.animate_rotation, defrot, duration=0.2, curve=curve.in_out_quad, delay=0.2)

def update():
    global fov_slider, issprinting, iscrouching, paused, last_y_position, fall_start_y, health, is_falling, light_to_dark, currently_breaking_block, block_break_start_time, mouse_held, overlay_entity, mining_animation_running, coordslabel, tiptext, title_screen_open, slot1amount
    if paused:
        player.enabled = False
        return
    current_y = player.position.y
    if not main_menu_open:
        slot1amount.text = slot1.amount
        slot2amount.text = slot2.amount
        slot3amount.text = slot3.amount
        slot4amount.text = slot4.amount
        slot5amount.text = slot5.amount
        slot6amount.text = slot6.amount
        slot7amount.text = slot7.amount
        slot8amount.text = slot8.amount
        slot9amount.text = slot9.amount
        if slotselected.amount < 1:
            slotselected.amount = 0
            slotselected.visible = False
            slotselected.equipped = None
            update_equipped_slot(slotselected)
    if not creative:
        if last_y_position is not None:
            if current_y < last_y_position:
                if not is_falling:
                    fall_start_y = last_y_position
                is_falling = True
            elif current_y >= last_y_position:
                if is_falling:
                    fall_distance = fall_start_y - current_y
                    if fall_distance > 3:
                        fall_damage = int((fall_distance - 3) * 5)
                        health -= fall_damage
                        flash_vignette()
                        print(f'You took {fall_damage} damage from fall damage!')
                        num_full_hearts = int(health / 10)
                        remainder = health % 10

                        for i in range(10):
                            if i < num_full_hearts:
                                hearts[::-1][i].texture = 'PyCraft/Textures/fullheart.png'
                            elif i == num_full_hearts and remainder >= 5:
                                hearts[::-1][i].texture = 'PyCraft/Textures/halfheart.png'
                            else:
                                hearts[::-1][i].texture = 'PyCraft/Textures/emptyheart.png'

                        if health <= 0:
                            build_death_screen()
                            print("Player has died")
                    is_falling = False
    if debugOpen:
        coordslabel.text = f'Coordinates: X:{int(player.position.x)} Y:{int(player.position.y)} Z:{int(player.position.z)}'
    last_y_position = current_y
    update_hand_position(   )
    if title_screen_open:
        tiptext.scale = 1.5 + math.sin(time.time() * 2) * 0.1
    if holding_block:
        block_drag.position = Vec3(mouse.x, mouse.y, -2.1)
        block_drag_amount.position = Vec3(mouse.x + 0.01, mouse.y - 0.01, -2.2)
    if held_keys['shift']:
        player.speed = 10
        if not issprinting:
            camera.animate('fov', camera.fov + 10, duration = 0.05, curve=curve.linear)
            issprinting = True
    else:
        player.speed = 5
        if issprinting:
            camera.animate('fov', camera.fov - 10, duration=0.05, curve=curve.linear)
            issprinting = False

    if light_to_dark:
        sky.color = color.rgb(
            max(sky.color.r - transition_speed * time.dt, 0),
            max(sky.color.g - transition_speed * time.dt, 0),
            max(sky.color.b - transition_speed * time.dt, 0), 
        )
        if sky.color.r <= 0 and sky.color.g <= 0 and sky.color.b <= 0:
            light_to_dark = False
    else:
        sky.color = color.rgb(
            min(sky.color.r + transition_speed * time.dt, 1),
            min(sky.color.g + transition_speed * time.dt, 1),
            min(sky.color.b + transition_speed * time.dt, 1),
        )
        if sky.color.r >= 1 and sky.color.g >= 1 and sky.color.b >= 1:
            light_to_dark = True


    brightness = sky.color.r

    start_color = color.rgba(1,1,1,0.5)
    end_color = color.rgba(0.5,0.5,0.5,0.5)

    cloud_r = end_color.r + (start_color.r - end_color.r)*brightness
    cloud_g = end_color.g + (start_color.g - end_color.g)*brightness
    cloud_b = end_color.b + (start_color.b - end_color.b)*brightness
    cloud_a = 0.5

    for cloud in clouds:
        for c in cloud.children:
            c.color = color.rgba(cloud_r, cloud_g, cloud_b, cloud_a)

    for cloud in clouds:
        cloud.x += time.dt * 0.2
        if cloud.x > 60:
            cloud.x = -60
    if not creative and mouse_held and currently_breaking_block:
        hit_info = raycast(camera.world_position, camera.forward, distance=5, ignore=(player,))
        if not hit_info.hit or hit_info.entity != currently_breaking_block:
            currently_breaking_block.texture = currently_breaking_block.original_texture
            currently_breaking_block = None
            block_break_start_time = None
            mouse_held = False

            if overlay_entity:
                destroy(overlay_entity)
                overlay_entity = None
        else:
            elapsed = time.time() - block_break_start_time
            block_type = type(currently_breaking_block).__name__
            required_time = block_break_times.get(block_type, 1.0)
            tool_multiplier = mining_tools.get(selectedvoxel, 1.0) if hasattr(currently_breaking_block, 'blockclass') and hasattr(selectedvoxel, 'classaffect') and currently_breaking_block.blockclass in selectedvoxel.classaffect else 1.0
            if required_time == float('inf'):
                pass
            else:
                ratio = elapsed / (required_time * tool_multiplier)
                stage_count = 6
                stage = int(ratio * stage_count)
                if stage >= stage_count:
                    stage = stage_count - 1
                if overlay_entity:
                    overlay_entity.texture = block_breaking_stages[stage]
                if elapsed >= (required_time * tool_multiplier):
                    position = currently_breaking_block.position
                    destroy(currently_breaking_block)
                    DroppedBlock(position=position, texture=currently_breaking_block.texture, block_class=type(currently_breaking_block))
                    for block in world_data:
                        if block['position'] == [position.x, position.y, position.z]:
                            world_data.remove(block)
                            break
                    
                    currently_breaking_block = None
                    block_break_start_time = None
                    mouse_held = False
                    animatehand()
                    if overlay_entity:
                        destroy(overlay_entity)
                        overlay_entity = None

    player.enabled = mouse.locked
player = CustomFirstPersonController()
player.height = 1.8
player.camera_pivot.y = 1.8
mouse.locked = False
sky = Sky(texture="sky_default")
sky.color = color.hsv(0, 0, 0.9)
app.run()
