#!/bin/bash

if [ $# -lt 1 ]
then
    echo "usage: ./small_run [vberti/vbertim] [compile]"
    exit
fi

truncate -s 0 deltas_out.txt
traces_all=true
run_now=true
NUM_THREAD=48
DATE_SET="0333"
output_base="outputsum/output${DATE_SET}/"
res_test_name="debug"
tmp_par_path="${DATE_SET}tmp_par.out"
tmp_par_path_compile="${DATE_SET}tmp_par_compile.out"
traces=( "spec" )
trace_base_path="traces/"
# 设置参数
# warmupInstructions=1400000
# simulationInstructions=10000
warmupInstructions=5000000
simulationInstructions=20000000

spec_traces=(
            "403.gcc-17B.champsimtrace.xz"
            # "602.gcc_s-734B.champsimtrace.xz"
            # "401.bzip2-7B.champsimtrace.xz"
            # "471.omnetpp-188B.champsimtrace.xz"
            # "400.perlbench-41B.champsimtrace.xz"
            # "654.roms_s-1007B.champsimtrace.xz"
            # "602.gcc_s-734B.champsimtrace.xz"
            # "401.bzip2-277B.champsimtrace.xz"
            # "621.wrf_s-6673B.champsimtrace.xz"
             )
spec_traces1=(
  # "401.bzip2-277B.champsimtrace.xz"
            "403.gcc-17B.champsimtrace.xz"
            "410.bwaves-1963B.champsimtrace.xz"
            "410.bwaves-2097B.champsimtrace.xz"
            "429.mcf-184B.champsimtrace.xz"
            "429.mcf-192B.champsimtrace.xz"
            "429.mcf-217B.champsimtrace.xz"
            "429.mcf-22B.champsimtrace.xz"
            "429.mcf-51B.champsimtrace.xz"
            "433.milc-127B.champsimtrace.xz"
            "433.milc-274B.champsimtrace.xz"
            "433.milc-337B.champsimtrace.xz"
            "434.zeusmp-10B.champsimtrace.xz"
            "436.cactusADM-1804B.champsimtrace.xz"
            "437.leslie3d-134B.champsimtrace.xz"
            "437.leslie3d-149B.champsimtrace.xz"
            "437.leslie3d-232B.champsimtrace.xz"
            "437.leslie3d-265B.champsimtrace.xz"
            "437.leslie3d-271B.champsimtrace.xz"
            "437.leslie3d-273B.champsimtrace.xz"
            "450.soplex-247B.champsimtrace.xz"
            "450.soplex-92B.champsimtrace.xz"
            "459.GemsFDTD-1169B.champsimtrace.xz"
            "459.GemsFDTD-1211B.champsimtrace.xz"
            "459.GemsFDTD-1320B.champsimtrace.xz"
            "459.GemsFDTD-1418B.champsimtrace.xz"
            "459.GemsFDTD-1491B.champsimtrace.xz"
            "459.GemsFDTD-765B.champsimtrace.xz"
            "462.libquantum-1343B.champsimtrace.xz"
            "462.libquantum-714B.champsimtrace.xz"
            "470.lbm-1274B.champsimtrace.xz"
            "471.omnetpp-188B.champsimtrace.xz"
            "473.astar-359B.champsimtrace.xz"
            "473.astar-42B.champsimtrace.xz"
            "481.wrf-1254B.champsimtrace.xz"
            "481.wrf-1281B.champsimtrace.xz"
            "481.wrf-196B.champsimtrace.xz"
            "481.wrf-455B.champsimtrace.xz"
            "481.wrf-816B.champsimtrace.xz"
            "482.sphinx3-1100B.champsimtrace.xz"
            "482.sphinx3-1297B.champsimtrace.xz"
            "482.sphinx3-1395B.champsimtrace.xz"
            "482.sphinx3-1522B.champsimtrace.xz"
            "482.sphinx3-234B.champsimtrace.xz"
            "482.sphinx3-417B.champsimtrace.xz"
            "483.xalancbmk-127B.champsimtrace.xz"
            "602.gcc_s-1850B.champsimtrace.xz"
            "602.gcc_s-2226B.champsimtrace.xz"
            "602.gcc_s-734B.champsimtrace.xz"
            "603.bwaves_s-1740B.champsimtrace.xz"
            "603.bwaves_s-2609B.champsimtrace.xz"
            "603.bwaves_s-2931B.champsimtrace.xz"
            "603.bwaves_s-891B.champsimtrace.xz"
            "605.mcf_s-1152B.champsimtrace.xz"
            "605.mcf_s-1536B.champsimtrace.xz"
            "605.mcf_s-1554B.champsimtrace.xz"
            "605.mcf_s-1644B.champsimtrace.xz"
            "605.mcf_s-472B.champsimtrace.xz"
            "605.mcf_s-484B.champsimtrace.xz"
            "605.mcf_s-665B.champsimtrace.xz"
            "605.mcf_s-782B.champsimtrace.xz"
            "605.mcf_s-994B.champsimtrace.xz"
            "607.cactuBSSN_s-2421B.champsimtrace.xz"
            "607.cactuBSSN_s-3477B.champsimtrace.xz"
            "607.cactuBSSN_s-4004B.champsimtrace.xz"
            "619.lbm_s-2676B.champsimtrace.xz"
            "619.lbm_s-2677B.champsimtrace.xz"
            "619.lbm_s-3766B.champsimtrace.xz"
            "619.lbm_s-4268B.champsimtrace.xz"
            "620.omnetpp_s-141B.champsimtrace.xz"
            "620.omnetpp_s-874B.champsimtrace.xz"
            "621.wrf_s-6673B.champsimtrace.xz"
            "621.wrf_s-8065B.champsimtrace.xz"
            "623.xalancbmk_s-10B.champsimtrace.xz"
            "623.xalancbmk_s-165B.champsimtrace.xz"
            "623.xalancbmk_s-202B.champsimtrace.xz"
            "625.x264_s-20B.champsimtrace.xz"
            "627.cam4_s-490B.champsimtrace.xz"
            "628.pop2_s-17B.champsimtrace.xz"
            "649.fotonik3d_s-10881B.champsimtrace.xz"
            "649.fotonik3d_s-1176B.champsimtrace.xz"
            "649.fotonik3d_s-7084B.champsimtrace.xz"
            "649.fotonik3d_s-8225B.champsimtrace.xz"
            "654.roms_s-1007B.champsimtrace.xz"
            "654.roms_s-1070B.champsimtrace.xz"
            "654.roms_s-1390B.champsimtrace.xz"
            "654.roms_s-1613B.champsimtrace.xz"
            "654.roms_s-293B.champsimtrace.xz"
            "654.roms_s-294B.champsimtrace.xz"
            "654.roms_s-523B.champsimtrace.xz"
            "657.xz_s-2302B.champsimtrace.xz"
)

cs_traces=(
  "cassandra_phase0_core0.trace.xz"
)
gap_traces=(
  "sssp-3.trace.gz"
)
ligra_traces=()

# 检查是否定义了编译参数，并且据此对champsim进行编译
function compile_champsim
{
  ##########参数说明
  # - $1: 预取器名称
  ##########
  cd ChampSim/Berti
  # if [ "$1" = "vberti" ] || [ "$1" = "vbertim" ] ; then
  #   cd ChampSim/Berti
  # else
  #   cd ChampSim/Other_PF
  # fi
  
  # 执行构建命令
  ./build_champsim.sh hashed_perceptron no $1 no no no no no lru lru lru srrip drrip lru lru lru 1 no $DATE_SET

  # 返回上级目录
  cd ../..
}

function get_ChampSimPath
{
  ##########参数说明
  # - $1: 预取器名称
  ##########
  champSimPath="./ChampSim/Berti/bin/${DATE_SET}hashed_perceptron-no-$1-no-no-no-no-no-lru-lru-lru-srrip-drrip-lru-lru-lru-1core-no"

  # if [ "$1" = "vberti" ] || [ "$1" = "vbertim" ] ; then
  #   champSimPath="./ChampSim/Berti/bin/${DATE_SET}hashed_perceptron-no-$1-no-no-no-no-no-lru-lru-lru-srrip-drrip-lru-lru-lru-1core-no"
  # else
  #   champSimPath="./ChampSim/Other_PF/bin/${DATE_SET}hashed_perceptron-no-$1-no-no-no-no-no-lru-lru-lru-srrip-drrip-lru-lru-lru-1core-no"
  # fi
  echo "$champSimPath"
}


# 判断结果路径是否存在，如果不存在则创建结果路径
function res_path_exist
{
  ##########参数说明
  # - $1: res_output_path
  ##########
  if [ ! -d "$1" ]; then
      mkdir -p "$1"
  fi
}



# 运行ChampSim命令，针对每个跟踪文件进行循环,生成对应的模拟器bin文件运行trace的指令
function generate_par
{
  ##########参数说明
  # - $1: trace_file_path
  # - $2: res_output_path
  # - $3: prefetcher
  # - $4: champSimPath
  # - $5: trace
  ##########
  if [ "$traces_all" = "true" ]; then
    case "$5" in
      "spec")
        traceFiles=("${spec_traces1[@]}")
        ;;
    *)
        traceFiles=()
        while IFS= read -r line; do
          traceFiles+=("$line")
        done < "$trace_base_path$5_name.txt"
        ;;
    esac
      # traceFiles=()
      # while IFS= read -r line; do
      #   traceFiles+=("$line")
      # done < "$trace_base_path$5_name.txt"
  else
    case "$5" in
      "spec")
        traceFiles=("${spec_traces[@]}");;
      "cs")
        traceFiles=("${cs_traces[@]}");;
      "gap")
        traceFiles=("${gap_traces[@]}");;
      "ligra")
      traceFiles=("${ligra_traces[@]}");;
    esac 
  fi
  for traceFile in "${traceFiles[@]}"
  do
    # 设置输出文件名
    traceFilebase=$(basename "$traceFile")
    # outputFile="$2/hashed_perceptron-no-${3}-no-no-no-no-no-lru-lru-lru-srrip-drrip-lru-lru-lru-1core-no---$traceFilebase"
    outputFile="$2/-${3}-no---$traceFilebase"
    # outputFile="$2/$traceFilebase"    
    # 运行ChampSim命令
    if [[ $output_base == *"test"* ]]; then
      outputFile="$2/$res_test_name$traceFilebase"
    fi
    if [[ $5 == "cs" ]];then
      echo "$4 -warmup_instructions $warmupInstructions -simulation_instructions $simulationInstructions -cloudsuite -traces $1$traceFilebase > $outputFile 2>/dev/null" >> ${tmp_par_path}
    else
      echo "$4 -warmup_instructions $warmupInstructions -simulation_instructions $simulationInstructions -traces $1$traceFilebase > $outputFile 2>&1" >> ${tmp_par_path}
    fi
  done
}
# 2>&1

main()
{
      # 设置源文件和目标文件的路径
    
    source_file="ChampSim/Berti/batch_prefetcher/hyperion_hpc_aDiGHB_UTBh1.l1d_pref"
    cp "ChampSim/Berti/prefetcher/hyperion_hpc_aDiGHB_UTBh1.l1d_pref" "$source_file"
    P1S=( 16 24 32 64 128 )
    prefs=()
    for P1 in "${P1S[@]}"; do
        pref="hyperion_hpc_pcstride_${P1}"
        # pref="no"
        destination_file="ChampSim/Berti/batch_prefetcher/${pref}.l1d_pref"
        cp "$source_file" "$destination_file"
        const uint64_t PC_STRIDE_TABLE_SIZE=16
        sed -i "s/const uint64_t PC_STRIDE_TABLE_SIZE = 16/const uint64_t PC_STRIDE_TABLE_SIZE = ${P1}/" "$destination_file"
        prefs+=("$pref")
    done

    python3 analysis_py/evaluation3/sensitive_design/json_modify.py "${prefs[@]}" "$DATE_SET"

  ########参数说明
  # - $1 是否compile
  truncate -s 0 $tmp_par_path
  
  
  for pref in "${prefs[@]}"
  do   
    #判断是否需要编译
    if [ "$1" == "compile" ]; then
      compile_champsim $pref
    fi
    #根据trace获取tmp_par
    # 设置ChampSim的bin路径
    champSimPath=$(get_ChampSimPath $pref)
    # 清空tmp_par文件
    
    
    for trace in "${traces[@]}"
    do
        trace_file_path="$trace_base_path$trace/"
        res_output_path="$output_base$trace"
        res_path_exist $res_output_path  
        generate_par $trace_file_path $res_output_path $pref $champSimPath $trace
    done
  done

  if [ "$run_now" = "true" ]; then
    cat $tmp_par_path | xargs -I CMD -P $NUM_THREAD bash -c CMD
  fi

  python3 analysis_py/evaluation3/sensitive_design/1core_1pref_evaluate_all.py
}

main $1
