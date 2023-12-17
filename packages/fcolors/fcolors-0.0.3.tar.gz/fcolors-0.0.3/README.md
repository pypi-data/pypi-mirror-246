# colors

Colors is a simple library that makes it easier to use colors in fstrings.
The standard ansi colors are (in order):

- Black
- Red
- Green
- Yellow
- Blue
- Pink
- Cyan
- White

These are accessible in the following variations:

- (f)ore(g)round
- (b)ack(g)round
- (u)nder(line)d
- (bold)ed
- (f)ore(g)round_(hi)lighted
- (b)ack(g)round_(hi)lighted
- (bold)_(hi)lighted

Forground, Background, Underline, and Bold can all be chained together in any order, as:

```python3
f"{uline.blue}{bg.red}red underlined text{reset}"
```

Highlighted colors must be custom-built due to a difference in how their codes are constructed.
This can be done as so:

```python3
f"{all_hi(Color.Blue, Color.White, bold=0)}this is white on blue text, unbolded{reset}"
```

While I may end up figuring out a way around this, it will not be soon. Feel free to use these features as-is.


## Installation
```sh
$ pip3 install colors
```

or

```sh
$ python3 setup.py install
```

## Examples
### Hello, World!
```python3
from fcolors.fcolors import fg, bg, bold, reset

print(f"{bg.blue}{bold.white}Hello, World!{reset}")

```
### A tree that talks
```python3
from fcolors.fcolors import fg, fg_hi, bg, bg_hi, bold, reset, all_hi, Color

canopy = f"{fg.green}"
leaves = f"{fg.green}"
wood   = f"{bold.yellow}"
grass  = f"{bg_hi.green}"
text   = f"{bold.white}"
c = canopy
l = leaves
w = wood
x = reset
t = text

def rgb(string):
    chars = [c for c in string]
    for index in range(len(chars)):
        chars[index] = bold.colors[index % len(bold.colors)-1] + chars[index]
    return ''.join(chars) + f'{text}'
picture = (
f"""\
  {c}__________{x}  {t}  ______________________
 {l}/       )  \{x} {t} /                      \ 
{l}| (          |{x}{t}|  Have fun using my     |
 {l}\________)_/{x} {t}|    {rgb('fcolors')} package!    |
   {w}|  ||  |{x}   {t}|   - Jayson             |
    {w}\ -- /{x}    {t} \    __________________/
     {w}|  |{x}     {t}  | _/
     {w}|  |{x}     {t} <_/
     {w}|  |{x}
     {w}|  |{x}
{grass}                                              {reset}""")

print(picture)
```


## License

See LICENSE.
