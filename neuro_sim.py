#Group 8: Gayoon Nam, Kristen Averett, Cassidy McDonald, Lora Elliott, Lynn Nguyen

# Many print lines which were used for debugging are commented out.

import numpy as np
import matplotlib.pyplot as plt
import argparse
import json

# Not used
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
    :return: I_syn
    """
    # print("t",t)
    # print("t0", t0)
    # print(-(t-t0)/tausyn)
    # print("val3", np.exp(-(t-t0)/tausyn))
    return w*g*(vrev-vm)*((t-t0)/tausyn)*np.exp(-(t-t0)/tausyn)


def e(x):
    """
    10th order Taylor series approximation of e^x centered at 0 for Experiment 5
    :param x: input value
    :return: approximated value
    """
    return 1 + x + (x**2)/2 + (x**3)/6 + (x**4)/24 + (x**5)/120 + (x**6)/720 + (x**7)/5040 + (x**8)/40320 + (x**9)/362880 + (x**10)/3628000


def alpha_synapse_model_bonus(w, g, vrev, vm, t, t0, tausyn):
    """
    Determines the spike's synaptic current using a 10th order Taylor series
    approximation of e^x centered at 0 instead of the exponential term in Equation 3
    :param w: (constant) weight of synapse
    :param g: (constant) maximum conductance of synapse (siemens)
    :param vrev: (constant) reverse potential (volts)
    :param vm: membrane voltage of postsynaptic neuron (volts)
    :param t: current time of simulation (seconds)
    :param t0: time spike started (seconds)
    :param tausyn: (constant) decay time of alpha synapse (seconds)
    :return: I_syn
    """
    return w*g*(vrev-vm)*((t-t0)/tausyn)*e(-(t-t0)/tausyn)


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Program to model the current of a neuron")
    parser.add_argument('m', type=str, help="The value of m; can either be spike or current")
    parser.add_argument('s', type=float, help="The value of s; amount of time to run the simulation in milliseconds")
    parser.add_argument('--spike_rate', default=50, type=int, help="input spike rate in Hz")
    parser.add_argument('--current', default = 1, type=float, help="input current in nanoamps")
    parser.add_argument('--bonus', default=0, type=int, help="toggle to 1 to use Taylor series approximation of e^x instead of exponential term")
    # Parse the command line arguments
    args = parser.parse_args()

    mode = args.m
    if mode != "spike" and mode != "current":
        print("Invalid mode")
        exit(1)

    bonus = args.bonus
    if bonus != 0 and bonus != 1:
        print("Invalid bonus mode toggle")
        exit(1)

    # Constants
    try:
        # Change to correct file path
        f = open('/Users/gynam/IdeaProjects/CSC 2262 HW 4/config.json', 'r')
        data = json.load(f)
        # print(data)
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

    # print(v_r, v_thr, v_spike, v_rev, tao_m, tao_syn, c_m, g_bar, t_r, w, dt)

    # Simulation time
    sim_time = args.s/1000

    # These will store the times and membrane voltages
    time = 0
    time_array = [time]
    membrane_voltage = v_r
    membrane_voltage_array = [membrane_voltage]

    ts = 0

    # Spike mode
    if mode == "spike":
        # print("SPIKE")
        firstSpike = True
        spike_rate = args.spike_rate
        spike_times = np.arange(0, sim_time, sim_time/spike_rate)
        time_between_spikes = (spike_times[1]-spike_times[0])*10
        # print(spike_times)

        while time <= sim_time:
            time += dt
            t0 = 0
            #problem here (SOLVED)
            i_syn = alpha_synapse_model(w, g_bar, v_rev, membrane_voltage, time, ts, tao_syn)
            if bonus == 1:
                i_syn = alpha_synapse_model_bonus(w, g_bar, v_rev, membrane_voltage, time, ts, tao_syn)
            #print("Isyn =", i_syn)
            #print("val1", dt*((-((membrane_voltage-v_r)/tao_m))))
            #print("val2", i_syn/c_m)
            membrane_voltage += dt*((-((membrane_voltage-v_r)/tao_m) + i_syn/c_m)*heaviside_step_function(time, ts, t_r))
            #print("Step Function", heaviside_step_function(time, ts, t_r))
            #print("Membrane Voltage", membrane_voltage)
            if time-ts-t_r > time_between_spikes:
                ts = time
                membrane_voltage = v_spike
            if membrane_voltage > v_thr:
                #print("Membrane Voltage 2", membrane_voltage)
                membrane_voltage = v_spike
                membrane_voltage_array.append(membrane_voltage)
                ts = time + dt
                membrane_voltage = v_r
                # print("Current Time: ", time, "Start Time of Last Input Spike: ", t0)
            else:
                membrane_voltage_array.append(membrane_voltage)
            # print("Time", time)
            # print("TS", ts)
            time_array.append(time*1000)

    # Current mode
    if mode == "current":
        #membrane_voltage_array[0]=v_spike
        current = args.current/1000000000
        while time <= sim_time:
            time += dt
            i_syn = current
            membrane_voltage += (dt*((-((membrane_voltage-v_r)/tao_m) + i_syn/c_m)*heaviside_step_function(time, ts, t_r)))
            # print("Membrane Voltage", membrane_voltage)
            if membrane_voltage > v_thr:
                membrane_voltage = v_r
                membrane_voltage_array.append(v_spike)
                # print("Membrane Voltage 2", membrane_voltage)
                ts = time
            else:
                membrane_voltage_array.append(membrane_voltage)
            # print("Time", time)
            # print("val1", dt * ((-((membrane_voltage - v_r) / tao_m))))
            # print("val2", i_syn / c_m)
            time_array.append(time*1000)

# print(spike_times)
# print("Membrane Voltage Array", membrane_voltage_array)
# Plot it
plt.plot(time_array, membrane_voltage_array, color='r')
plt.title("Group 8 Membrane Potential Track", size=16)
plt.xlabel("Time (msec)", size=16)
plt.ylabel("V_m (volt)", size=16)
plt.show()
