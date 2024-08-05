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
DATE_SET="0326"
NUM_CORE=4

prefsL1=("ip_stride")
# prefsL1=( "vberti" )

output_base="outputsum/output${DATE_SET}/"
res_test_name="debug"
tmp_par_path="${DATE_SET}tmp_par_4core.out"
traces=( "spec" "cs" "parsec")
trace_base_path="./"
# 设置参数
# warmupInstructions=1400000
# simulationInstructions=10000
warmupInstructions=20000000
simulationInstructions=80000000

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
  ./build_champsim.sh hashed_perceptron no $1 no no no no no lru lru lru srrip drrip lru lru lru 4 no $DATE_SET

  # 返回上级目录
  cd ../..
}

function get_ChampSimPath
{
  ##########参数说明
  # - $1 $2: 预取器名称
  ##########
  champSimPath="./ChampSim/Berti/bin/${DATE_SET}hashed_perceptron-no-$1-no-no-no-no-no-lru-lru-lru-srrip-drrip-lru-lru-lru-4core-no"

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



# 2>&1
function generate_par_multi_core
{
  ##########参数说明
  # - $1: trace_file_path
  # - $2: res_output_path
  # - $3: L1D prefetcher
  # - $4: champSimPath(execute_bin_path)
  # - $5: L2 prefetcher
  ##########
  res_path_exist $2
  execute_bin_name=$(echo $4 | rev | cut -d'/' -f1 | rev)
  
   idx=0
  trace=""
  trace_lists=( "${NUM_CORE}core_homogeneous2.in" "${NUM_CORE}core_heterogeneous2.in" )
  # trace_lists=( "${NUM_CORE}core_homogeneous2.in" )
  for trace_list in "${trace_lists[@]}"
  do
    while read -r line
    do   
        if [[ ! -z $line ]]; then
            # echo $trace
            trace="$trace $trace_base_path$line" 
            continue
        else
          suite_name=$(echo $trace | grep -o './traces/[^ ]*' | head -1 | cut -d'/' -f3)
          echo "$suite_name"
          if [ "$suite_name" == "cs" ]; then
            echo "match_cs"
            echo  "$4 -warmup_instructions $warmupInstructions -simulation_instructions $simulationInstructions -cloudsuite -traces $trace > $2-${3}-no---$idx.out 2>/dev/null" >> $tmp_par_path
          else
            echo  "$4 -warmup_instructions $warmupInstructions -simulation_instructions $simulationInstructions -traces $trace > $2-${3}-no---$idx.out 2>/dev/null" >> $tmp_par_path
          fi
          idx=$(($idx + 1))
          trace=""
        fi
    done < ${trace_list}
  done

}

main()
{
  ########参数说明
  # - $1 是否compile
  truncate -s 0 $tmp_par_path
  for prefL1 in "${prefsL1[@]}"
    do

    #判断是否需要编译
    if [ "$1" == "compile" ]; then
      compile_champsim $prefL1
    fi

    #根据trace获取tmp_par
    # 设置ChampSim的bin路径
    champSimPath=$(get_ChampSimPath $prefL1)
    # 清空tmp_par文件
    
    
    generate_par_multi_core $trace_base_path "$output_base${NUM_CORE}core/" $prefL1 $champSimPath
  done

  if [ "$run_now" = "true" ]; then
  cat $tmp_par_path | xargs -I CMD -P $NUM_THREAD bash -c CMD
  fi
}

main $1
