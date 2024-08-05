#!/bin/bash

if [ $# -lt 1 ]
then
    echo "usage: ./small_run [vberti/vbertim] [compile]"
    exit
fi

truncate -s 0 deltas_out.txt
traces_all=true
run_now=true
NUM_THREAD=64
output_base="outputsum/output0704/"
tmp_par_path="tmp_par_test_all.out"


# 设置ChampSim路径
if [ "$1" = "vberti" ] || [ "$1" = "vbertim" ] || [ "$1" = "no" ]; then
  champSimPath="./ChampSim/Berti/bin/hashed_perceptron-no-$1-test_all-no-no-no-no-no-lru-lru-lru-srrip-drrip-lru-lru-lru-1core-no"
else
  champSimPath="./ChampSim/Other_PF/bin/hashed_perceptron-no-$1-no-no-no-no-no-lru-lru-lru-srrip-drrip-lru-lru-lru-1core-no"
fi

# 设置参数
warmupInstructions=20000000
simulationInstructions=80000000
# warmupInstructions=50000
# simulationInstructions=50000
trace_path=traces/spec2k17

if [ "$traces_all" = "true" ]; then
  traceFiles=$(ls $trace_path/*.champsimtrace.xz)
  IFS=$'\n' read -d '' -r -a traceFiles <<< "$traceFiles"
else
  traceFiles=(
             
            "602.gcc_s-1850B.champsimtrace.xz"
            "602.gcc_s-2226B.champsimtrace.xz"
            #  "403.gcc-16B.champsimtrace.xz"
            #  "403.gcc-17B.champsimtrace.xz"
            #  "403.gcc-48B.champsimtrace.xz"
            #  "433.milc-337B.champsimtrace.xz"
            #  "433.milc-274B.champsimtrace.xz"
            #  "433.milc-127B.champsimtrace.xz"
            #  "607.cactuBSSN_s-2421B.champsimtrace.xz"
            #  "605.mcf_s-1554B.champsimtrace.xz"
            #  "605.mcf_s-472B.champsimtrace.xz"
            #  "605.mcf_s-484B.champsimtrace.xz"
            #  "605.mcf_s-665B.champsimtrace.xz"
            #  "607.cactuBSSN_s-2421B.champsimtrace.xz"
            #  "607.cactuBSSN_s-3477B.champsimtrace.xz"
            #  "607.cactuBSSN_s-4004B.champsimtrace.xz"
            #  "607.cactuBSSN_s-4248B.champsimtrace.xz"
             )
fi
# 定义跟踪文件列表


# 检查是否定义了编译参数
if [ "$2" = "compile" ]; then
  # 进入ChampSim/Berti目录
  cd ChampSim/Berti
  
  line_number=234  # 要修改的行号
  pattern="\${L1D_PREFETCHER}"  # 要替换的旧内容
  replacement="\${L1D_PREFETCHER}-test_all"  # 要替换成的新内容
  # 执行构建命令
  sed -i "${line_number}s/${pattern}/${replacement}/" "build_champsim.sh"
  ./build_champsim.sh hashed_perceptron no $1 no no no no no lru lru lru srrip drrip lru lru lru 1 no
  sed -i "${line_number}s/${replacement}/${pattern}/" "build_champsim.sh"
  
  # 返回上级目录
  cd ../..
fi


truncate -s 0 $tmp_par_path

# 运行ChampSim命令，针对每个跟踪文件进行循环
for traceFile in "${traceFiles[@]}"
do
  # 设置输出文件名
  traceFilebase=$(basename "$traceFile")
  outputFile="$output_base/spec2k17/hashed_perceptron-no-$1-no-no-no-no-no-lru-lru-lru-srrip-drrip-lru-lru-lru-1core-no---$traceFilebase"
  
  # 运行ChampSim命令
  #echo "$champSimPath -warmup_instructions $warmupInstructions -simulation_instructions $simulationInstructions -traces traces/spec2k17/$traceFilebase > $outputFile 2>/dev/null" >> $tmp_par_path
  echo "$champSimPath -warmup_instructions $warmupInstructions -simulation_instructions $simulationInstructions -traces traces/spec2k17/$traceFilebase > $outputFile" >> $tmp_par_path

  #ons 80000000 -traces $traceFile > $outputFile 2>/dev/null
done


if [ "$run_now" = "true" ]; then
  cat $tmp_par_path | xargs -I CMD -P $NUM_THREAD bash -c CMD
  for traceFile in "${traceFiles[@]}"
  do
    # 设置输出文件名
    outputFileName=$(basename "$traceFile")
    outputFile="$output_base/spec2k17/hashed_perceptron-no-$1-no-no-no-no-no-lru-lru-lru-srrip-drrip-lru-lru-lru-1core-no---$outputFileName"
    
    ipcValue=$(grep -Po 'CPU 0 cumulative IPC: \K[0-9.]*' $outputFile)
    echo "IPC value for $1 $outputFileName: $ipcValue"
  done
fi