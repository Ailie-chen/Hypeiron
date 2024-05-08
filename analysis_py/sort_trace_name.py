# Splitting the filenames and extracting the two numbers
filenames = [
"605.mcf_s-1536B",
"628.pop2_s-17B",
"619.lbm_s-3766B",
"603.bwaves_s-2609B",
"602.gcc_s-2226B",
"649.fotonik3d_s-1176B",
"649.fotonik3d_s-10881B",
"602.gcc_s-734B",
"654.roms_s-293B",
"654.roms_s-523B",
"619.lbm_s-4268B",
"605.mcf_s-1152B",
"657.xz_s-2302B",
"605.mcf_s-1644B",
"625.x264_s-20B",
"619.lbm_s-2676B",
"649.fotonik3d_s-7084B",
"654.roms_s-1390B",
"607.cactuBSSN_s-4004B",
"654.roms_s-1613B",
"607.cactuBSSN_s-3477B",
"605.mcf_s-665B",
"654.roms_s-1007B",
"621.wrf_s-6673B",
"627.cam4_s-490B",
"603.bwaves_s-1740B",
"619.lbm_s-2677B",
"620.omnetpp_s-874B",
"623.xalancbmk_s-165B",
"605.mcf_s-484B",
"654.roms_s-294B",
"621.wrf_s-8065B",
"623.xalancbmk_s-202B",
"603.bwaves_s-891B",
"605.mcf_s-1554B",
"607.cactuBSSN_s-2421B",
"654.roms_s-1070B",
"603.bwaves_s-2931B",
"602.gcc_s-1850B",
"649.fotonik3d_s-8225B",
"605.mcf_s-994B",
"605.mcf_s-472B",
"605.mcf_s-782B",
"623.xalancbmk_s-10B",
"620.omnetpp_s-141B",
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
