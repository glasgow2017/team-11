
# coding: utf-8

# In[22]:

import time
import os
import random


# In[23]:

fn = 'test_shake.txt'
with open(fn, 'r') as f:
    data = f.readlines()

print(len([x for x in data if len(x) > 30 and len(x) < 50]))


# In[24]:

ns = [
    'This commission ',
    'This version ',
    'This piece of new code ',
    'This new piece of code ',
    'This '
]

actions = [
    'changed the text file and ',
    'removed some lines from text file, e.g. ',
    'is not really useful, but it removes ',
    'is from a robot -> '
]

random.choice(ns)


# In[25]:

def auto_submission():
    mess = random.choice(ns)
    mess += random.choice(actions)
    mess += generate_comment(data)
    print mess
    os.system('git pull')
    time.sleep(5)
    os.system("git add *")
    time.sleep(5)
    os.system("git commit -m '{mess}'".format(mess=mess))
    time.sleep(5)
    os.system("git push")


def generate_comment(data):
    fn = 'test_shake.txt'
    with open(fn, 'r') as f:
        data = f.readlines()

    data = [x for x in data if len(x) > 30 and len(x) < 50]

    message = data.pop().strip()
    with open(fn, 'wb') as f:
        f.writelines(data)
    f.close()
    return message


# In[ ]:

for i in range(100):
    rnd = random.randint(60, 300)
    print i, rnd
    time.sleep(rnd)
    auto_submission()


# In[ ]:
