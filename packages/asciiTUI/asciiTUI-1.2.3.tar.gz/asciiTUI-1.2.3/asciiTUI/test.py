import __init__ as tui

from __init__ import remove_ansi

from TextJustify import justify_text

long_text_ls = ['\033[32mHello \033[31mWorld!\033[0m' for i in range(10)]
result = ' '.join(long_text_ls)


print(justify_text(tui.lorem_ipsum, 40, 'center'))
print(tui.justify(tui.lorem_ipsum, 40, 'center'))
print('='*40)