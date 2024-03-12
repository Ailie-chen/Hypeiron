#include "cache.h"
#include <algorithm>
#include <vector>
#include <tuple>
#include <queue>
#include <cmath>
#include <map>

#include <stdlib.h>
#include <time.h>


typedef struct l2c_shadow_cache {
    uint64_t addr; // IP Tag
    uint8_t  pf;   // Is this accesed
} l2c_shadow_cache_t; // This struct is the vberti table

l2c_shadow_cache_t l2c_scache[NUM_CPUS][L2C_SET][L2C_WAY];


// Shadow cache
void l2c_shadow_cache_init(uint32_t cpu);
uint8_t l2c_shadow_cache_add(uint32_t cpu, uint32_t set, uint32_t way, 
        uint64_t line_addr, uint8_t pf);
uint8_t l2c_shadow_cache_get(uint32_t cpu, uint64_t line_addr);
uint8_t l2c_shadow_cache_pf(uint32_t cpu, uint64_t line_addr);
uint8_t l2c_shadow_cache_is_pf(uint32_t cpu, uint64_t line_addr);