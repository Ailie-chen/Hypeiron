#!/bin/bash
#!/bin/bash

# 设置源文件和目标文件的路径
source_file="ChampSim/Berti/prefetcher/hyperion.l1d_pref"

# sets=(128 96 64 48 32 16 8)
# ways=(2 4 6 8 10 12)
# pages=(8 12 16 32)
# for set in "${sets[@]}"; do
#     for way in "${ways[@]}"; do
#         for page in "${pages[@]}"; do
#             destination_file="ChampSim/Berti/prefetcher/hyperion_${page}_${set}_${way}.l1d_pref"
#             cp "$source_file" "$destination_file"
#             sed -i "s/#define PAGE_SIZE (64 \* 1)/#define PAGE_SIZE (64 * $page)/" "$destination_file"
#             size=$(($set * $way))
#             sed -i "s/const uint64_t ACCUMULATE_TABLE=.*/const uint64_t ACCUMULATE_TABLE=$size;/" "$destination_file"
#             sed -i "s/const uint64_t ACCUMULATE_WAYS=.*/const uint64_t ACCUMULATE_WAYS=$way;/" "$destination_file"
#             pref="hyperion_${page}_${set}_${way}"
#             # sed -i "s/run_now=true/run_now=false/" "small_run.sh"
#             ./small_run.sh "$pref" "compile"
#         done
#     done
# done

sets=(128 96 64 48 32 16 8)
ways=(2 4 6 8 10 12)
pages=(8 12 16 32)
for set in "${sets[@]}"; do
    for page in "${pages[@]}"; do
        for way in "${ways[@]}"; do
        
            # destination_file="ChampSim/Berti/prefetcher/hyperion_${page}_${set}_${way}.l1d_pref"
            # cp "$source_file" "$destination_file"
            # sed -i "s/#define PAGE_SIZE (64 \* 1)/#define PAGE_SIZE (64 * $page)/" "$destination_file"
            # size=$(($set * $way))
            # sed -i "s/const uint64_t ACCUMULATE_TABLE=.*/const uint64_t ACCUMULATE_TABLE=$size;/" "$destination_file"
            # sed -i "s/const uint64_t ACCUMULATE_WAYS=.*/const uint64_t ACCUMULATE_WAYS=$way;/" "$destination_file"
            pref="hyperion_${page}_${set}_${way}"
            echo "\"${pref}\","
            # sed -i "s/run_now=true/run_now=false/" "small_run.sh"
            # ./small_run.sh "$pref"
        done
    done
done