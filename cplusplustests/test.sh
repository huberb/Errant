#!/bin/bash

g++ binary_test.cpp -o binary_test && 
echo "first program:" &&
./binary_test && 
python2 fill_up.py && 
echo "second program:" &&
./binary_test_filled_up
