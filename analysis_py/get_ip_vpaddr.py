test_names = [
        "401.bzip2-277B.champsimtrace.xz",
        "403.gcc-17B.champsimtrace.xz",
        "410.bwaves-1963B.champsimtrace.xz",
        "410.bwaves-2097B.champsimtrace.xz",
        "429.mcf-184B.champsimtrace.xz",
        "429.mcf-192B.champsimtrace.xz",
        "429.mcf-217B.champsimtrace.xz",
        "429.mcf-22B.champsimtrace.xz",
        "429.mcf-51B.champsimtrace.xz",
        "433.milc-127B.champsimtrace.xz",
        "433.milc-274B.champsimtrace.xz",
        "433.milc-337B.champsimtrace.xz",
        "434.zeusmp-10B.champsimtrace.xz",
        "436.cactusADM-1804B.champsimtrace.xz",
        "437.leslie3d-134B.champsimtrace.xz",
        "437.leslie3d-149B.champsimtrace.xz",
        "437.leslie3d-232B.champsimtrace.xz",
        "437.leslie3d-265B.champsimtrace.xz",
        "437.leslie3d-271B.champsimtrace.xz",
        "437.leslie3d-273B.champsimtrace.xz",
        "450.soplex-247B.champsimtrace.xz",
        "450.soplex-92B.champsimtrace.xz",
        "459.GemsFDTD-1169B.champsimtrace.xz",
        "459.GemsFDTD-1211B.champsimtrace.xz",
        "459.GemsFDTD-1320B.champsimtrace.xz",
        "459.GemsFDTD-1418B.champsimtrace.xz",
        "459.GemsFDTD-1491B.champsimtrace.xz",
        "459.GemsFDTD-765B.champsimtrace.xz",
        "462.libquantum-1343B.champsimtrace.xz",
        "462.libquantum-714B.champsimtrace.xz",
        "470.lbm-1274B.champsimtrace.xz",
        "471.omnetpp-188B.champsimtrace.xz",
        "473.astar-359B.champsimtrace.xz",
        "473.astar-42B.champsimtrace.xz",
        "481.wrf-1254B.champsimtrace.xz",
        "481.wrf-1281B.champsimtrace.xz",
        "481.wrf-196B.champsimtrace.xz",
        "481.wrf-455B.champsimtrace.xz",
        "481.wrf-816B.champsimtrace.xz",
        "482.sphinx3-1100B.champsimtrace.xz",
        "482.sphinx3-1297B.champsimtrace.xz",
        "482.sphinx3-1395B.champsimtrace.xz",
        "482.sphinx3-1522B.champsimtrace.xz", 
        "482.sphinx3-234B.champsimtrace.xz",
        "482.sphinx3-417B.champsimtrace.xz",
        "483.xalancbmk-127B.champsimtrace.xz",
        "602.gcc_s-1850B.champsimtrace.xz",
        "602.gcc_s-2226B.champsimtrace.xz",
        "602.gcc_s-734B.champsimtrace.xz",
        "603.bwaves_s-1740B.champsimtrace.xz",
        "603.bwaves_s-2609B.champsimtrace.xz",
        "603.bwaves_s-2931B.champsimtrace.xz",
        "603.bwaves_s-891B.champsimtrace.xz",
        "605.mcf_s-1152B.champsimtrace.xz",
        "605.mcf_s-1536B.champsimtrace.xz",
        "605.mcf_s-1554B.champsimtrace.xz",
        "605.mcf_s-1644B.champsimtrace.xz",
        "605.mcf_s-472B.champsimtrace.xz",
        "605.mcf_s-484B.champsimtrace.xz",
        "605.mcf_s-665B.champsimtrace.xz",
        "605.mcf_s-782B.champsimtrace.xz",
        "605.mcf_s-994B.champsimtrace.xz",
        "607.cactuBSSN_s-2421B.champsimtrace.xz",
        "607.cactuBSSN_s-3477B.champsimtrace.xz",
        "607.cactuBSSN_s-4004B.champsimtrace.xz",
        "619.lbm_s-2676B.champsimtrace.xz",
        "619.lbm_s-2677B.champsimtrace.xz",
        "619.lbm_s-3766B.champsimtrace.xz",
        "619.lbm_s-4268B.champsimtrace.xz",
        "620.omnetpp_s-141B.champsimtrace.xz",
        "620.omnetpp_s-874B.champsimtrace.xz",
        "621.wrf_s-6673B.champsimtrace.xz",
        "621.wrf_s-8065B.champsimtrace.xz",
        "623.xalancbmk_s-10B.champsimtrace.xz",
        "623.xalancbmk_s-165B.champsimtrace.xz",
        "623.xalancbmk_s-202B.champsimtrace.xz",
        "625.x264_s-20B.champsimtrace.xz",
        "627.cam4_s-490B.champsimtrace.xz",
        "628.pop2_s-17B.champsimtrace.xz",
        "649.fotonik3d_s-10881B.champsimtrace.xz",
        "649.fotonik3d_s-1176B.champsimtrace.xz",
        "649.fotonik3d_s-7084B.champsimtrace.xz",
        "649.fotonik3d_s-8225B.champsimtrace.xz",
        "654.roms_s-1007B.champsimtrace.xz",
        "654.roms_s-1070B.champsimtrace.xz",
        "654.roms_s-1390B.champsimtrace.xz",
        "654.roms_s-1613B.champsimtrace.xz",
        "654.roms_s-293B.champsimtrace.xz",
        "654.roms_s-294B.champsimtrace.xz",
        "654.roms_s-523B.champsimtrace.xz",
        "657.xz_s-2302B.champsimtrace.xz"
]
import os
import csv
import re
import threading

def process_file(filepath, results):
    with open(filepath, "r") as file:
        content = file.readlines()

    pc_count = sum(1 for line in content if line.startswith("pc:"))
    
    # Change set comprehension to normal list comprehension for safety inside string formats
    set_a_list = [line for line in content if line.startswith("pc:")]
    set_a = set(set_a_list)
    
    set_ip = set([re.search(r'ip:(\d+)', line).group(1) for line in set_a if re.search(r'ip:(\d+)', line)])
    set_vpaddr = set([re.search(r'vpaddr:(\d+)', line).group(1) for line in set_a if re.search(r'vpaddr:(\d+)', line)])
    set_offset = set([re.search(r'offset:(\d+)', line).group(1) for line in set_a if re.search(r'offset:(\d+)', line)])
    test_name = re.search(r"---(.*?)(?:\\.|$)", filepath).group(1)
    results.append([test_name, pc_count, len(set_ip), len(set_vpaddr),len(set_offset)])

def main():
    directory_path = './outputsum/output0970/spec2k17/'
    output_csv = './analysis_py/ip_addr.csv'
    results = []
    threads = []

    for test_name in test_names:
        filepath = os.path.join(directory_path, "hashed_perceptron-no-vbertim-no-no-no-no-no-lru-lru-lru-srrip-drrip-lru-lru-lru-1core-no---" + test_name)
        thread = threading.Thread(target=process_file, args=(filepath, results))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    results.sort(key=lambda x: x[0])  # Sort by test name for consistent output

    with open(output_csv, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Test Name", "pc: Line Count", "Set_ip Size", "Set_vpaddr Size"])
        writer.writerows(results)

    print("Processing completed!")

if __name__ == "__main__":
    main()