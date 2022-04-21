#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

flag = open(f"{os.path.abspath(os.path.dirname(__file__))}/.passwd", "r").read()

print(flag)