# firstpersonroguelike
Roguelike with a first-person 3D viewport

### Tech
Written in python using libtcod. It's kinda slow, but it works, and I didn't have to write a terminal renderer from scratch which is nice.

## How to run
Requires Python 3 installed (I used 3.8)

```bash
$ git clone https://github.com/TechniMan/firstpersonroguelike
$ cd firstpersonroguelike
$ virtualenv venv
$ ./venv/Scripts/activate  # (add .bat for Windows cmd)

> pip install pillow
> pip install tcod
> python engine.py
```
When you're done with the virtual environment, simply enter:
```bash
> deactivate
```

## Controls

Use the direction keys left and right to rotate 45degrees either direction, and up to move forwards. Use `g` to pick up an item you're standing on, `i` to open inventory to use an item, and `d` to open inventory to drop an item. Walking into an enemy will attack them.
* `up`: move forwards
* `left`: turn 45deg left
* `right`: turn 45deg right
* `down`: move backwards
* `g`: pick up an item you're standing on
* `i`: open inventory to use an item
* `d`: open inventory to drop an item
* numpad `1`,`2`,`3`,`4`,`6`,`7`,`8`,`9`: move in that direction relative to the map
* `esc` to quit

Other entities aren't yet drawn in the 3D viewport. I'm working on texture mapping which should allow this.
