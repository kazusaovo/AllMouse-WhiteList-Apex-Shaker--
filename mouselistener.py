from pynput import mouse

mousel = 0
mouser = 0

def on_click(x, y, button, pressed):
    global mousel, mouser
    if button == mouse.Button.left:
        mousel = 1 if pressed else 0
    elif button == mouse.Button.right:
        mouser = 1 if pressed else 0

listener = mouse.Listener(on_click=on_click)
listener.start()

