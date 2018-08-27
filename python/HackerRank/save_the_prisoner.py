#!/bin/python3

import math
import os
import random
import re
import sys

# Complete the saveThePrisoner function below.
def saveThePrisoner(people, candy, start):
    remaining = candy
    if candy > people:
        remaining = candy % people
    
    if start > 1:
        start -= 1
    else:
        start = people

    last = start + remaining
    if last > people:
        last -= people
    return last

if __name__ == '__main__':

    lines = []

    f = open('save_the_prisoner2.txt',"r")
    lines = f.readlines()
    f.close()

    #print(lines)

    for line in lines:
        #print(line)
        n,m,s = line.split(" ")
        result = saveThePrisoner(int(n), int(m), int(s))
        print(result)