import numpy as np
import matplotlib.pyplot as plt
import tqdm as tqdm
import argparse
import json

if __name__ == "__main__":
    # print("Hello World")
    # parser = argparse.ArgumentParser("Program to model the current of a neuron")
    # #mode
    # parser.add_argument("m", type=str, help="The value of m")
    # mode = parser.parse_args().m
    # if(mode!="spike" and mode!="current"):
    #     print("Invalid mode")
    #     exit(1)
    # #simulation time
    # parser.add_argument("s", type=float, help="Simulation time")
    # sim_time = parser.parse_args().s

    # #spike rate
    # if mode == "spike":
    #     parser.add_argument("r", type=float, help="Spike rate")
    #     spike_rate = parser.parse_args().r

    # #current
    # if mode == "current":
    #     parser.add_argument("i", type=float, help="Current")
    #     current = parser.parse_args().i
    
    
    #reading vals from json file
    # with open("config.json", 'r') as file:
    #     data = json.load(file)
    # print(data)
    try:
        f = open('config.json')
    # Proceed with reading or processing the file
    except FileNotFoundError:
        print("File not found. Please check the file path.")
    except PermissionError:
        print("Permission denied. You don't have the necessary permissions to read the file.")
    else:
        print("other error")

