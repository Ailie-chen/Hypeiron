# define SIZE_16X

# if defined(SIZE_1X)
// MICRO Size
# define HISTORY_TABLE_SET            (8)
# define HISTORY_TABLE_WAY            (16)
# define TABLE_SET_MASK               (0x7)

# define BERTI_TABLE_SIZE             (16)
# define BERTI_TABLE_STRIDE_SIZE      (16)

# elif defined(SIZE_2X)
// 2xMICRO Size
# define HISTORY_TABLE_SET            (16)
# define HISTORY_TABLE_WAY            (32)
# define TABLE_SET_MASK               (0xF)

# define BERTI_TABLE_SIZE             (32)
# define BERTI_TABLE_STRIDE_SIZE      (16)
//# define BERTI_TABLE_STRIDE_SIZE      (32)

# elif defined(SIZE_4X)
// 4xMICRO Size
# define HISTORY_TABLE_SET            (32)
# define HISTORY_TABLE_WAY            (64)
# define TABLE_SET_MASK               (0x1F)
// # define HISTORY_TABLE_SET            (8)
// # define HISTORY_TABLE_WAY            (16)
// # define TABLE_SET_MASK               (0x7)

# define BERTI_TABLE_SIZE             (64)
# define BERTI_TABLE_STRIDE_SIZE      (16)
//# define BERTI_TABLE_STRIDE_SIZE      (64)

# elif defined(SIZE_050X)
// 0.5xMICRO Size
# define HISTORY_TABLE_SET            (16)
# define HISTORY_TABLE_WAY            (8)
# define TABLE_SET_MASK               (0x3)

# define BERTI_TABLE_SIZE             (8)
# define BERTI_TABLE_STRIDE_SIZE      (8)

# elif defined(SIZE_025X)
// 0.25xMICRO Size
# define HISTORY_TABLE_SET            (2)
# define HISTORY_TABLE_WAY            (4)
# define TABLE_SET_MASK               (0x1)

# define BERTI_TABLE_SIZE             (4)
# define BERTI_TABLE_STRIDE_SIZE      (4)

# elif defined(SIZE_8X)
// 4xMICRO Size
# define HISTORY_TABLE_SET            (64)
# define HISTORY_TABLE_WAY            (128)
# define TABLE_SET_MASK               (0x3F)
# define BERTI_TABLE_SIZE             (128)
# define BERTI_TABLE_STRIDE_SIZE      (16)

# elif defined(SIZE_16X)
// 4xMICRO Size
# define HISTORY_TABLE_SET            (256)
# define HISTORY_TABLE_WAY            (16)
# define TABLE_SET_MASK               (0xFF)
# define BERTI_TABLE_SIZE             (256)
# define BERTI_TABLE_STRIDE_SIZE      (16)

# elif defined(SIZE_64X)
// 4xMICRO Size
# define HISTORY_TABLE_SET            (512)
# define HISTORY_TABLE_WAY            (1024)
# define TABLE_SET_MASK               (0x1FF)
# define BERTI_TABLE_SIZE             (1024)
# define BERTI_TABLE_STRIDE_SIZE      (16)
#endif


#ifndef VBERTI_H_
#define VBERTI_H_


#include "cache.h"
#include <algorithm>
#include <vector>
#include <tuple>
#include <queue>
#include <cmath>
#include <map>

#include <stdlib.h>
#include <time.h>

// vBerti defines
# define LATENCY_TABLE_SIZE           (L1D_MSHR_SIZE + 16)

// Mask
# define MAX_HISTORY_IP               (8)
# define MAX_PF                       (16)
# define MAX_PF_LAUNCH                (12)
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
    bool issue;
    bool cold_issue;
    uint64_t access;
    uint64_t pc;
} vberti_t; // This struct is the history table

typedef struct shadow_cache {
    uint64_t addr; // IP Tag
    uint64_t lat;  // Latency
    uint8_t  pf;   // Is this accesed
} shadow_cache_t; // This struct is the vberti table

// Structs
latency_table_t latencyt[NUM_CPUS][LATENCY_TABLE_SIZE];
// Cache Style
history_table_t historyt[NUM_CPUS][HISTORY_TABLE_SET][HISTORY_TABLE_WAY];
shadow_cache_t scache[NUM_CPUS][L1D_SET][L1D_WAY];
std::map<uint64_t, vberti_t*> vbertit[NUM_CPUS];
// To Make a FIFO MAP
std::queue<uint64_t> vbertit_queue[NUM_CPUS];

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

// Auxiliar history table functions
void vberti_table_add(uint64_t tag, uint32_t cpu, int64_t stride);
uint8_t vberti_table_get(uint64_t tag, uint32_t cpu, stride_t res[MAX_PF]);
void vberti_increase_conf_ip(uint64_t tag, uint32_t cpu);

void find_and_update(uint32_t cpu, uint64_t latency, uint64_t tag, 
        uint64_t cycle, uint64_t line_addr);
#endif

void print_stride_table(uint32_t cpu, bool all_print, uint64_t key);