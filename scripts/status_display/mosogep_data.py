# int->(str,str) map
# key is floor number
# values are pairs of (washer, drier) type of floor
# valid values: 
# - "new" for new whirlpool devices
# - "old_1" for old devices with 1 line displays
# - "old_2" for old devices with 2 line displays
# - "" for no device
# there are currently 5 types of machines working:
# - new washers
# - new driers
# - old washeres with 1 line displays
# - old washeres with 2 line displays
# - old driers with 2 line displays

device_types = {
   3: ("new", "new"),
   5: ("new", "new"),
   6: ("old_1", ""),
   7: ("new", "new"),
   9: ("old_1", "new"),
   10: ("old_1", ""),
   11: ("old_2", "old_2"),
   13: ("new", "new"),
   15: ("new", "new"),
   16: ("new", ""),
   17: ("old_2", "old_2"),
}

def get_types_for_floor(floor_num):
   return device_types.get(floor_num, ("",""))

def floor_has_device(floor_num):
   return floor_num in device_types
