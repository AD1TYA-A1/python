#   Sets are lke same to same as used in Mathematics
# Sets are collection of well defined objects tha are not repeating.Set do not contain more than one same value

# Sets arenot Indexed i.e, We cannot access data in a set using index
# Sets in pyhton have no way to change elements inside it you may replace but not change
s = {1, 2, 3, 4, 5}
print(type(s))  # <class 'set'>
# Here is how to create an EMPTY SET
# ASKED IN INTERVIEWS
emptSet = set()
print(type(emptSet))  # <class 'set'>

# WE use set when we have a data where we have multiple same value but we want to have thtdata only one time
set = {12, 3, 3, 3, 3, 45, 6, 5, 3, 90}  # {3, 5, 6, 90, 12, 45}
print(set)

# POINT TO NOTE HERE IS THAT A SET DOESN'T MAINTAIN ORDER!!!
# set = {12, 3, 3, 3, 3, 45, 6, 5, 3, 90} ----------> {3, 5, 6, 90, 12, 45}
# WE CAN SEE "3" AT FRST THEN "5" AT SECOND "12" AT 4TH INDEX


#   FOR ORDER WE USE LIST
#   FOR ORDER WE USE LIST
#   FOR ORDER WE USE LIST


#   METHODS IN SETS
st = {
    12,
    56,
    "Admin",
    True,
}  
print(st, type(st))
print(len(st))
st.add("Boolean")
st.add("AdminHun")
st.add(44)
st.add(False)
st.add(True)

# s.remove(1)
print(st, type(st))
print(len(st))
