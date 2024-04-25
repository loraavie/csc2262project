#import numpy as np
#import matplotlib.pyplot as plt
#import tqdm as tqdm
import argparse
import json

def equation1(vm, vr, tm, iSyn, cm, t, ts, tr, delta):
    eq1 = (-1*(vm - vr)/tm + (iSyn/cm)) * delta(t-ts-tr)
    return eq1

def equation2(deltaX):
    if(deltaX<=0):
        return 0
    else:
        return 1

def alphaSynapseModel(w, g, vRev, vm, t, t0, tSyn, exp):
    equation = w*g*(vRev - vm)*((t-t0)/tSyn)*exp(-(t-t0)/tSyn)
if __name__ == "__main__":
    print("Hello World")

    #initializing vals to be read from the json file
    v_r = 0
    v_th = 0
    v_spike = 0
    v_rev = 0
    tao_m = 0
    tao_syn = 0
    c_m = 0
    g_bar = 0
    t_r = 0
    w = 0
    dt = 0


    parser = argparse.ArgumentParser("Program to model the current of a neuron")
    
    #mode
    parser.add_argument("m", type=str, help="The value of m")
    parser.add_argument("s", type=float, help="Simulation time")
    parser.add_argument("--current", type=float, default=1, help="Current")
    parser.add_argument("--spike", type=float, default=1, help="Spike rate")
    mode = parser.parse_args().m
    if(mode!="spike" and mode!="current"):
        print("Invalid mode")
        exit(1)
    #simulation time

    sim_time = parser.parse_args().s

    #spike rate
    if(mode=="spike"):
        spike_rate = parser.parse_args().spike

    #current
    if(mode=="current"):
        current = parser.parse_args().current
    
    #reading json file plus error handling
    try:
        #change to file path on your computer
        f = open('\\Users\\loraa\\Downloads\\CSC2262Project\\config.json', 'r')
        data = json.load(f)
        print(data)
        v_r = data["v_r"]
        v_thr = data["v_thr"]
        v_spike = data["v_spike"]
        v_rev = data["v_rev"]
        tao_m = data["tao_m"]
        tao_syn = data["tao_syn"]
        c_m = data["c_m"]
        g_bar = data["g_bar"]
        t_r = data["t_r"]
        w = data["w"]
        dt = data["dt"]
        f.close()

    except FileNotFoundError:
        print("File not found. Please check the file path.")
    except PermissionError:
        print("Permission denied. You don't have the necessary permissions to read the file.")
    else:
        print("other error")

    print(v_r, v_th, v_spike, v_rev, tao_m, tao_syn, c_m, g_bar, t_r, w, dt)
