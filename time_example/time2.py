# wait for 10 seconds to pass and then for 10 more and quit

from time import time

t0 = time()
print("start counting", t0)
passed = False
while True:
    # havingConversation() # eg. check buttons
    if time() == t0+10 and not passed:
        # ten seconds have passed
        print("ten seconds have passed")
        passed = True
    elif time() == t0+20:
        print("quitting because 20 seconds have passed")
        break # ends loop
