def textPrettier():
  try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
  except:
    pass

def place_value(number): 
    return ("{:,}".format(number))

def sliceTextDate(strDate):
  return strDate[:10]