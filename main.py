import numpy as np
import matplotlib.pyplot as plt
import tqdm as tqdm
import argparse
import json

def LIF_model_eulers_method(prev, vm, vr, tm, isyn, cm, t, ts, tr, dt):
    """
    Uses Euler's method
    :param prev: previous membrane voltage
    :param vm: membrane voltage
    :param vr: (constant) resting potential of neuron; voltage of neuron at "rest" (volts)
    :param taum: (constant) decay time of neuron; how fast neuron leaks charge (seconds)
    :param isyn: either the constant or the calculated?
    :param cm: (constant) membrane capacitance; how much charge neuron can hold (farads)
    :param t: time (seconds)
    :param ts: time of last spike (seconds)
    :param tr: (constant) refactor period (seconds)
    :param dt: delta t; step size
    :return: membrane voltage at next step
    """
    heaviside_value = heaviside_step_function(t, ts, tr)
    return prev + dt * ((-((vm-vr)/tm) + isyn/cm)*heaviside_value)


def heaviside_step_function(t, ts, tr):
    """
    Returns either 0 or 1
    :param t: time (seconds)
    :param ts: time of last spike
    :param tr: (constant) refactory period
    :return: either 0 or 1
    """
    if (t - ts - tr) <= 0:
        return 0
    else:
        #set ts to last spike time
        tSpike = t
        return 1


def alpha_synapse_model(w, g, vrev, vm, t, t0, tausyn):
    """
    Determines the spike's synaptic current
    :param w: (constant) weight of synapse
    :param g: (constant) maximum conductance of synapse (siemens)
    :param vrev: (constant) reverse potential (volts)
    :param vm: membrane voltage of postsynaptic neuron (volts)
    :param t: current time of simulation (seconds)
    :param t0: time spike started (seconds)
    :param tausyn: (constant) decay time of alpha synapse (seconds)
    :return: isyn
    """
    return w*g*(vrev-vm)*((t-t0)/tausyn)*np.exp(-(t-t0)/tausyn)

if __name__ == "__main__":
    print("Hello World")

    parser = argparse.ArgumentParser("Program to model the current of a neuron")
    parser.add_argument('m', type=str, help="The value of m; can either be spike or current")
    parser.add_argument('s', type=float, help="The value of s; amount of time to run the simulation in milliseconds")
    parser.add_argument('--spike_rate', type=int, help="input spike rate in Hz")
    parser.add_argument('--current',default = 1, type=float, help="input current in nanoamps")
    # Parse the command line arguments
    args = parser.parse_args()
    dt = 0.001
    mode = args.m

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


    if mode != "spike" and mode != "current":
        print("Invalid mode")
        exit(1)

    # Constants
    try:
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
        print("File not found")
    except PermissionError:
        print("Permission denied")

    print(v_r, v_thr, v_spike, v_rev, tao_m, tao_syn, c_m, g_bar, t_r, w, dt)

    # Simulation time
    sim_time = args.s/1000

    # These will store the time and membrane voltages?
    time = [0]
    membrane_voltage = [v_r]
    # not sure if correct
    vm = 0
    tSpike = 0
    # Spike mode
    if mode == "spike":
        spike_rate = args.spike_rate
        while time[-1] < sim_time:
            time.append(time[-1] + dt)
            print("here spike")
            i_syn = alpha_synapse_model(w, g_bar, v_rev, membrane_voltage[-1], time[-1], 0, tao_syn)
            membrane_voltage.append(LIF_model_eulers_method(membrane_voltage[-1], vm, v_r, tao_m, i_syn, c_m, time[-1], tSpike, t_r, dt))

    # Current mode
    if mode == "current":
        current = args.current
        while time[-1] < sim_time:
            time.append(time[-1] + dt)
            i_syn = current
            print("here")
            membrane_voltage.append(LIF_model_eulers_method(membrane_voltage[-1], vm, v_r, tao_m, i_syn, c_m, time[-1], tSpike, t_r, dt))

# Plot it
plt.plot(time, membrane_voltage, color='r')
plt.title("Group 8 Membrane Potential Track", size=16)
plt.xlabel("Time (msec)", size=16)
plt.ylabel("V_m (volt)", size=16)
plt.show()
