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
DATE_SET="0418"
NUM_CORE=4

prefsL1=( "hyperion_hpc_2table_UTBh1_buffer9_1" )
# prefsL1=( "vberti" )

output_base="outputsum/output${DATE_SET}/"
res_test_name="debug"
tmp_par_path="${DATE_SET}tmp_par_4core.out"
traces=( "spec2k17" "cs" "gap" "ligra")
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
  
  if [ ! -f ${NUM_CORE}core_test.in ]; then #判断多核的traces文件是否存在,Xcore.in最终以两个空格结尾
    echo "muti core traces does not exist..."
  else
    idx=0
    trace=""
    while read -r line
    do   
        if [[ ! -z $line ]]; then
            # echo $trace
            traces_set_name=$(echo $trace | cut -d'/' -f1) #注意cs测试集不能和其他的测试集混合作为多核的测试集
            trace="$trace $trace_base_path$line" 
            continue
        else
        #   if [ trace_set_name == " cs" ]; then
        #     echo  "$4 -warmup_instructions $warmupInstructions -simulation_instructions $simulationInstructions -cloudsuite -traces $trace > $2$---$idx.out 2>/dev/null" >> $tmp_par_path
        #   else
        #     echo  "$4 -warmup_instructions $warmupInstructions -simulation_instructions $simulationInstructions -traces $trace > $2$execute_bin_name---$idx.out 2>/dev/null" >> $tmp_par_path
        #   fi
            echo  "$4 -warmup_instructions $warmupInstructions -simulation_instructions $simulationInstructions -traces $trace > $2-${3}-no---$idx.out 2>/dev/null" >> $tmp_par_path

          idx=$(($idx + 1))
          trace=""
        fi
    done < ${NUM_CORE}core_test.in
  fi
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
