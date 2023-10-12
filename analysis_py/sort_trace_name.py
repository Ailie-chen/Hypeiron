# Splitting the filenames and extracting the two numbers
filenames = [
"450.soplex-247B",
"471.omnetpp-188B",
"483.xalancbmk-127B",
"401.bzip2-226B",
"623.xalancbmk_s-592B",
"657.xz_s-2302B",
"482.sphinx3-1297B",
"623.xalancbmk_s-10B",
"621.wrf_s-6673B",
"605.mcf_s-994B",
"619.lbm_s-4268B",
"623.xalancbmk_s-700B",
"607.cactuBSSN_s-4004B",
"619.lbm_s-2677B",
"605.mcf_s-1644B",
"619.lbm_s-2676B",
"473.astar-359B",
"602.gcc_s-2226B",
"605.mcf_s-665B",
"605.mcf_s-782B",
"607.cactuBSSN_s-3477B",
"429.mcf-51B",
"620.omnetpp_s-141B",
"644.nab_s-12459B",
"605.mcf_s-472B",
"483.xalancbmk-716B",
"605.mcf_s-1554B",
"473.astar-42B",
"429.mcf-192B",
"620.omnetpp_s-874B",
"459.GemsFDTD-1320B",
"429.mcf-22B",
"602.gcc_s-1850B",
"453.povray-252B",
"482.sphinx3-417B",
"429.mcf-217B",
"605.mcf_s-484B",
"605.mcf_s-1536B",
"602.gcc_s-2375B",
"435.gromacs-111B",
"429.mcf-184B",
"403.gcc-17B",
"649.fotonik3d_s-10881B",
"607.cactuBSSN_s-2421B",
"450.soplex-92B",
"459.GemsFDTD-765B",
"459.GemsFDTD-1169B",
"401.bzip2-7B",
"434.zeusmp-10B",
"435.gromacs-134B",
"605.mcf_s-1152B",
"623.xalancbmk_s-325B"
]

# Extracting the two numbers from each filename
def extract_numbers(filename):
    parts = filename.split('-')
    first_number = int(parts[0].split('.')[0])
    second_number = int(parts[1].rstrip('B'))
    return (first_number, second_number)

# Sorting the filenames
sorted_filenames = sorted(filenames, key=extract_numbers)

for trace_name in sorted_filenames:
    print(f"\"{trace_name}\",")
