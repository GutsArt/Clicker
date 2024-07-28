from pynput.keyboard import Listener, Key, KeyCode


toggle_key = KeyCode(char='p')
exit_key = Key.esc

clicking = False
exit_flag = False