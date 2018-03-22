#!/bin/bash

g++ main.cpp -o main
python2 inject_pdfs.py ./main
chmod +x main_injected_1
chmod +x main_injected_2
