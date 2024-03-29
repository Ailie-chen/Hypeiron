output_workloads = [
        "403.gcc-17B",
        "410.bwaves-1963B",
        "410.bwaves-2097B",
        "429.mcf-184B",
        "429.mcf-192B",
        "429.mcf-217B",
        "429.mcf-22B",
        "429.mcf-51B",
        "433.milc-127B",
        "433.milc-274B",
        "433.milc-337B",
        "434.zeusmp-10B",
        "436.cactusADM-1804B",
        "437.leslie3d-134B",
        "437.leslie3d-149B",
        "437.leslie3d-232B",
        "437.leslie3d-265B",
        "437.leslie3d-271B",
        "437.leslie3d-273B",
        "450.soplex-247B",
        "450.soplex-92B",
        "459.GemsFDTD-1169B",
        "459.GemsFDTD-1211B",
        "459.GemsFDTD-1320B",
        "459.GemsFDTD-1418B",
        "459.GemsFDTD-1491B",
        "459.GemsFDTD-765B",
        "462.libquantum-1343B",
        "462.libquantum-714B",
        "470.lbm-1274B",
        "471.omnetpp-188B",
        "473.astar-359B",
        "473.astar-42B",
        "481.wrf-1254B",
        "481.wrf-1281B",
        "481.wrf-196B",
        "481.wrf-455B",
        "481.wrf-816B",
        "482.sphinx3-1100B",
        "482.sphinx3-1297B",
        "482.sphinx3-1395B",
        "482.sphinx3-1522B", 
        "482.sphinx3-234B",
        "482.sphinx3-417B",
        "483.xalancbmk-127B",
        "602.gcc_s-1850B",
        "602.gcc_s-2226B",
        "602.gcc_s-734B",
        "603.bwaves_s-1740B",
        "603.bwaves_s-2609B",
        "603.bwaves_s-2931B",
        "603.bwaves_s-891B",
        "605.mcf_s-1152B",
        "605.mcf_s-1536B",
        "605.mcf_s-1554B",
        "605.mcf_s-1644B",
        "605.mcf_s-472B",
        "605.mcf_s-484B",
        "605.mcf_s-665B",
        "605.mcf_s-782B",
        "605.mcf_s-994B",
        "607.cactuBSSN_s-2421B",
        "607.cactuBSSN_s-3477B",
        "607.cactuBSSN_s-4004B",
        "619.lbm_s-2676B",
        "619.lbm_s-2677B",
        "619.lbm_s-3766B",
        "619.lbm_s-4268B",
        "620.omnetpp_s-141B",
        "620.omnetpp_s-874B",
        "621.wrf_s-6673B",
        "621.wrf_s-8065B",
        "623.xalancbmk_s-10B",
        "623.xalancbmk_s-165B",
        "623.xalancbmk_s-202B",
        "625.x264_s-20B",
        "627.cam4_s-490B",
        "628.pop2_s-17B",
        "649.fotonik3d_s-10881B",
        "649.fotonik3d_s-1176B",
        "649.fotonik3d_s-7084B",
        "649.fotonik3d_s-8225B",
        "654.roms_s-1007B",
        "654.roms_s-1070B",
        "654.roms_s-1390B",
        "654.roms_s-1613B",
        "654.roms_s-293B",
        "654.roms_s-294B",
        "654.roms_s-523B",
        "657.xz_s-2302B"  
]
import os
import shutil

def move_files_not_containing_keywords(src_folder, dst_folder, keywords):
    """
    移动src_folder中不包含keywords中任意元素的文件到dst_folder

    参数:
    - src_folder: 源文件夹路径
    - dst_folder: 目标文件夹路径
    - keywords: 关键词列表
    """

    # 确保目标文件夹存在
    if not os.path.exists(dst_folder):
        os.makedirs(dst_folder)

    # 遍历源文件夹中的每个文件
    for filename in os.listdir(src_folder):
        full_file_path = os.path.join(src_folder, filename)

        # 如果当前文件是一个文件并且文件名不包含关键词列表中的任何关键词
        if os.path.isfile(full_file_path) and not any(keyword in filename for keyword in keywords):
            shutil.move(full_file_path, os.path.join(dst_folder, filename))

if __name__ == "__main__":
    src_folder = "./outputsum/output1021/spec2k17/" # 源文件夹的路径
    dst_folder = "./outputsum/output1021/spec2k06/" # 目标文件夹的路径 

    move_files_not_containing_keywords(src_folder, dst_folder, output_workloads)
