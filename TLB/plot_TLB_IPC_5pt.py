# Advanced Computer Architecture, 2019-2020, 3.4.37.8
# 1st Assignment

# Plotting Code (TLB)
# You shouldn't run this directly, run plotter_TLB.sh instead.
# Dependencies: python, python-matplotlib

import sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

x_Axis = []
ipc_Axis = []
mpki_Axis = []

index = 0
tlb_entries_base = 8
tlb_assoc_base = 4
tlb_psize_base = 4096

for outFile in sys.argv[1:]:
    fp = open(outFile)
    line = fp.readline()
    while line:
        tokens = line.split()
        if (line.startswith("Total Instructions: ")):
            total_instructions = int(tokens[2])
        elif (line.startswith("IPC:")):
            ipc = float(tokens[1])
        elif (line.startswith("  Data Tlb")):
            sizeLine = fp.readline()
            tlb_entries = int(sizeLine.split()[1])
            bsizeLine = fp.readline()
            tlb_psize = int(bsizeLine.split()[2])
            assocLine = fp.readline()
            tlb_assoc = int(assocLine.split()[1])
        elif (line.startswith("Tlb-Total-Misses")):
            tlb_total_misses = int(tokens[1])
            tlb_miss_rate = float(tokens[2].split('%')[0])
            mpki = tlb_total_misses / (total_instructions / 1000.0)

        line = fp.readline()

    fp.close()

    index += (tlb_entries / tlb_entries_base) - 1
    index += (tlb_assoc / tlb_assoc_base) - 1
    index += (tlb_psize / tlb_psize_base) - 1

    while index > 0:
        ipc *= 95/100
        index -= 1

    tlbConfigStr = '{}.{}.{}B'.format(tlb_entries,tlb_assoc,tlb_psize)
    print(tlbConfigStr)
    x_Axis.append(tlbConfigStr)
    ipc_Axis.append(ipc)
    mpki_Axis.append(mpki)

print(x_Axis)
print(ipc_Axis)
print(mpki_Axis)

fig, ax1 = plt.subplots()
ax1.grid(True)
ax1.set_xlabel("TLB Size.Associativity.Page Size")

xAx = np.arange(len(x_Axis))
ax1.xaxis.set_ticks(np.arange(0, len(x_Axis), 1))
ax1.set_xticklabels(x_Axis, rotation=45)
ax1.set_xlim(-0.5, len(x_Axis) - 0.5)
ax1.set_ylim(min(ipc_Axis) - 0.05 * min(ipc_Axis), max(ipc_Axis) + 0.05 * max(ipc_Axis))
ax1.set_ylabel("$IPC$")
line1 = ax1.plot(ipc_Axis, label="IPC", color="red",marker='x')

ax2 = ax1.twinx()
ax2.xaxis.set_ticks(np.arange(0, len(x_Axis), 1))
ax2.set_xticklabels(x_Axis, rotation=45)
ax2.set_xlim(-0.5, len(x_Axis) - 0.5)
ax2.set_ylim(min(mpki_Axis) - 0.05 * min(mpki_Axis), max(mpki_Axis) + 0.05 * max(mpki_Axis))
ax2.set_ylabel("$MPKI$")
line2 = ax2.plot(mpki_Axis, label="TLB_MPKI", color="green",marker='o')

lns = line1 + line2
labs = [l.get_label() for l in lns]

plt.title("IPC vs MPKI, 5% IPC Reduction")
lgd = plt.legend(lns, labs)
lgd.draw_frame(False)
plt.savefig("TLB.png",bbox_inches="tight")
