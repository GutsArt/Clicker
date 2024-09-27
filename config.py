from pynput.keyboard import Listener, Key, KeyCode

click_all, click_max = 0, 500

toggle_key = KeyCode(char='+')
exit_key = Key.esc

clicking = False
exit_flag = False