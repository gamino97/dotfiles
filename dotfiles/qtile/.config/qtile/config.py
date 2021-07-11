# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# Qtile Website: http://docs.qtile.org/en/latest/index.html
import os
import subprocess
from typing import List  # noqa: F401

from libqtile import bar, layout, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen, KeyChord
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

mod = "mod4"
terminal = guess_terminal()

keys = [
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(),
        desc="Move window focus to other window"),

    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(),
        desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(),
        desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(),
        desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
# RESIZE UP, DOWN, LEFT, RIGHT
    Key([mod, "control"], "l",
        lazy.layout.grow_right(),
        lazy.layout.grow(),
        lazy.layout.increase_ratio(),
        lazy.layout.delete(),
        ),
    Key([mod, "control"], "Right",
        lazy.layout.grow_right(),
        lazy.layout.grow(),
        lazy.layout.increase_ratio(),
        lazy.layout.delete(),
        ),
    Key([mod, "control"], "h",
        lazy.layout.grow_left(),
        lazy.layout.shrink(),
        lazy.layout.decrease_ratio(),
        lazy.layout.add(),
        ),
    Key([mod, "control"], "Left",
        lazy.layout.grow_left(),
        lazy.layout.shrink(),
        lazy.layout.decrease_ratio(),
        lazy.layout.add(),
        ),
    Key([mod, "control"], "k",
        lazy.layout.grow_up(),
        lazy.layout.grow(),
        lazy.layout.decrease_nmaster(),
        ),
    Key([mod, "control"], "Up",
        lazy.layout.grow_up(),
        lazy.layout.grow(),
        lazy.layout.decrease_nmaster(),
        ),
    Key([mod, "control"], "j",
        lazy.layout.grow_down(),
        lazy.layout.shrink(),
        lazy.layout.increase_nmaster(),
        ),
    Key([mod, "control"], "Down",
        lazy.layout.grow_down(),
        lazy.layout.shrink(),
        lazy.layout.increase_nmaster(),
        ),

    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    # Key([mod, "control"], "h", lazy.layout.grow_left(),
    #     desc="Grow window to the left"),
    # Key([mod, "control"], "l", lazy.layout.grow_right(),
    #     desc="Grow window to the right"),
    # Key([mod, "control"], "j", lazy.layout.grow_down(),
    #     desc="Grow window down"),
    # Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "shift"], "Return", lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack"),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),

    Key([mod, "control"], "r", lazy.restart(), desc="Restart Qtile"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawn("dmenu_run -p 'Run: '"),
        # lazy.spawncmd(), # This was the original.
        desc="Spawn a command using a prompt widget"),
    Key([], 'Print', lazy.spawn("scrot '%Y-%m-%d_%H-%M-%S-$wx$h_scrot.png' -e 'mv $f ~/Imágenes/Screenshots'")),
    Key(['shift'], 'Print', lazy.spawn("./dmscripts/scrot.sh")),
    # Key([mod], 's', lazy.spawn("./dmscripts/scrot.sh")),

    Key([mod], 's', lazy.spawn(["sh", "-c", "scrot -s '%Y-%m-%d_%H-%M-%S-$wx$h_scrot.png' -e 'mv $f ~/Imágenes/Screenshots'"])),
    Key([mod], "m",
        lazy.window.toggle_floating(),
        desc='toggle window between minimum and maximum sizes'),

    # Set theme on restart keybinding.
    Key([mod, 'control'], 't', lazy.spawn('python3.7 ./bashscripts/restart_qtile.py')),

    # These lines allow to raise or lower master volume
    # Key([], 'XF86AudioRaiseVolume', lazy.spawn('amixer -D pulse sset Master 5%+')),
    Key([], 'XF86AudioRaiseVolume', lazy.spawn('./bashscripts/raise_volume.sh')),
    # Key([], 'XF86AudioLowerVolume', lazy.spawn('amixer -D pulse sset Master 5%-')),
    Key([], 'XF86AudioLowerVolume', lazy.spawn('./bashscripts/lower_volume.sh')),
    Key([], 'XF86AudioMute', lazy.spawn('./bashscripts/mute_volume.sh')),
    Key([], 'XF86AudioPlay', lazy.spawn('./dmscripts/audio-control')),
    KeyChord([mod], 'e', [
        Key([], 'e', lazy.spawn("emacsclient -c -a 'emacs'"), desc='Launch Emacs'),
        Key([], 'b', lazy.spawn("brave-browser-stable"), desc='Launch Brave'),
        Key([], 'd', lazy.spawn("./bashscripts/toggle_monitors.sh"), desc='Restore monitors'),
        Key([], 'f', lazy.spawn("pcmanfm"), desc='Restore monitors'),

    ]),
]


group_names = [("", {'layout': 'monadtall'}),
               ("", {'layout': 'max'}),
               ("", {'layout': 'monadtall'}),
               ("", {'layout': 'monadtall'}),
               ("", {'layout': 'monadtall'}),
               ("", {'layout': 'monadtall'}),
               ("", {'layout': 'monadtall'}),
               ("", {'layout': 'monadtall'}),
               ("", {'layout': 'monadtall'})]

# group_keybindings = ('t', 'e', 'b', 'f', 'm', 'd', 'v', 'i', '1')

groups = [Group(name, **kwargs) for name, kwargs in group_names]

for i, (name, kwargs) in enumerate(group_names, 1):
    keys.append(Key([mod], str(i), lazy.group[name].toscreen()))        # Switch to another group
    keys.append(Key([mod, "shift"], str(i), lazy.window.togroup(name)))  # Send current window to another group
# groups = [Group(i) for i in "123456789"]

#     keys.extend([
#         # mod1 + letter of group = switch to group
#         Key([mod], i.name, lazy.group[i.name].toscreen(),
#             desc="Switch to group {}".format(i.name)),

#         # mod1 + shift + letter of group = switch to & move focused window to group
#         Key([mod, "shift"], i.name, lazy.window.togroup(i.name, switch_group=True),
#             desc="Switch to & move focused window to group {}".format(i.name)),
#         # Or, use below if you prefer not to switch to that group.
#         # # mod1 + shift + letter of group = move focused window to group
#         # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
#         #     desc="move focused window to group {}".format(i.name)),
#     ])

layout_theme = {"border_width": 2,
                "margin": 4,
                "border_focus": "e1acff",
                "border_normal": "1D2330"
                }
layouts = [
    layout.MonadTall(**layout_theme),
    # layout.Columns(border_focus_stack='#d75f5f'),
    layout.Max(**layout_theme),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(**layout_theme),
    # layout.Matrix(**layout_theme),
    # layout.MonadTall(),
    # layout.MonadWide(**layout_theme),
    layout.RatioTile(**layout_theme),
    # layout.Tile(**layout_theme),
    # layout.TreeTab(**layout_theme),
    # layout.VerticalTile(**layout_theme),
    # layout.Zoomy(**layout_theme),
]

widget_defaults = dict(
    font='sans',
    fontsize=12,
    padding=3,
)
extension_defaults = widget_defaults.copy()


colors = [["#282c34", "#282c34"],  # panel background
          ["#3d3f4b", "#434758"],  # background for current screen tab
          ["#ffffff", "#ffffff"],  # font color for group names
          ["#ff5555", "#ff5555"],  # border line color for current tab
          ["#74438f", "#74438f"],  # border line color for 'other tabs' and color for 'odd widgets'
          ["#4f76c7", "#4f76c7"],  # color for the 'even widgets'
          ["#e1acff", "#e1acff"],  # window name
          ["#ecbbfb", "#ecbbfb"]]  # backbround for inactive screens

colors = []
cache='/home/gamino/.cache/wal/colors'
def load_colors(cache):
    with open(cache, 'r') as file:
        for i in range(8):
            colors.append(file.readline().strip())
    colors.append('#ffffff')
    lazy.reload()
load_colors(cache)

colors2 = {
    'background': colors[0],
    'foreground': colors[1],
    'group_name': colors[2],
    'border_current_tab': colors[3],
    'border_other_tab': colors[4],
    'even': colors[3],
    'window_name': colors[7],
    'inactive_screens': colors[7],
    'color1': colors[8],
    'active_group': colors[4],
    'inactive_group': colors[8],
    'odd': colors[2],
}
even = False
even_odd_list = [colors2['odd'], colors2['even']]

def get_powerline(first=False):
    global even
    even = not even
    current_color = even_odd_list[int(even)]
    if first:
        current_color = colors2['background']
    return widget.TextBox(text='', background=current_color, foreground=even_odd_list[int(not even)], padding=0, fontsize=37)

def get_bg_color():
    return even_odd_list[int(not even)]

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.Image(
                    filename='~/.config/qtile/icons/mint.png',
                    scale='False',
                    background=colors2['background']
                ),
                widget.Sep(
                    linewidth=0,
                    padding=6,
                    foreground=colors2['background'],
                    background=colors2['background']
                ),
                # widget.CurrentLayout(),
                widget.GroupBox(
                    font="file-icons",
                    fontsize=20,
                    margin_y=3,
                    margin_x=0,
                    padding_y=5,
                    padding_x=3,
                    borderwidth=3,
                    active=colors2['active_group'],
                    inactive=colors2['inactive_group'],
                    rounded=False,
                    highlight_color=colors[1],
                    highlight_method='line',
                    this_current_screen_border=colors[6],
                    this_screen_border=colors[4],
                    other_current_screen_border=colors[6],
                    other_screen_border=colors[4],
                    foreground=colors2['foreground'],
                    background=colors2['background'],
                ),
                widget.Prompt(
                    # prompt = prompt,
                    font="Ubuntu Mono",
                    padding=10,
                    foreground=colors[3],
                    background=colors[1]
                ),
                widget.Sep(
                    linewidth=0,
                    padding=40,
                    foreground=colors2['background'],
                    background=colors2['background']
                ),
                widget.WindowName(
                    foreground=colors2['window_name'],
                    background=colors2['background'],
                    padding=0
                ),
                widget.Chord(
                    chords_colors={
                        'launch': ("#ff0000", "#ffffff"),
                    },
                    name_transform=lambda name: name.upper(),
                ),
                widget.Sep(
                    linewidth=0,
                    padding=6,
                    foreground=colors2['background'],
                    background=colors2['background']
                ),
                widget.Notify(
                    background=colors2['background'],
                ),
                # widget.TextBox(
                #     text='',
                #     background=colors2['background'],
                #     foreground=colors[4],
                #     padding=0,
                #     fontsize=37
                # ),
                # get_even_powerline(),
                get_powerline(True),
                widget.CurrentLayoutIcon(
                    scale=0.7,
                    foreground=colors2['color1'],
                    background=get_bg_color(),
                ),
                get_powerline(),
                # get_odd_powerline(),
                # widget.TextBox(
                #     text='',
                #     background=colors[4],
                #     foreground=colors[5],
                #     padding=0,
                #     fontsize=37
                # ),
                # widget.Net(
                #     interface = "enp1s0",
                #     format = '{down} ↓↑ {up}',
                #     foreground = colors[2],
                #     background = colors[4],
                #     padding = 5
                # ),
                widget.TextBox(
                    text="🌡",
                    foreground=colors2['color1'],
                    background=get_bg_color(),
                    fontsize=20
                ),
                widget.ThermalSensor(
                    foreground=colors2['color1'],
                    background=get_bg_color(),
                    threshold=90,
                    padding=5
                ),
                get_powerline(),
                widget.Volume(
                    foreground=colors2['color1'],
                    background=get_bg_color(),
                    device='pulse',
                    emoji=True,
                    step=5
                ),  # We set device to pulse to get it working
                get_powerline(),
                # widget.Battery(
                #     foreground=colors[2],
                #     background=colors[5],
                # ),
                widget.Battery(
                    foreground=colors2['color1'],
                    background=get_bg_color(),
                    notify_below=25,
                    format='{char} {percent:2.0%} {hour:d}:{min:02d}',
                    update_interval=5,
                ),
                widget.BatteryIcon(
                    foreground=colors2['color1'],
                    background=get_bg_color(),
                ),
                get_powerline(),
                widget.Systray(
                    foreground=colors2['color1'],
                    background=get_bg_color(),
                    padding=5
                ),
                get_powerline(),
                widget.Clock(
                    # format='%Y-%m-%d %a\n %I:%M %p',
                    format='%a %d-%m-%Y %I:%M %p',
                    foreground=colors2['color1'],
                    background=get_bg_color(),
                    # fontsize=10,

                ),
            ],
            24,
            opacity=0.9,
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
main = None  # WARNING: this is deprecated and will be removed soon
follow_mouse_focus = False
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    *layout.Floating.default_float_rules,
    Match(wm_class='confirmreset'),  # gitk
    Match(wm_class='makebranch'),  # gitk
    Match(wm_class='maketag'),  # gitk
    Match(wm_class='ssh-askpass'),  # ssh-askpass
    Match(title='branchdialog'),  # gitk
    Match(title='pinentry'),  # GPG key password entry
    Match(wm_class='Matplotlib'),  # Matplotlib graph
    Match(wm_class='org-languagetool-openoffice-SpellAndGrammarCheckDialog'),  # Libre office grammar check
])
auto_fullscreen = True
focus_on_window_activation = "smart"


@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/autostart.sh'])


# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
