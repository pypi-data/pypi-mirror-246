"""
=================== __file__: 'asciiTUI/__init__.py' ===================
======================= import_name : 'asciiTUI' =======================
                                                                        
Last Update: 16/12 (December)/2023 <GMT+7>                              
                                                                        
Description: This is a library of tools for you to use with your needs  
               for an attractive type of terminal (console) display.    
                                                                        
Information: Type `print(dir(asciiTUI))` for further functions, then    
                type `print(asciiTUI.<func>.__doc__)` for further       
                      document information of each function             
"""

# -- importing: all: {os, re, sys, getpass}, add: {windows: {msvcrt} else: {tty, termios}} -- #
import os as _os
import re as _re
import sys as _sys
import getpass as _getpass
if _sys.platform == 'win32':
  from msvcrt import getch as _getch
else:
  import tty as _tty
  import termios as _termios

# -- var(s) -- #
__version__ = '1.2.2'
module_use  = r'{os, re, sys, getpass}, add: {windows: {msvcrt} else: {tty, termios}}'
lorem_ipsum = "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum."

# -- class Error(s) -- #
class OptionNotFoundError(Exception):
  def __init__(self, *message):
    super().__init__(*message)

class PythonVersionError(Exception):
  def __init__(self, *message):
    super().__init__(*message)

# -- Python version checking -- #
if _sys.version_info[0] == 2:
  raise PythonVersionError("asciiTUI only works in python 3, not 2")

# -- func(s) -- #
# -- func: removing ansi code | return [str] -- #
def remove_ansi(text:str)->str:
  """
return: `str`

Example use:
  >>> import asciiTUI as tui
  >>> text = '\\033[32mHello World!\\033[36m'
  >>> len(text)
  22
  >>> len(tui.remove_ansi(text=text))
  12

Args:
  `text` : The main text that will remove the ansi code
  """
  text = str(text)
  text = _re.sub(r'\033\[[0-9;]*[mK]', '', text)
  text = _re.sub(r'\x1b\[[0-9;]*[mK]', '', text)
  text = _re.sub(r'\x1B\][0-9;]*[mK]', '', text)
  text = _re.sub(r'\u001b\][0-9;]*[mK]', '', text)
  return text

# -- func: get terminal size | return [int] -- #
def terminal_size(get:str)->int:
  """
return: `int`

Example use:
  >>> import asciiTUI as tui
  >>> tui.terminal_size(get='x')
  120
  >>> # The numbers above will not match the output results you get. It all depends on the size of your terminal when executed.
  >>> tui.terminal_size('xy')
  (120, 30)

Args:
  `get` : The type of terminal size you will get. `x`: width, `y`: height
  """
  get = str(get).lower()
  x, y = _os.get_terminal_size().columns, _os.get_terminal_size().lines
  if get == 'x': return x
  elif get == 'y': return y
  elif get == 'xy': return x, y
  elif get == 'yx': return y, x
  else: raise OptionNotFoundError(f"'{get.lower()}' The get type is not found.")

# -- func: make color text terminal | return [str] -- #
def rgb(r=255, g=255, b=255, style='fg')->str:
  """
return: `str`

Example use:
  >>> import asciiTUI as tui
  >>> print("%sHello %sWorld%s!%s" % (tui.rgb(r=0), tui.rgb(r=24,g=90,b=123), tui.rgb(style='bg'), '\\033[0m'))
  Hello World!
  >>> # The resulting output is in the form of RGB colors in general. Style as foreground (fg) or background (bg) type. The resulting color depends on the type of console used.

Args:
  `r`     : Red value (0-255)
  `g`     : Green value (0-255)
  `b`     : Blue value (0-255)
  `style` : Color style, either `fg` for foreground or `bg` for background
  """
  style = str(style).lower()
  if not (isinstance(r, int) and isinstance(g, int) and isinstance(b, int)): raise TypeError(f"r, g, b is int, and style is str not r:{type(r).__name__}, g:{type(g).__name__}, b:{type(b).__name__}")
  if ((r < 0) or (r > 255)) or ((g < 0) or (g > 255)) or ((b < 0) or (b > 255)): raise ValueError(f'The values of r, g, b are not up to standard r:{r}, g:{g}, b:{b}')
  if style == 'fg': return f"\u001b[38;2;{r};{g};{b}m"
  elif style == 'bg': return f"\u001b[48;2;{r};{g};{b}m"
  else: raise OptionNotFoundError(f"'{style}' The style type is not found. Only 'fg' (foreground) or 'bg' (background)")

# -- func: make a table ascii for terminal | return [str] -- #
def table(headers:list, data:list, type='table', borders=(['\u2500', '\u2502', '\u250c', '\u2510', '\u2514', '\u2518', '\u252c', '\u2534', '\u251c', '\u2524', '\u253c']))->str:
  """
return: `str`

Example use:
  >>> import asciiTUI as tui
  >>> print(tui.table(
  ...   headers = ['NUM', 'Name'],
  ...   data    = [
  ...               [1, 'Alice'],
  ...               [2, 'Steve'],
  ...             ],
  ...   type    = 'table',
  ...   borders = ['\\u2500', '\\u2502', '\\u250c', '\\u2510', '\\u2514', '\\u2518', '\\u252c', '\\u2534', '\\u251c', '\\u2524', '\\u253c'] # need 11 borders
  ... ))
  ┌─────┬───────┐
  │ NUM │  Name │
  ├─────┼───────┤
  │ 1   │ Alice │
  ├─────┼───────┤
  │ 2   │ Steve │
  └─────┴───────┘

Model types:
  >>> # 'table' Types of table models in general.
  ┌─────┬───────┐
  │ NUM │  Name │
  ├─────┼───────┤
  │ 1   │ Alice │
  ├─────┼───────┤
  │ 2   │ Steve │
  └─────┴───────┘
  >>> # 'table_fancy-grid' Table model type without rows in the data.
  ┌─────┬───────┐
  │ NUM │  Name │
  ├─────┼───────┤
  │ 1   │ Alice │
  │ 2   │ Steve │
  └─────┴───────┘
  >>> # 'tabulate' Tabulate model type with minimal borders.
  NUM │ Name 
  ───────────
  1   │ Alice
  2   │ Steve

Args:
  `headers` : The header list is in the form of a list type. Example: `['NUM', 'Name'] [<col 1>, <col 2>]`
  `data`    : The data list is in the form of a list type. Example: `[[1, 'Alice'], [2, 'Steve']] [<row 1>, <row 2>]`
  `type`    : Table model type (`table` or `table_fancy-grid` or `tabulate`)
  `borders` : Changing borders, default: (`['\\u2500', '\\u2502', '\\u250c', '\\u2510', '\\u2514', '\\u2518', '\\u252c', '\\u2534', '\\u251c', '\\u2524', '\\u253c']`)
  """
  if not (isinstance(headers, list) and isinstance(data, list) and isinstance(borders, list)): raise TypeError(f"type is str, and headers, data, borders is list")
  for item in data:
    if not isinstance(item, list): raise TypeError("data type in it must be a list")
  if len(borders) != 11: raise ValueError('borders length cannot be less or more than 11')
  type = str(type).lower()
  headers = [str(item) for item in headers]
  data = [[str(item) for item in row] for row in data]
  borders = [str(item)[0] for item in borders]
  table_main = ''
  if (type == 'table') or (type == 'table_fancy-grid'):
    column_widths = [max(len(remove_ansi(item)) for item in column) for column in zip(headers, *data)]
    header_line =  borders[2] + borders[6].join(borders[0] * (width + 2) for width in column_widths) + borders[3]+'\n'
    header = borders[1] + borders[1].join(f" {justify(header, width)} " for header, width in zip(headers, column_widths)) + borders[1]+'\n'
    table_main += header_line
    table_main += header
    for i, row in enumerate(data):
      row_line = borders[8] + borders[10].join(borders[0] * (width + 2) for width in column_widths) + borders[9]+'\n'
      row_line_down = borders[4] + borders[7].join(borders[0] * (width + 2) for width in column_widths) + borders[5]
      row_content = borders[1] + borders[1].join(f" {item + ' ' * (width-len(remove_ansi(item)))} " for item, width in zip(row, column_widths)) + borders[1]+'\n'
      table_main += (row_line if i == 0 else '') if type == 'table_fancy-grid' else row_line
      table_main += row_content
    table_main += row_line_down
  elif type == 'tabulate':
    column_widths = [max(len(remove_ansi(header)), max(len(remove_ansi(item)) for item in col) if col else 0) for header, col in zip(headers, zip(*data))]
    header_str = (' '+borders[1]+' ').join([header + ' ' * (width-len(remove_ansi(header))) for header, width in zip(headers, column_widths)])
    table_main += header_str + '\n'
    table_main += borders[0] * len(remove_ansi(header_str)) + '\n'
    count = 0
    for row in data:
      row_str = (' '+borders[1]+' ').join([item + ' ' * (width-len(remove_ansi(item))) for item, width in zip(row, column_widths)])
      table_main += row_str + ('\n' if count <= len(data)-2 else '')
      count += 1
  else:
    raise OptionNotFoundError(f"'{type}' The type is not found.")
  return table_main

# -- func: make progress bar ascii terminal | yield [str] -- #
def progress_bar(type='line', width=50, max=100, bar_progress="#", bar_space=".", bar_box="[]", text="Hello World! - asciiTUI", isdone=" ")->str:
  """
yield: `str`

Example use:
  >>> import asciiTUI as tui
  >>> from time import sleep
  >>> pbg = tui.progress_bar(type='line', width=50, max=100, bar_progress="#", bar_space=".", bar_box="[]")
  >>> for i in pbg:
  ...   print(next(pbg), end='\\r')
  ...   sleep(0.01)
  ... print() # Adding a new line
  [.........................................] 0.2%
  >>> # Progress will increase for 0.01 seconds.

Args:
  `type`         : Type of progress model (`line` or `circle`)
  `width`        : Width length of the progress bar (applies to `line` type)
  `max`          : Maximum progress percentage (applies to `line` type). If it is in the `circle` type then it is a progress time limit
  `bar_progress` : Progress symbol (valid in `line` type)
  `bar_space`    : Space bar symbol (valid in `line` type)
  `bar_box`      : Progress symbol box (valid in `line` type)
  `text`         : Display text in `circle` type
  `isdone`       : Display done in `circle` type if is done
  """
  type, bar_progress, bar_space, bar_box, text, isdone = map(str, [type, bar_progress, bar_space, bar_box, text, isdone])
  if not (isinstance(width, int) and isinstance(max, int)): raise TypeError("width, max is int")
  if len(bar_box) != 2: raise IndexError("bar_box need 2 characters")
  if 'line' in type.lower():
    total = 100
    progress = 0
    bar_start = bar_box[0]
    bar_end = bar_box[-1]
    max = int(max)
    width = int(width)
    width = width - len(str(max)) - 6
    for i in range(max * 10):
      progress += 1
      percent = total * (progress / float(total) / 10)
      filled_width = int(width * (progress // 10) // max)
      bar = f'{bar_progress}' * filled_width + f'{bar_space}' * (width - filled_width)
      yield f"\r{bar_start}{bar}{bar_end} {percent:.1f}%"
  elif 'circle' in type.lower():
    circle_keys = {0: '-', 1: '\\', 2: '|', 3: '/'}
    count = 0
    while max >= 0:
      yield text + circle_keys[count]
      count += 1
      max -= 1
      if count >= 4:
        count = 0
    yield text + isdone
  else:
    raise OptionNotFoundError(f"'{type.lower()}' The type is not found.")

# -- func: make justify func for text | return [str] -- #
def justify(content:str, width:int, make='center', height=50, space=' ', align=False)->str:
  """
return: `str`

Example use:
  >>> import asciiTUI as tui
  >>> print(tui.justify(content=tui.lorem_ipsum, width=50, make='center', height=50, space=' ', align=False))
  Lorem Ipsum is simply dummy text of the printing a
  nd typesetting industry. Lorem Ipsum has been the
  industry's standard dummy text ever since the 1500
  s, when an unknown printer took a galley of type a
  nd scrambled it to make a type specimen book. It h
  as survived not only five centuries, but also the
  leap into electronic typesetting, remaining essent
  ially unchanged. It was popularised in the 1960s w
  ith the release of Letraset sheets containing Lore
  m Ipsum passages, and more recently with desktop p
  ublishing software like Aldus PageMaker including
              versions of Lorem Ipsum.

Args:
  `content` : Content string to be justified
  `width`   : Set the width size
  `make`    : Make the string printed with the center `center` or to the right `right`
  `height`  : Set the height size
  `space`   : Space character
  `align`   : Makes text center align (depending on size in height)
  """
  content, make, space = map(str, [content, make, space])
  align = bool(align)
  if not (isinstance(width, int) or isinstance(height, int)): raise TypeError(f"width, height is int not width:{type(width).__name__}, height:{type(height).__name__}")
  if width <= 1: return content
  content_lines = content.split('\n')
  content_end = ''
  contents = ''
  content_pieces = []
  def cutting_content(main_text, width):
    content_pieces = []
    content_end = str(main_text[(len(main_text) // width) * width:])
    start_index = 0
    while start_index < len(main_text):
      if start_index + width <= len(main_text): content_pieces.append(main_text[start_index:start_index + width])
      start_index += width
    return content_pieces, content_end
  for coline in content_lines:
    if len(remove_ansi(coline)) >= width:
      ctn_list, ctn_end = cutting_content(coline, width)
      for item in ctn_list: content_pieces.append(item)
      content_end = ctn_end
    if 'center' in make.lower():
      if len(remove_ansi(coline)) <= width: contents += space[0] * ((width - len(remove_ansi(coline))) // 2) + coline + space[0] * ((width - len(remove_ansi(coline))) // 2)
      else:
        for item in content_pieces: contents += item + '\n'
        contents += space[0] * ((width - len(remove_ansi(content_end))) // 2) + content_end + space[0] * ((width - len(remove_ansi(content_end))) // 2)
    elif 'right' in make.lower():
      if len(remove_ansi(coline)) <= width: contents += space[0] * (width - len(remove_ansi(coline))) + coline
      else:
        for item in content_pieces: contents += item + '\n'
        contents += space[0] * (width - len(remove_ansi(content_end))) + content_end
    else: raise OptionNotFoundError(f"'{make.lower()}' The type is not found.")
  if align: return ("\n" * height) + contents
  else: return contents

# -- class -- #
# -- func class: splits multiple command arguments on a string | return [None, str] -- #
class cmd_split:

  def __init__(self, esc_char='\\', quotes_char='"', ln_char=';', backslash_char='\\', param_char=' ')->None:
    """
Functions (method): `split_args`, `split_ln`
return: `None`

Example use:
  >>> import asciiTUI as tui
  >>> cs = tui.cmd_split(esc_char='\\', quotes_char='"', ln_char=';', backslash_char='\\', param_char=' ')
  >>> # Other method documentation is in each method..

Args:
  `esc_char`       : Escape character
  `quotes_char`    : Quote character
  `ln_char`        : Line character. To separate and create rows
  `backslash_char` : Backslash character
  `param_char`     : Parameter character. To separate parameters
    """
    esc_char, quotes_char, ln_char, backslash_char, param_char = map(str, [esc_char, quotes_char, ln_char, backslash_char, param_char])
    if (len(esc_char) != 1) or (len(quotes_char) != 1) or (len(ln_char) != 1) or (len(backslash_char) != 1) or (len(param_char) != 1): raise ValueError("All characters only consist of 1 character")
    self.esc_char = esc_char
    self.quotes_char = quotes_char
    self.ln_char = ln_char
    self.backslash_char = backslash_char
    self.param_char = param_char

  def split_args(self, cmd:str) -> list:
    """
return: `list`

Example use:
  >>> command = 'pip install asciiTUI; echo "Hello World!\\""; py'
  >>> cs.split_args(cmd=command)
  [['pip', 'install', 'asciiTUI'], ['echo', 'Hello World!"'], ['py']]

Args:
  `cmd` : main command string
    """
    cmd = str(cmd)
    result = []
    in_quotes = False
    current_cmd = ''
    params = []
    escape_char = False
    for char in cmd:
      if char == self.esc_char and not escape_char: escape_char = True
      elif char == self.quotes_char and not escape_char: in_quotes = not in_quotes
      elif char == self.ln_char and not in_quotes:
        if current_cmd or params:
          result.append(params + [current_cmd])
          current_cmd = ''
          params = []
      elif char == self.param_char and not in_quotes:
        if current_cmd:
          params.append(current_cmd)
          current_cmd = ''
      else:
        if escape_char and char == self.backslash_char:
          current_cmd += char
          escape_char = False
        else:
          current_cmd += char
          escape_char = False
    if current_cmd or params: result.append(params + [current_cmd])
    return result

  def split_ln(self, cmd:str) -> list:
    """
return: `list`

Example use:
  >>> command = 'pip install asciiTUI; echo "Hello World!\\""; py'
  >>> cs.split_ln(cmd=command)
  ['pip install asciiTUI', 'echo "Hello World!""', 'py']

Args:
  `cmd` : main command string
    """
    cmd = str(cmd)
    result = []
    in_quotes = False
    current_cmd = ''
    escape_char = False
    for char in cmd:
      if char == self.esc_char and not escape_char: escape_char = True
      elif char == self.quotes_char and not escape_char:
        in_quotes = not in_quotes
        current_cmd += char
      elif char == self.ln_char and not in_quotes:
        if current_cmd:
          result.append(current_cmd.strip())
          current_cmd = ''
      else:
        current_cmd += char
        escape_char = False
    if current_cmd: result.append(current_cmd.strip())
    return result

# -- Special module for Windows -- #
if _sys.platform == 'win32':

  # -- func: password input function | return [str] -- #
  def pwinput(prompt='', mask='*')->str:
    """
return: `str`

Example use:
  >>> import asciiTUI as tui
  >>> password = tui.pwinput(prompt='Password: ', mask='*'); print(password)
  Password: ***********
  Hello World

Args:
  `prompt` : Appearance of prompt or text.
  `mask`   : As the character mask displayed.
    """
    prompt, mask = map(str, [prompt, mask])
    if len(mask) > 1:
      raise ValueError('Mask argument must be a zero or one character str')
    if mask == '' or _sys.stdin is not _sys.__stdin__:
      return _getpass.getpass(prompt)
    enteredPassword = []
    _sys.stdout.write(prompt)
    _sys.stdout.flush()
    while True:
      key = ord(_getch())
      if key == 13:
        _sys.stdout.write('\n')
        return ''.join(enteredPassword)
      elif key in (8, 127):
        if len(enteredPassword) > 0:
          _sys.stdout.write('\b \b')
          _sys.stdout.flush()
          enteredPassword = enteredPassword[:-1]
      elif 0 <= key <= 31:
        pass
      else:
        char = chr(key)
        _sys.stdout.write(mask)
        _sys.stdout.flush()
        enteredPassword.append(char)

# -- Special module for MacOS or Linux -- #
else:

  # -- func: replacement for the getch() function in the msvcrt module | return [str] -- #
  def getch()->str:
    """
return: `str`

Example use:
  >>> import asciiTUI as tui
  >>> tui.getch() # none args or parameters
  'S'

Info:
  Replacement for the `getch()` function in the msvcrt module because this library does not support anything other than Windows.
    """
    fd = _sys.stdin.fileno()
    old_settings = _termios.tcgetattr(fd)
    try:
      _tty.setraw(_sys.stdin.fileno())
      ch = _sys.stdin.read(1)
    finally:
      _termios.tcsetattr(fd, _termios.TCSADRAIN, old_settings)
    return ch

  # -- func: password input function | return [str] -- #
  def pwinput(prompt='', mask='*')->str:
    """
return: `str`

Example use:
  >>> import asciiTUI as tui
  >>> password = tui.pwinput(prompt='Password: ', mask='*'); print(password)
  Password: ***********
  Hello World

Args:
  `prompt` : Appearance of prompt or text.
  `mask`   : As the character mask displayed.
    """
    prompt, mask = map(str, [prompt, mask])
    if len(mask) > 1:
      raise ValueError('Mask argument must be a zero or one character str')
    if mask == '' or _sys.stdin is not _sys.__stdin__:
      return _getpass.getpass(prompt)
    enteredPassword = []
    _sys.stdout.write(prompt)
    _sys.stdout.flush()
    while True:
      key = ord(getch())
      if key == 13:
        _sys.stdout.write('\n')
        return ''.join(enteredPassword)
      elif key in (8, 127):
        if len(enteredPassword) > 0:
          _sys.stdout.write('\b \b')
          _sys.stdout.flush()
          enteredPassword = enteredPassword[:-1]
      elif 0 <= key <= 31:
        pass
      else:
        char = chr(key)
        _sys.stdout.write(mask)
        _sys.stdout.flush()
        enteredPassword.append(char)

# test functions
if __name__ == '__main__':
  import time
  table_type = 'table'
  print(justify('\033[32masciiTUI \033[36mTEST \033[1;33mFUNCTIONS\033[0m', 50))
  print('=' * 50)
  print(table(
              headers = ['\033[1;34mNUM\033[0m', '\033[1;32mNames\033[0m'],
              data    = [
                [1, 'Alice'],
                [2, 'Steve'],
              ],
              type    = table_type,
              borders = ['\u2500', '\u2502', '\u250c', '\u2510', '\u2514', '\u2518', '\u252c', '\u2534', '\u251c', '\u2524', '\u253c']
  ))
  pw = pwinput('Password: ', '\u2022')
  print(pw)
  pbg = progress_bar(max=2)
  for i in pbg:
    print(
      rgb(212,53,24)+
      next(pbg)+
      rgb(),
      end='\r'
    )
    time.sleep(0.1)
  print()
  print(justify(lorem_ipsum, 50))
  cmd = input('Enter some comm: ')
  init_cmd = cmd_split()
  print(init_cmd.split_args(cmd))
  print(init_cmd.split_ln(cmd))
  text = '\033[32;4masciiTUI\033[0m'
  print(text, remove_ansi(text))
  # end
  exit()