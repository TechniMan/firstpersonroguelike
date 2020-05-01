# firstpersonroguelike
Roguelike with a first-person 3D viewport

### Tech
Written in python using libtcod. It's kinda slow, but it works, and I didn't have to write a terminal renderer from scratch which is nice.

## How to play

Use the direction keys left and right to rotate 45degrees either direction, and up to move forwards. Use `g` to pick up an item you're standing on, `i` to open inventory to use an item, and `d` to open inventory to drop an item. Walking into an enemy will attack them.

Other entities aren't yet drawn in the 3D viewport.

## How to run

```bash
$ git clone https://github.com/TechniMan/firstpersonroguelike
$ cd firstpersonroguelike
$ ./venv/Scripts/activate  # (add .bat for Windows)
$ pip install pillow
$ pip install tcod
$ python engine.py
```

Wow, that sucks. Maybe I'll make a script for it later.
