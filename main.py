import numpy as np
import matplotlib.pyplot as plt
import tqdm as tqdm
import argparse
import json


def LIF_model_eulers_method(vm, vr, tm, isyn, cm, t, ts, tr, dt):
    """
    Uses Euler's method
    :param vm: membrane voltage
    :param vr: (constant) resting potential of neuron; voltage of neuron at "rest" (volts)
    :param taum: (constant) decay time of neuron; how fast neuron leaks charge (seconds)
    :param isyn: either the constant or the calculated? (amps)
    :param cm: (constant) membrane capacitance; how much charge neuron can hold (farads)
    :param t: time (seconds)
    :param ts: time of last spike (seconds)
    :param tr: (constant) refactor period (seconds)
    :param dt: delta t; step size
    :return: membrane voltage at next step
    """
    heaviside_value = heaviside_step_function(t, ts, tr)
    return vm + dt * ((-((vm-vr)/tm) + isyn/cm)*heaviside_value)


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
    print("t",t)
    print("t0", t0)
    print(-(t-t0)/tausyn)
    print("val3", np.exp(-(t-t0)/tausyn))
    return w*g*(vrev-vm)*((t-t0)/tausyn)*np.exp(-(t-t0)/tausyn)


# Experiment 5 Taylor Series approximation of e^x centered at 0
def bonus(x):
    return 1 + x + (x**2)/2 + (x**3)/6 + (x**4)/24 + (x**5)/120 + (x**6)/720 + (x**7)/5040 + (x**8)/40320 + (x**9)/362880 + (x**10)/3628000


if __name__ == "__main__":
    print("Hello World")

    parser = argparse.ArgumentParser("Program to model the current of a neuron")
    parser.add_argument('m', type=str, help="The value of m; can either be spike or current")
    parser.add_argument('s', type=float, help="The value of s; amount of time to run the simulation in milliseconds")
    parser.add_argument('--spike_rate', type=int, help="input spike rate in Hz")
    parser.add_argument('--current', default = 1, type=float, help="input current in nanoamps")
    # Parse the command line arguments
    args = parser.parse_args()

    mode = args.m
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
    #t_r = t_r/1000

    # These will store the time and membrane voltage
    time = 0
    time_array = [time]
    membrane_voltage = v_r
    membrane_voltage_array = [membrane_voltage]

    ts = 0

    # Spike mode
    if mode == "spike":
        print("SPIKE")
        spike_rate = args.spike_rate
        spike_times = np.arange(0, sim_time, sim_time/spike_rate)

        while time < sim_time:
            time += dt
            #problem here
            i_syn = alpha_synapse_model(1, g_bar, v_rev, membrane_voltage, time, ts, tao_syn)
            print("Isyn =", i_syn)
            print("val1", dt*((-((membrane_voltage-v_r)/tao_m)) ))
            print("val2", i_syn/c_m)
            membrane_voltage += dt*((-((membrane_voltage-v_r)/tao_m) + i_syn/c_m)*heaviside_step_function(time, ts, t_r))
            print("Step Function", heaviside_step_function(time, ts, t_r))
            print("Membrane Voltage", membrane_voltage)
            if membrane_voltage > v_thr:
                print("Membrane Voltage 2", membrane_voltage)
                #membrane_voltage_array.append(membrane_voltage)
                membrane_voltage = v_r
                ts = time
            membrane_voltage_array.append(membrane_voltage)
            print("Time", time)
            time_array.append(time)


    # Current mode
    if mode == "current":
        #membrane_voltage_array[0]=v_spike
        current = args.current/1000000000
        while time <= sim_time:
            time += dt
            i_syn = current
            membrane_voltage += (dt*((-((membrane_voltage-v_r)/tao_m) + i_syn/c_m)*heaviside_step_function(time, ts, t_r)))
            print("Membrane Voltage", membrane_voltage)
            if membrane_voltage > v_thr:
                membrane_voltage = v_r
                membrane_voltage_array.append(v_spike)
                #print("Membrane Voltage 2", membrane_voltage)
                ts = time
            else:
                membrane_voltage_array.append(membrane_voltage)
            print("Time", time)
            print("val1", dt * ((-((membrane_voltage - v_r) / tao_m))))
            print("val2", i_syn / c_m)
            time_array.append(time)


# Plot it
# print("Membrane Voltage Array", membrane_voltage_array)
plt.plot(time_array, membrane_voltage_array, color='r')
plt.title("Group 8 Membrane Potential Track", size=16)
plt.xlabel("Time (msec)", size=16)
plt.ylabel("V_m (volt)", size=16)
plt.show()
