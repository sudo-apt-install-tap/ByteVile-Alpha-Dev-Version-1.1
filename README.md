# BYTEVILE — Alpha Dev v1.1  
### *(ProcGen v1 | highly unstable)*

> *“The code remembers. Even when you don’t.”*

---

## What is this place?
**ByteVile** is a terminal-bound narrative experiment —  
a text adventure rotting gently inside a digital corpse.

You walk through fragments.  
Rooms generate themselves.  
Memory lies.  
The world pretends it’s deterministic.

This build is **actively mutating**.  
Expect bugs. Expect gaps. Expect the story to occasionally stare back.

Also yeah — the plot is a little feral right now. That’s intentional. Probably.

---

## ⚠️ Warning: ProcGen Branch
This is the **procedural generation branch**.  
It is:
- unstable  
- experimental  
- mildly haunted  

I do **not** recommend trying to fully comprehend the code.  
It barely comprehends itself.

---

## Commands
start → begin the descent </br>
save → preserve the illusion</br>
load → resurrect old ghosts</br>
exit → leave (you never really leave)</br>

---

## Feedback / Bugs / Weirdness
If something breaks — or something *feels* too sentient —  
email me: **work.tapishnud@gmail.com**

Testing, suggestions, and existential dread are all welcome.  
Happy hacking 🖤

---

-- ByteVile — Alpha Dev v1.1
 With Love 🖤

---

## 🔧 Adding POIs (Points of Interest)

You can add in-game POIs by editing `Data/pois.json`. Each POI entry is a JSON object with fields:

- `id` (string): short identifier
- `name` (string): display name
- `text` (string): the text shown when the player reaches the POI
- `story_node` (string|null): optional link to a story node in `Data/story.json`
- `once` (bool): if true, the POI is removed after being triggered
- `x`, `y` (ints, optional): optional fixed coordinates; if omitted (or invalid), the POI will be auto-placed on a floor tile

If you don't add `Data/pois.json`, the game will place a few example POIs automatically.

Example entry:

```json
{ "id": "terminal", "name": "Flickering Terminal", "text": "A terminal pulses...", "story_node": "terminal", "once": false }
```
