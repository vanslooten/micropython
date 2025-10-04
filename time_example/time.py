# wait for 10 seconds to pass

from time import time

t0 = time()
print("start counting", t0)
passed = False
while True:
    # havingConversation()
    if time() == t0+10 and not passed:
        # ten seconds have passed
        print("ten seconds have passed")
        passed = True
