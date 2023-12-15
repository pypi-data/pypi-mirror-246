



import clipboard




def get():
    return clipboard.paste()

def set(value):
    return clipboard.copy(value)






