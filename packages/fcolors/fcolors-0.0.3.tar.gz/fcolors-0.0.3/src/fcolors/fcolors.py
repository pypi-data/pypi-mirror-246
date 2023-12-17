from dataclasses import dataclass

esc = '\x1B['

reset = f'{esc}0m'

"""
This is a Color module for python that supports ANSI color escapes.
Colors can be referenced by name as the standard ANSI color names.
Usage:
    from colors import fg, bg, reset
    f"{fg.red}this is some red text{reset}"
    f"{bg.red}this is some default text on red background{reset}"

"""


@dataclass
class Color:
    """This class can be used as an enumeration, but should not be modified or instantiated.
    A style can be iterated over via the property `NAME.colors`"""

    Black = 0
    Red = 1
    Green = 2
    Yellow = 3
    Blue = 4
    Pink = 5
    Cyan = 6
    White = 7
    
    PX = 3
    def __init__(self,px:int):
        self.PX = px
    @property
    def black(self):
        return f"{esc}{self.PX}{Color.Black}m"
    @property
    def red(self):
        return f"{esc}{self.PX}{Color.Red}m"
    @property
    def green(self):
        return f"{esc}{self.PX}{Color.Green}m"
    @property
    def yellow(self):
        return f"{esc}{self.PX}{Color.Yellow}m"
    @property
    def blue(self):
        return f"{esc}{self.PX}{Color.Blue}m"
    @property
    def pink(self):
        return f"{esc}{self.PX}{Color.Pink}m"
    @property
    def cyan(self):
        return f"{esc}{self.PX}{Color.Cyan}m"
    @property
    def white(self):
        return f"{esc}{self.PX}{Color.White}m"

    @property
    def colors(self):
        return [self.black,self.red,self.green,self.yellow,self.blue,self.pink,self.cyan,self.white]


bg = Color(4)
fg = Color(3)
bold = Color("1;3")
uline = Color("4;3")
fg_hi = Color(";9")
bold_hi = Color("1;9")
bg_hi = Color("0;10")

def all_hi(bgcolor:int,fgcolor:int,*,bold=0):
    """Usage: all_hi(bgcolor: Color.<...>, fgcolor: Color.<...>, {bold=1|0})"""
    return f"{esc}{bold};10{bgcolor};9{fgcolor}m"

if __name__ == '__main__':

    for bgc,fgc in zip(reversed(bg.colors),fg.colors):
        print(f"{bgc}{fgc}Standard{reset}")

    for fgc in fg_hi.colors:
        print(f"{fgc}High Intensity Foreground{reset}")

    for bgc in bg_hi.colors:
        print(f"{bgc}High Intensity Background{reset}")

    for fgc in uline.colors:
        print(f"{fgc}{bg.white}Underline with white background!{reset}")

    for fgc in bold.colors:
        print(f"{fgc}{bg.blue}Bolded text on blue background!{reset}")

    print(f"{all_hi(Color.Blue,Color.Yellow,bold=1)}some yellow on blue action{reset}")

    print(f"{bold_hi.red}Caveats: Currently high intensity fg/bg cannot be used via concatenation.")
    print(f"The proper way to handle this is {all_hi(Color.Blue,Color.White,bold=1)}`hi_2(Color.Blue,Color.White,bold=1|0)`{reset}")
    print(f"{bold_hi.red}I probably won't add the extra logic necessary to fix this issue.{reset}")

