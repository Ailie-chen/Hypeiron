#ifndef VBERTI_H_
#define VBERTI_H_

// #define BERTI_IP_TABLE_DEBUG

#include "vberti_size.h"

#include "cache.h"
#include <algorithm>
#include <vector>
#include <tuple>
#include <queue>
#include <cmath>
#include <map>

#include <stdlib.h>
#include <time.h>

//# define LOG2_BLOCKS_PER_PAGE            (6)

// vBerti defines
# define LATENCY_TABLE_SIZE           (L1D_MSHR_SIZE + 16)

// Mask
# define MAX_HISTORY_IP               (8)
# define MAX_PF                       (16)
# define MAX_PF_LAUNCH                (12)//12
# define STRIDE_MASK                  (12)

// Mask
# define IP_MASK                      (0x3FF)
# define TIME_MASK                    (0xFFFF)
# define LAT_MASK                     (0xFFF)
//# define LAT_MASK                     (0xFFFF)
# define ADDR_MASK                    (0xFFFFFF)

// Confidence
# define CONFIDENCE_MAX               (16) // 6 bits
# define CONFIDENCE_INC               (1) // 6 bits
# define CONFIDENCE_INIT              (1) // 6 bits
# define CONFIDENCE_L1                (65) // 6 bits
# define CONFIDENCE_L2                (50) // 6 bits
# define CONFIDENCE_L2R               (35) // 6 bits
//# define CONFIDENCE_L2R               (CONFIDENCE_L2) // 6 bits
# define MSHR_LIMIT                   (70)

// Stride rpl
// L1, L2, L2 reemplazable y No (reemplazable).
# define R                            (0x0)
# define L1                           (0x1)
# define L2                           (0x2)
# define L2R                          (0x3)
# define NO_PREFETCH                  (0x4)

// Structs define
typedef struct latency_table {
    uint64_t addr; // Addr
    uint64_t tag; // Addr
    uint64_t time; // Time where the line is accessed or time between PQ and 
                   // MSHR in case of prefetch
    uint8_t  pf; // Is the entry accessed by a demand miss
} latency_table_t; // This struct is the latency table

typedef struct history_table {
    uint64_t tag;  // IP Tag
    uint64_t addr; // IP @ accessed
    uint64_t time; // Time where the line is accessed
} history_table_t; // This struct is the history table

// Confidence tuple
typedef struct Stride {
    uint64_t conf;
    int64_t stride;
    uint8_t rpl;
    float   per;
    Stride(): conf(0), stride(0), rpl(0), per(0) {};
} stride_t; 

typedef struct VBerti {
    stride_t *stride;
    uint64_t conf;
    uint64_t total_used;
    
} vberti_t; // This struct is the history table

typedef struct shadow_cache {
    uint64_t addr; // IP Tag
    uint64_t lat;  // Latency
    uint8_t  pf;   // Is this accesed
} shadow_cache_t; // This struct is the vberti table

typedef struct Pages_Berti{
    stride_t *stride;
    uint64_t conf;
    uint64_t total_used;
        
} pages_berti_t;

// Structs
latency_table_t latencyt[NUM_CPUS][LATENCY_TABLE_SIZE];
// Cache Style
history_table_t historyt[NUM_CPUS][HISTORY_TABLE_SET][HISTORY_TABLE_WAY];
shadow_cache_t scache[NUM_CPUS][L1D_SET][L1D_WAY];
std::map<uint64_t, vberti_t*> vbertit[NUM_CPUS];
std::map<uint64_t, pages_berti_t*> pages_bertit[NUM_CPUS];
// To Make a FIFO MAP
std::queue<uint64_t> vbertit_queue[NUM_CPUS];
std::queue<uint64_t> pages_bertit_queue[NUM_CPUS];

// Auxiliar pointers
history_table_t *history_pointers[NUM_CPUS][HISTORY_TABLE_SET];

void notify_prefetch(uint64_t addr, uint64_t cycle);

// Auxiliary latency table functions
void latency_table_init(uint32_t cpu);
uint8_t latency_table_add(uint64_t line_addr, uint64_t tag, uint32_t cpu, 
        uint8_t pf);
uint8_t latency_table_add(uint64_t line_addr, uint64_t tag, uint32_t cpu, 
        uint8_t pf, uint64_t cycle);
uint64_t latency_table_del(uint64_t line_addr, uint32_t cpu);
uint64_t latency_table_get_ip(uint64_t line_addr, uint32_t cpu);

// Shadow cache
void shadow_cache_init(uint32_t cpu);
uint8_t shadow_cache_add(uint32_t cpu, uint32_t set, uint32_t way, 
        uint64_t line_addr, uint8_t pf, uint64_t latency);
uint8_t shadow_cache_get(uint32_t cpu, uint64_t line_addr);
uint8_t shadow_cache_pf(uint32_t cpu, uint64_t line_addr);
uint8_t shadow_cache_is_pf(uint32_t cpu, uint64_t line_addr);

// Auxiliar history table functions
void history_table_init(uint32_t cpu);
void history_table_add(uint64_t tag, uint32_t cpu, uint64_t addr);
uint8_t is_in_history(uint64_t tag, uint32_t cpu, uint64_t addr);
uint16_t history_table_get(uint32_t cpu, uint32_t latency, 
        uint64_t tag, uint64_t act_addr, uint64_t ip[HISTORY_TABLE_WAY], 
        uint64_t addr[HISTORY_TABLE_WAY], uint64_t cycle);

uint16_t history_table_pages_get(uint32_t cpu, uint32_t latency, 
         uint64_t act_addr, uint64_t addr[HISTORY_TABLE_WAY*HISTORY_TABLE_SET], uint64_t cycle);

// Auxiliar history table functions
void vberti_table_add(uint64_t tag, uint32_t cpu, int64_t stride);
uint8_t vberti_table_get(uint64_t tag, uint32_t cpu, stride_t res[MAX_PF]);
void vberti_increase_conf_ip(uint64_t tag, uint32_t cpu);

void find_and_update(uint32_t cpu, uint64_t latency, uint64_t tag, 
        uint64_t cycle, uint64_t line_addr);

void pages_berti_table_add(uint64_t page_addr, uint32_t cpu, int64_t stride);
uint8_t pages_berti_table_get(uint64_t page_addr, uint32_t cpu, stride_t res[MAX_PF]);
void pages_berti_increase_conf_ip(uint64_t page_addr, uint32_t cpu);

#endif
//add
//history ：添加使用page或者page+offset进行索引的功能，返回page内满足要求的deltas
//deltas table：对于每一个page设置一个deltas表，找出最高的deltas，计算deltas要求使用访问次数，


//添加BOP
//# define    BOP_LEARN_DEPTH     (8)
# define    BOP_DELTAS_NUM      (52)
# define    BOP_MAX_SCORE       (32)
# define    BOP_MAX_ROUND       (300)
# define    BOP_PF_DEGREE       (1)
typedef struct BOP_DELTA_ENTRY
{
    int64_t delta;
    uint64_t score;
}bop_delta_entry;

bop_delta_entry bop_deltas_table[NUM_CPUS][BOP_DELTAS_NUM];
bop_delta_entry bop_local_best_delta[NUM_CPUS];
uint64_t bop_global_best_delta[NUM_CPUS];
uint64_t bop_learning_round[NUM_CPUS];
bool bop_pf_init_finish[NUM_CPUS];

uint16_t history_table_bop_get(uint32_t cpu, uint32_t latency, 
         uint64_t line_addr, 
         uint64_t timely_addr[HISTORY_TABLE_WAY*HISTORY_TABLE_SET], 
         uint64_t cycle);

void bop_deltas_table_update(uint32_t cpu, int64_t delta);
void bop_deltas_table_init(uint32_t cpu);


//为BINGO_BOP进行定义
# define RR_TABLE_SIZE  (256)
# define DEGREE         (2)

#ifdef PREFETCHER_CLASS_DEBUG
//对应的decode版本定义在cache.cc和cache.h中
//metadata[8:7]来做标记：01：IP， 10：Pages 11：bop
uint32_t metadata_encode(uint32_t metadata_origin, uint32_t prefetcher_type);
#endif

#ifdef BERTI_IP_TABLE_DEBUG
    void print_latency_table(uint32_t cpu);
    void print_history_table(uint32_t cpu);
    void print_stride_table(uint32_t cpu);
#endif


typedef struct mix_delta_struct
{
    uint64_t pf_addr;
    uint64_t ip;
    int fill_level;
    std::vector<int> prefetcher;//0:berti_pp_cold, 1:berti_pp_hot,2:nextline, 3:berti_ip,4:bop,5:bingo
    uint64_t berti_pp_index;
    uint64_t score;
    std::vector<uint64_t> scores;
} mix_delta;
std::vector<mix_delta> mix_deltas;
void mergeDelta(std::vector<mix_delta> &data, const mix_delta &newElement);
bool compare_delta_scores(const mix_delta &a, const mix_delta &b);

typedef struct _berti_pp_pref_entry
{
    uint64_t ip;
    uint64_t addr;
    uint64_t pf_addr;  
    int fill_level;
}berti_pp_pref_entry;

std::queue<berti_pp_pref_entry> berti_pp_pref_queue;