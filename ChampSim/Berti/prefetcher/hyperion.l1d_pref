#include "vbertimix.h"
#include "bingo_frame.h"
#define LANZAR_INT 8
//采用组相联架构，page索引，pc做tag
// Last edit: 27 - Sept - 2021 12:10
#define LOG2_BLOCKS_PER_PAGE 10
#define PAGE_SIZE (64 * 1)
//data structure:
//(1) filter table: fully-associated, lru, page to tag
//(2) history table: fully-associated, lru, hash(page,pc) or page to index
//(3) delta table:fully-associated, lru, hash(page,pc) or page to index

// FIFO queue
//#define SIZE_RR 16
//uint64_t RR[NUM_CPUS][SIZE_RR] = {0};
//uint64_t RR_cycle[NUM_CPUS][SIZE_RR] = {0};
//uint64_t RR_dx[NUM_CPUS] = {0};
#define PAGE
#define PAGE_PREF
// #define OFFSET
// #define GLOBAL
bool spec_intructions_complete;
uint64_t global_first_offset;
struct PAGE_SETTING{
    const uint64_t ACCUMULATE_TABLE=32;
    const uint64_t ACCUMULATE_WAYS=4;
    const uint64_t OFFSET_NUMBER=16;
    const uint64_t STRIDES_NUMBER=16;


    const uint64_t WAY_CONFIDENCE_MAX = 16;
    const float WAY_L1_THRESHOLD=0.6;
    const float WAY_L2_THRESHOLD=0.5;
    const float WAY_LLC_THRESHOLD=0.35;

    const uint64_t SET_CONFIDENCE_MAX = 16;
    const float SET_L1_THRESHOLD=0.6;
    const float SET_L2_THRESHOLD=0.15;
    const float SET_LLC_THRESHOLD=0.3;

    const uint64_t STRIDE_COUNT_TABLE=32;
    const uint64_t INTERVAL=100;
    const float GLOBAL_STRIDE_THRESHOLD=0.50;
    // const float GLOBAL_STRIDE_THRESHOLD=2.0;
    const float GLOBAL_STRIDE_THRESHOLD_LLC=GLOBAL_STRIDE_THRESHOLD;

    const int ALL_MAX_PF = 12;
};


struct global_setting{
    const uint64_t GLOBAL_HISTORY_NUMBER = 16;
};


struct Berti_SETTING{
    const uint64_t CONFIDENCE_INC_S = 1;
    const uint64_t CONFIDENCE_INIT_S = 1;
    const int CONFIDENCE_L1_S = 65;
    const uint64_t CONFIDENCE_L2_S = 50;
    const uint64_t CONFIDENCE_L2R_S = 35;
    const uint64_t HISTORY_TABLE_SET_S = 32;
    const uint64_t HISTORY_TABLE_WAY_S = 64;
    const uint64_t TABLE_SET_MASK_S = (1<<HISTORY_TABLE_SET_S)-1;
    const uint64_t BERTI_TABLE_SIZE_S = 64;
    const uint64_t BERTI_TABLE_STRIDE_SIZE_S = 16;
};
struct stride_info {
    int64_t stride;
    uint64_t conf;
    uint64_t prefetch_level; 
    uint64_t lru;
};
struct _Strides{
    vector<stride_info> conf_page_stride;
};

struct Berti_SETTING berti_setting;

struct stat_info{
    uint64_t ip_prefetch_nums;
    uint64_t page_prefetch_nums;
    uint64_t global_prefetch_nums;
    uint64_t prefetch_times;

    vector<uint64_t> ips;
    vector<uint64_t> pages;

    float mshr_occupancy;
    uint64_t access_times;

    uint64_t get_vector_max(vector<uint64_t> numbers){
        uint64_t maxIndex = 0;
        uint64_t maxValue = numbers[0];
        
        for (uint64_t i = 1; i < numbers.size(); i++) {
            if (numbers[i] > maxValue) {
                maxValue = numbers[i];
                maxIndex = i;
            }
        }
        return maxIndex;
    }


    uint64_t berti_long; //访问delta table，对应条目的总访问次数小于16
    bool berti_long_true;
    uint64_t berti_get;   //访问delta table，里面有一个条目
    uint64_t berti_access;//访问delta table总次数
    uint64_t berti_conf;//有conf delta的访问次数
    bool berti_conf_true;

    

    uint64_t page_long;
    bool page_long_true;
    uint64_t page_get;
    uint64_t page_access;
    uint64_t page_conf;
    bool page_conf_true;

    uint64_t offset_long;
    bool offset_long_true;
    uint64_t offset_get;
    uint64_t offset_access;
    uint64_t offset_conf;
    bool offset_conf_true;

    uint64_t global_long;
    bool global_long_true;
    uint64_t global_get;
    uint64_t global_access;
    uint64_t global_conf;
    bool global_conf_true;

    uint64_t all_long;
    uint64_t all_conf;


    void reset(){
        ip_prefetch_nums = 0;
        page_prefetch_nums = 0;
        global_prefetch_nums = 0;
        prefetch_times = 0;
        for(int i =0; i<16;i++){
            ips.push_back(0);
            pages.push_back(0);
        }
        mshr_occupancy = 0;
        access_times=0;
    
    berti_long = 0;
    berti_long_true = false;
    berti_get = 0;
    berti_access = 0;
    berti_conf = 0;
    berti_conf_true= false;



    page_long = 0;
    page_long_true = false;
    page_get = 0;
    page_access = 0;
    page_conf = 0;
    page_conf_true = false;

    offset_long = 0;
    offset_long_true = false;
    offset_get = 0;
    offset_access = 0;
    offset_conf = 0;
    offset_conf_true = false;

    global_long = 0;
    global_long_true = false;
    global_get = 0;
    global_access = 0;
    global_conf = 0;
    global_conf_true = false;

    all_long = 0;
    all_conf = 0;
    }

    
};
struct stat_info stat;
uint8_t warmup_flag_l1 = 0;

void notify_prefetch(uint64_t addr, uint64_t tag, uint32_t cpu, uint64_t cycle)
{
    //这个是预取时，进入到缺失状态寄存器的时间
    latency_table_add(addr, tag, cpu, 0, cycle & TIME_MASK);
}

bool compare_greater_stride_t(stride_t a, stride_t b)
{
    if (a.rpl == L1 && b.rpl != L1) return 1;
    else if (a.rpl != L1 && b.rpl == L1) return 0;
    else
    {
        if (a.rpl == L2 && b.rpl != L2) return 1;
        else if (a.rpl != L2 && b.rpl == L2) return 0;
        else
        {
            if (a.rpl == L2R && b.rpl != L2R) return 1;
            if (a.rpl != L2R && b.rpl == L2R) return 0;
            else
            {
                if (std::abs(a.stride) < std::abs(b.stride)) return 1;
                return 0;
            }
        }
    }
}

bool compare_greater_stride_t_per(stride_t a, stride_t b)
{
    if (a.per > b.per) return 1;
    else
    {
        if (std::abs(a.stride) < std::abs(b.stride)) return 1;
        return 0;
    }
}

/******************************************************************************/
/*                      Latency table functions                               */
/******************************************************************************/
void latency_table_init(uint32_t cpu)
{
    /*
     * Init pqmshr (latency) table
     *
     * Parameters:
     *      - cpu: cpu
     */
    for (uint32_t i = 0; i < LATENCY_TABLE_SIZE; i++)
    {
        latencyt[cpu][i].tag  = 0;
        latencyt[cpu][i].addr = 0;
        latencyt[cpu][i].time = 0;
        latencyt[cpu][i].pf   = 0;
    }
}

uint64_t latency_table_get_ip(uint64_t line_addr, uint32_t cpu)
{
    /*
     * Return 1 or 0 if the addr is or is not in the pqmshr (latency) table
     *
     * Parameters:
     *  - line_addr: address without cache offset
     *  - cpu: actual cpu
     *
     * Return: 1 if the line is in the latency table, otherwise 0
     */

    for (uint32_t i = 0; i < LATENCY_TABLE_SIZE; i++)
    {
        // Search if the line_addr already exists
        if (latencyt[cpu][i].addr == line_addr && latencyt[cpu][i].tag) 
            return latencyt[cpu][i].tag;
    }

    return 0;
}

uint8_t latency_table_add(uint64_t line_addr, uint64_t tag, uint32_t cpu, 
        uint8_t pf)
{
    /*
     * Save if possible the new miss into the pqmshr (latency) table
     *
     * Parameters:
     *  - line_addr: address without cache offset
     *  - cpu: actual cpu
     *  - access: is the entry accessed by a demand request
     */
    return latency_table_add(line_addr, tag, cpu, pf, current_core_cycle[cpu] & TIME_MASK);
}

uint8_t latency_table_add(uint64_t line_addr, uint64_t tag, uint32_t cpu, 
        uint8_t pf, uint64_t cycle)
{
    /*
     * Save if possible the new miss into the pqmshr (latency) table
     *
     * Parameters:
     *  - line_addr: address without cache offset
     *  - cpu: actual cpu
     *  - access: is theh entry accessed by a demand request
     *  - cycle: time to use in the latency table
     *
     * Return: 1 if the addr already exist, otherwise 0.
     */

    latency_table_t *free;
    free = nullptr;

    for (uint32_t i = 0; i < LATENCY_TABLE_SIZE; i++)
    {
        // Search if the line_addr already exists. If it exist we does not have
        // to do nothing more
        if (latencyt[cpu][i].addr == line_addr) 
        {
            latencyt[cpu][i].time = cycle;
            latencyt[cpu][i].tag  = tag;
            latencyt[cpu][i].pf   = pf;
            return latencyt[cpu][i].pf;
        }

        // We discover a free space into the latency table, save it for later
        //if (latencyt[cpu][i].addr == 0) free = &latencyt[cpu][i];
        if (latencyt[cpu][i].tag == 0) free = &latencyt[cpu][i];
    }

    // No free space!! This cannot be truth
    if (free == nullptr) return 0;

    // We save the new entry into the latency table
    free->addr = line_addr;
    free->time = cycle;
    free->tag  = tag;
    free->pf   = pf;

    return free->pf;
}

uint64_t latency_table_del(uint64_t line_addr, uint32_t cpu)
{
    /*
     * Remove the address from the latency table
     *
     * Parameters:
     *  - line_addr: address without cache offset
     *  - cpu: actual cpu
     *
     *  Return: the latency of the address
     */
    for (uint32_t i = 0; i < LATENCY_TABLE_SIZE; i++)
    {
        // Line already in the table
        if (latencyt[cpu][i].addr == line_addr)
        {
            uint64_t latency = (current_core_cycle[cpu] & TIME_MASK)
                - latencyt[cpu][i].time; // Calculate latency

            //latencyt[cpu][i].addr = 0; // Free the entry
            latencyt[cpu][i].tag  = 0; // Free the entry
            latencyt[cpu][i].time = 0; // Free the entry
            latencyt[cpu][i].pf   = 0; // Free the entry

            // Return the latency
            return latency;
        }
    }

    // We should always track the misses
    //assert(0);
    return 0;
}

uint64_t latency_table_get(uint64_t line_addr, uint32_t cpu)
{
    /*
     * Return 1 or 0 if the addr is or is not in the pqmshr (latency) table
     *
     * Parameters:
     *  - line_addr: address without cache offset
     *  - cpu: actual cpu
     *
     * Return: 1 if the line is in the latency table, otherwise 0
     */

    for (uint32_t i = 0; i < LATENCY_TABLE_SIZE; i++)
    {
        // Search if the line_addr already exists
        if (latencyt[cpu][i].addr == line_addr) return latencyt[cpu][i].time;
    }

    return 0;
}

/******************************************************************************/
/*                       Shadow Cache functions                               */
/******************************************************************************/
void shadow_cache_init(uint32_t cpu)
{
    /*
     * Init shadow cache
     *
     * Parameters:
     *      - cpu: cpu
     */
    for (uint8_t i = 0; i < L1D_SET; i++)
    {
        for (uint8_t ii = 0; ii < L1D_WAY; ii++)
        {
            scache[cpu][i][ii].addr = 0;
            scache[cpu][i][ii].lat  = 0;
            scache[cpu][i][ii].pf   = 0;
        }
    }
}

uint8_t shadow_cache_add(uint32_t cpu, uint32_t set, uint32_t way, 
        uint64_t line_addr, uint8_t pf, uint64_t latency)
{
    /*
     * Add block to shadow cache
     *
     * Parameters:
     *      - cpu: cpu
     *      - set: cache set
     *      - way: cache way
     *      - addr: cache block v_addr
     *      - access: the cache is access by a demand
     */
    scache[cpu][set][way].addr = line_addr;
    scache[cpu][set][way].pf   = pf;
    scache[cpu][set][way].lat  = latency;
    return scache[cpu][set][way].pf;
}

uint8_t shadow_cache_get(uint32_t cpu, uint64_t line_addr)
{
    /*
     * Init shadow cache
     *
     * Parameters:
     *      - cpu: cpu
     *      - addr: cache block v_addr
     *
     * Return: 1 if the addr is in the l1d cache, 0 otherwise
     */

    for (uint32_t i = 0; i < L1D_SET; i++)
    {
        for (uint32_t ii = 0; ii < L1D_WAY; ii++)
        {
            if (scache[cpu][i][ii].addr == line_addr) return 1;
        }
    }

    return 0;
}

uint8_t shadow_cache_pf(uint32_t cpu, uint64_t line_addr)
{
    /*
     * Init shadow cache
     *
     * Parameters:
     *      - cpu: cpu
     *      - addr: cache block v_addr
     *
     * Return: 1 if the addr is in the l1d cache, 0 otherwise
     */

    for (uint32_t i = 0; i < L1D_SET; i++)
    {
        for (uint32_t ii = 0; ii < L1D_WAY; ii++)
        {
            if (scache[cpu][i][ii].addr == line_addr) 
            {
                scache[cpu][i][ii].pf = 0;
                return 1;
            }
        }
    }

    return 0;
}

uint8_t shadow_cache_is_pf(uint32_t cpu, uint64_t line_addr)
{
    /*
     * Init shadow cache
     *
     * Parameters:
     *      - cpu: cpu
     *      - addr: cache block v_addr
     *
     * Return: 1 if the addr is in the l1d cache, 0 otherwise
     */

    for (uint32_t i = 0; i < L1D_SET; i++)
    {
        for (uint32_t ii = 0; ii < L1D_WAY; ii++)
        {
            if (scache[cpu][i][ii].addr == line_addr) return scache[cpu][i][ii].pf;
        }
    }

    return 0;
}

uint8_t shadow_cache_latency(uint32_t cpu, uint64_t line_addr)
{
    /*
     * Init shadow cache
     *
     * Parameters:
     *      - cpu: cpu
     *      - addr: cache block v_addr
     *
     * Return: 1 if the addr is in the l1d cache, 0 otherwise
     */

    for (uint32_t i = 0; i < L1D_SET; i++)
    {
        for (uint32_t ii = 0; ii < L1D_WAY; ii++)
        {
            if (scache[cpu][i][ii].addr == line_addr) return scache[cpu][i][ii].lat;
        }
    }
    assert(0);
    return 0;
}

uint64_t hash_index(uint64_t key, int index_len) {
    if (index_len == 0)
        return key;
    for (uint64_t tag = (key >> index_len); tag > 0; tag >>= index_len)
        key ^= tag & ((1 << index_len) - 1);
    return key;
}
struct Delta_info {
    int64_t stride;
    uint64_t conf;
    uint64_t prefetch_level; 
    uint64_t lru;
};
struct page_tmp_info{
    uint64_t offset;
    uint64_t timestamp;
    int way;
};
class AccululateTableData {
public:
    //history info
    deque<int> offsets;
    deque<uint64_t> timestamps;
    //strides info
    uint64_t total;
    vector<Delta_info> strides;
    uint64_t set_total;
    vector<Delta_info> set_strides;
};
bool compareByConf(const Delta_info& s1, const Delta_info& s2) {

    if(s1.prefetch_level != s2.prefetch_level){
        return s1.prefetch_level < s2.prefetch_level ;
    }else{
        return s1.conf > s2.conf;
    }
}
bool compareByOnlyConf(const Delta_info& s1, const Delta_info& s2) {
    return s1.conf > s2.conf;
}
class AccululateTable : public LRUSetAssociativeCache<AccululateTableData> {
    typedef LRUSetAssociativeCache<AccululateTableData> Super;
    public:
        AccululateTable(int size,int ways, int offset_number,int strides_number,
        uint64_t way_confidence_max, uint64_t way_l1_thres, uint64_t way_l2_thres, uint64_t way_llc_thres,
        uint64_t set_confidence_max, uint64_t set_l1_thres, uint64_t set_l2_thres, uint64_t set_llc_thres) : 
        Super(size,ways),offset_number(offset_number), strides_number(strides_number), 
        way_confidence_max(way_confidence_max),
        way_l1_thres(way_l1_thres),way_l2_thres(way_l2_thres),way_llc_thres(way_llc_thres),
        set_confidence_max(set_confidence_max),
        set_l1_thres(set_l1_thres),set_l2_thres(set_l2_thres),set_llc_thres(set_llc_thres){
            cerr<<"AccululateTable sets: "<< num_sets<<" ways: "<<num_ways<<endl;
        }
        void insert(uint64_t baddr, uint64_t pc, uint64_t timestamp){
            uint64_t region_number = baddr / PAGE_SIZE ;
            uint64_t offset = baddr % PAGE_SIZE;
            uint64_t key = this->build_key(pc,region_number);
            Entry *entry = Super::find(key);
            if(this->debug_level >= 2){
                cerr <<"[AT_insert]: region_number: "<< region_number <<" pc: " << pc << endl;
            }
            if(!entry){
                if(this->debug_level >= 2){
                    cerr <<"[AT_insert] no entry, insert" << endl;
                }
                deque<int> offsets;
                deque<uint64_t> timestamps;
                vector<Delta_info> strides;
                vector<Delta_info> set_strides;
                offsets.push_back(offset);
                timestamps.push_back(timestamp);
                Entry old_entry = Super::insert(key, {offsets,timestamps,0,strides,0,set_strides});
                Super::set_mru(key);
            }else{
                if(this->debug_level >= 2){
                    cerr <<"[AT_insert] find_entry,offset: "<< offset << endl;
                }
                Super::set_mru(key);
                for (size_t i = 0; i < entry->data.offsets.size(); ++i) {
                    if(entry->data.offsets[i] == offset){
                        return;
                    }
                } 
                
                entry->data.offsets.push_back(offset);
                entry->data.timestamps.push_back(timestamp);
                if(entry->data.offsets.size() > this->offset_number){
                    entry->data.offsets.pop_front();
                    entry->data.timestamps.pop_front();
                }
            }
        }

        int update_stride(uint64_t baddr, uint64_t pc, uint64_t latency, uint64_t cycle){
            uint64_t region_number = baddr / PAGE_SIZE;
            uint64_t offset = baddr % PAGE_SIZE;
            uint64_t key = this->build_key(pc,region_number);
            Entry *entry = Super::find(key);
            if(cycle < latency) return 0;
            cycle = cycle - latency;
            if(!entry){
            }else{
                this->set_mru(key);
                int get_stride = 0;
                for (size_t i = entry->data.offsets.size() ; i-- > 0; ) {
                    if( entry->data.timestamps[i] < cycle ){
                        int delta= offset - entry->data.offsets[i];                       
                        if(delta != 0 && std::abs(delta) < (1 << STRIDE_MASK) && get_stride <= 5){
                            this->way_stride_add(key, delta);
                            get_stride += 1;
                        }
                        if(this->debug_level>=2){
                            cerr  << "[AT_update_stride_way] delta: " << delta<<" cur_offset: " << offset<<" history_offset "<<entry->data.offsets[i]  << ", latency: " << latency << " cycle: "<< cycle <<endl;
                        }   
                    }      
                }
                
            }
            if(this->debug_level>=2){
                cerr  << "[AT_update_stride] update_set " << endl;
            }
            uint64_t index = key % this->num_sets;
            int cnt = 0;
            
            vector<page_tmp_info> tmp_offsets;
            for(uint32_t i = 0; i < this->num_ways; i += 1){
                Entry &entry1 = this->entries[index][i];
                Entry *entrys = &entry1;
                if(entrys->valid){
                    for(uint32_t j = 0; j < entrys->data.offsets.size(); j++){
                        if(entrys->data.timestamps[j] < cycle){
                            page_tmp_info tmp_offset_way;
                            tmp_offset_way.offset = entrys->data.offsets[j];
                            tmp_offset_way.timestamp = entrys->data.timestamps[j];
                            tmp_offset_way.way = i;
                            tmp_offsets.push_back(tmp_offset_way);
                            
                        }
                    }
                }
            }
            std::sort(tmp_offsets.begin(), tmp_offsets.end(),
              [](const page_tmp_info &a, const page_tmp_info &b) {
                  return a.timestamp > b.timestamp; // 降序排序
              });

            while(tmp_offsets.size() > 16){
                tmp_offsets.pop_back();
            }
            for(int i = 0; i < tmp_offsets.size(); i++){
                int delta= offset - tmp_offsets[i].offset; 
                if(delta != 0 && std::abs(delta) < 64){
                    this->set_stride_add(index, tmp_offsets[i].way, delta);
                    cnt ++;
                }
                if(this->debug_level>=2){
                    cerr  << "[AT_update_stride_set] delta: " << delta<<" cur_offset: " << offset<<" history_offset "<<entry->data.offsets[i]  << ", latency: " << latency << " cycle: "<< cycle <<endl;
                } 
            }

            return cnt;
        }

        int way_stride_add(uint64_t key, int64_t delta){
            Entry *entry = Super::find(key);
            for (size_t j = 0; j < entry->data.strides.size(); j++){
                if(entry->data.strides[j].stride == delta){
                    entry->data.strides[j].conf += CONFIDENCE_INC;
                    if (entry->data.strides[j].conf > CONFIDENCE_MAX) {
                        entry->data.strides[j].conf = CONFIDENCE_MAX;
                    }
                    return 1;
                }
            }
            std::sort(entry->data.strides.begin(), entry->data.strides.end(),compareByConf);
            if(entry->data.strides.size() >= this->strides_number){
                entry->data.strides.pop_back();
            }
            entry->data.strides.push_back({delta, 0,NO_PREFETCH,entry->data.total});
        }

        void set_stride_add(uint64_t index, uint64_t way, int64_t delta){
            Entry &entry1 = this->entries[index][way];
            Entry *entry = &entry1;
            for (size_t j = 0; j < entry->data.set_strides.size(); j++){
                if(entry->data.set_strides[j].stride == delta){
                    entry->data.set_strides[j].conf += CONFIDENCE_INC;
                    if (entry->data.set_strides[j].conf > CONFIDENCE_MAX) {
                        entry->data.set_strides[j].conf = CONFIDENCE_MAX;
                        return;
                    }
                }
            }
            std::sort(entry->data.set_strides.begin(), entry->data.set_strides.end(),compareByConf);
            if(entry->data.set_strides.size() >= this->strides_number){
                entry->data.set_strides.pop_back();
            }
            entry->data.set_strides.push_back({delta, 0,NO_PREFETCH,entry->data.set_total});
        }

        void add_way_conf(uint64_t baddr, int64_t pc){
            if(this->debug_level>=2){
                cerr  << "[AT_add_way_conf]" << endl;
            }
            uint64_t region_number = baddr / PAGE_SIZE ;
            uint64_t offset = baddr % PAGE_SIZE;
            uint64_t key = this->build_key(pc,region_number);
            Entry *entry = Super::find(key);
            if(!entry){
                if(this->debug_level>=2){
                    cerr  << "[AT] t entry : no way found" <<endl;
                }  
            }
            else{
                entry->data.total = entry->data.total + 1;
                if(entry->data.total == way_confidence_max){
                    for(auto& pair: entry->data.strides){
                        float conf_rate = 1.0*pair.conf / entry->data.total;
                        
                        if(conf_rate > way_l1_thres){
                            if(this->debug_level>=2 ){
                                cerr  << "set_find_stride_conf: "<<conf_rate<<endl;
                            }
                            pair.prefetch_level = L1;
                        }else if(conf_rate > way_l2_thres){
                            if(this->debug_level>=2 ){
                                cerr  << "set_find_stride_conf: "<<conf_rate<<endl;
                            }
                            pair.prefetch_level = L2;
                        }else if(conf_rate > way_llc_thres){
                            if(this->debug_level>=2 ){
                                cerr  << "set_find_stride_conf: "<<conf_rate<<endl;
                            }
                            pair.lru = L2R;
                        }else{
                            pair.prefetch_level = NO_PREFETCH;
                        }
                        if(this->debug_level >= 2){
                            cerr << '[AT_way_conf]:'<< endl;
                        }
                        pair.conf = 0;
                        pair.lru = 0;
                    }
                    entry->data.total = 1;
                }
            }
        }

        void add_set_conf(uint64_t baddr, int64_t pc){
            if(this->debug_level>=2){
                cerr  << "[AT_add_set_conf]" << endl;
            }
            uint64_t region_number = baddr / PAGE_SIZE;
            uint64_t offset = baddr % PAGE_SIZE;
            uint64_t key = this->build_key(pc,region_number);
            uint64_t index = key % this->num_sets;
            int cnt = 0;
            for(uint32_t i = 0; i < this->num_ways; i += 1){
                Entry &entry1 = this->entries[index][i];
                Entry *entry = &entry1;
                if(entry->valid){
                    entry->data.set_total = entry->data.set_total + 1;
                    if(entry->data.set_total == set_confidence_max){
                        for(auto& pair: entry->data.set_strides){
                            float conf_rate = 1.0*pair.conf / entry->data.set_total;
                            if(conf_rate > set_l1_thres){
                                pair.prefetch_level = L1;
                            }else if(conf_rate > set_l2_thres){
                                pair.prefetch_level = L2;
                            }else if(conf_rate > set_llc_thres){
                                pair.lru = L2R;
                            }else{
                                pair.prefetch_level = NO_PREFETCH;
                            }
                            if(this->debug_level >= 2){
                                cerr << '[AT_add_set_conf]:'<<" set: " << index << " way: "<< i << endl;
                            }
                            pair.conf = 0;
                            pair.lru = 0;
                        }
                        entry->data.set_total = 1;
                    }
                }              
            }
        }

        vector<Delta_info> get_conf_stride(uint64_t baddr, uint64_t pc){
            vector<Delta_info> conf_stride;
            uint64_t region_number = baddr / PAGE_SIZE;
            uint64_t offset = baddr % PAGE_SIZE;
            uint64_t key = this->build_key(pc,region_number);
            uint64_t index = key % this->num_sets;
            Entry *entry = Super::find(key);
            if (!entry){
                // return 0;
                 if(this->debug_level>=2){
                    cerr  << "[AT_get_stride] way not found"<<endl;
                 }
            }else{
                std::sort(entry->data.strides.begin(), entry->data.strides.end(), compareByConf);
                // cerr  << "[PST] get conf stride: "  << " page number: "<< region_num <<", size: " << entry->data.stride_conf.size() <<" total: "<< entry->data.total <<endl;
                for ( auto& pair : entry->data.strides) {
                    if(pair.stride!=0 && pair.prefetch_level < NO_PREFETCH){
                        
                        conf_stride.push_back({pair.stride, pair.conf, pair.prefetch_level});
                        
                    }
                }

                if( conf_stride.size() ==0 && entry->data.total >= LANZAR_INT){
                    std::sort(entry->data.strides.begin(), entry->data.strides.end(), compareByOnlyConf);
                    for ( auto& pair : entry->data.strides) {
                        float conf_rate = 1.0*pair.conf/entry->data.total ;
                        if( conf_rate > way_l1_thres+0.15 ){
                            conf_stride.push_back({pair.stride, pair.conf, L1});
                        }else if(conf_rate > way_l2_thres+0.15){
                            conf_stride.push_back({pair.stride, pair.conf, L2});
                        }else{
                            break;
                        }
                    }
                }
                if(this->debug_level>=2 && conf_stride.size() == 0){
                    cerr  << "[AT_get_stride] way not found, start find set"<<endl;
                }
                if(conf_stride.size() == 0){
                    for(size_t i = 0; i < this->num_ways; i += 1){
                        Entry &entry1 = this->entries[index][i];
                        Entry *entrys = &entry1;
                        if(entrys->valid){
                            for ( auto& pair : entrys->data.set_strides) {
                                if(pair.stride!=0 && pair.prefetch_level < NO_PREFETCH){
                                    bool find_stride = false;
                                    for(auto delta: conf_stride){
                                        if(delta.stride == pair.stride){
                                            find_stride = true;
                                            break;
                                        }
                                    }
                                    if(!find_stride){
                                        if(this->debug_level>=2 && conf_stride.size() == 0){
                                            cerr  << "set_find_stride: "<<pair.stride << " conf: " << pair.conf <<endl;
                                        }
                                        conf_stride.push_back({pair.stride, pair.conf, pair.prefetch_level});
                                    }
                                }
                            }
                        }

                        if( conf_stride.size() ==0 && entrys->data.set_total >= LANZAR_INT){
                            std::sort(entrys->data.set_strides.begin(), entrys->data.set_strides.end(), compareByOnlyConf);
                            for ( auto& pair : entrys->data.set_strides) {
                                float conf_rate = 1.0*pair.conf/entrys->data.set_total ;
                                bool find_stride = false;
                                if( conf_rate > set_l1_thres+0.15 ){
                                    for(size_t j = 0; j < conf_stride.size(); j++){
                                        if(conf_stride[j].stride == pair.stride){
                                            find_stride = true;
                                            break;                               
                                        }
                                    }
                                    if(!find_stride){
                                        if(this->debug_level>=2 && conf_stride.size() == 0){
                                            cerr  << "set_find_stride: "<<pair.stride << " conf: " << pair.conf <<endl;
                                        }
                                        conf_stride.push_back({pair.stride, pair.conf, L1});
                                    }
                                }else if(conf_rate > set_l2_thres+0.15){
                                    for(size_t j = 0; j < conf_stride.size(); j++ ){
                                        if(conf_stride[j].stride == pair.stride){
                                            find_stride = true;
                                            break;
                                        }
                                    }
                                    if(!find_stride){
                                        if(this->debug_level>=2 && conf_stride.size() == 0){
                                            cerr  << "set_find_stride: "<<pair.stride << " conf: " << pair.conf <<endl;
                                        }
                                        conf_stride.push_back({pair.stride, pair.conf, L2});
                                    }
                                }else{
                                    break;
                                }
                            }
                        }            
                    }
                }
                std::sort(conf_stride.begin(), conf_stride.end(), compareByConf);
                while(conf_stride.size() > this->offset_number){
                    conf_stride.pop_back();
                }
                if(this->debug_level>=2 ){
                    cerr << "[AT strides]: ";
                    for(size_t i = 0; i < conf_stride.size(); i++ ){
                        cerr << conf_stride[i].stride << " ";
                    }
                    cerr << endl;
                }             
            }
            return conf_stride;
        }
    private:
        uint64_t build_key(uint64_t pc, uint64_t region_number){
            //use region number to index, and use pc to tag
            pc = (pc >> 1)^(pc >> 4);
            pc &= IP_MASK;
            uint64_t index_key = hash_index(region_number, this->index_len);
            uint64_t key = (pc <<(this->index_len)) | index_key;
            return key;
        };
        uint64_t offset_number;
        uint64_t strides_number;
        uint64_t way_confidence_max;
        uint64_t way_l1_thres;
        uint64_t way_l2_thres;
        uint64_t way_llc_thres;
        uint64_t set_confidence_max;
        uint64_t set_l1_thres;
        uint64_t set_l2_thres;
        uint64_t set_llc_thres;
};



class StrideCountTableData {
  public:
    uint64_t cnt;
};

class StrideCountTable : public LRUFullyAssociativeCache<StrideCountTableData> {
    typedef LRUFullyAssociativeCache<StrideCountTableData> Super;
  public:
    StrideCountTable(int size, float threshold, uint64_t interval) : Super(size), global_threshold(threshold), interval(interval) {
        total_cnt = 0;
        select_stride = 0;
        rate = 0;
        cur_max = 0;
        cerr<<"StrideCountTable sets: "<< num_sets<<" ways: "<<num_ways<<endl;
        // assert(__builtin_popcount(size) == 1);
        // assert(__builtin_popcount(pattern_len) == 1);
    }
    uint64_t get_cnt(){
        return this->select_stride;
    }

    float get_threshold(){
        return rate;
    }

    uint64_t add_cnt(uint64_t pattern_number) {
        this->total_cnt++;
        if(this->total_cnt > this->interval && this->interval != 0 ){
            reset();
        }
        Entry *entry = Super::find(pattern_number);
        if (!entry){
            // assert(0);
            Entry victim =  Super::insert(pattern_number, {1});
            this->set_mru(pattern_number);
            // traverse_entry();
            if (this->debug_level >= 2) {
                cerr << "[Bingo] StrideCountTable insert stride: "   << " stride: " << pattern_number << endl;
                if(victim.valid){
                    cerr << "[Bingo] StrideCountTable replace stride: "   << victim.tag <<", cnt: "<< victim.data.cnt  << endl;
                }
                
            }
            return 1;
        }
        entry->data.cnt = entry->data.cnt + 1 ;
        // if(entry->data.cnt > cur_max){
        //     cur_max = entry->data.cnt;
        //     this->select_stride = pattern_number;
            
        // }

        // this->rate = 1.0 * cur_max /( this->total_cnt+1);
        this->rate = 1.0 * entry->data.cnt / this->total_cnt;
        if( rate > this->global_threshold){
            this->select_stride = pattern_number;
        }
        this->set_mru(pattern_number);
        // traverse_entry();
        if (this->debug_level >= 2) {
            cerr  << "[Bingo] StrideCountTable add cnt: "   << " stride: " << int64_t(entry->tag) <<", cnt: "<< entry->data.cnt << endl;
        }
        return entry->data.cnt;
    }

    void traverse_entry(){
        auto &set = this->entries[0];
        for (int i = 0; i < num_ways; i += 1){
            if (set[i].valid){
                cerr<<"Traverse way: "<< i<< ", tag : "<< set[i].tag <<" cnt: " << set[i].data.cnt <<" lru: " << (*get_lru(0,i))<<endl;
            }
        }    
    }

    void set_debug_level(int debug_level) { this->debug_level = debug_level; }

    bool reset() {
        auto &set = this->entries[0];
        auto &cam = cams[0];
        // assert(set.size() == size);
        assert(this->num_sets == 1);
        assert(this->num_ways == size);
        for (int i = 0; i < num_ways; i += 1){
            if (set[i].valid){
                set[i].valid =false;
            }
        }

        cam.clear();
        this->total_cnt = 1;
        this->select_stride = 0;
        this->rate = 0;
        this->cur_max = 0;
        return true;
    }

    private:
        uint64_t total_cnt;
        float global_threshold;
        uint64_t interval;
        uint64_t select_stride;
        uint64_t cur_max;
        float rate;


};


class MIX {
  public:

    MIX(struct PAGE_SETTING setting)
        : setting(setting),
        at(setting.ACCUMULATE_TABLE,setting.ACCUMULATE_WAYS, 
        setting.OFFSET_NUMBER, setting.STRIDES_NUMBER,
        setting.WAY_CONFIDENCE_MAX, 
        setting.WAY_L1_THRESHOLD, setting.WAY_L2_THRESHOLD, setting.WAY_LLC_THRESHOLD,
        setting.SET_CONFIDENCE_MAX, 
        setting.SET_L1_THRESHOLD, setting.SET_L2_THRESHOLD, setting.SET_LLC_THRESHOLD
        ),
        pct(setting.STRIDE_COUNT_TABLE, setting.GLOBAL_STRIDE_THRESHOLD, setting.INTERVAL){   
            cerr << dec << "MIX_START" << endl;
        }
       
    void insert_pct(uint64_t stride){
        pct.add_cnt(stride);
    }

    uint64_t get_pct(){
        return this->pct.get_cnt();
    }



    vector<Delta_info> access(uint32_t cpu, uint64_t line_addr, uint8_t cache_hit,uint64_t pc){

        uint64_t block_number =  line_addr;
        uint64_t cycle = current_core_cycle[cpu] & TIME_MASK;
        if (this->debug_level >= 2) {
            cerr << "[MIX] access "<<" cache_hit: "   << (cache_hit==1) <<" pf: " << (shadow_cache_is_pf(cpu, block_number) == 1 )<<", cycle "<< cycle  << endl;
        }

        uint64_t page_number = block_number >> 6;
        uint64_t offset = block_number % (1 << 6);


        if (!cache_hit){
            if(spec_intructions_complete && this->debug_level >= 2)
            {
                std::cout <<  "pc:"<<pc<<" ";
                std::cout << "offset:"<<offset<<" ";
                std::cout << "baddr:"<< line_addr<<" ";
                std::cout << "vpaddr:"<< page_number<<" ";
                std::cout << "M" << std::endl;
            }
            latency_table_add(line_addr, pc, cpu, 1);
            at.insert(line_addr, pc, cycle);
            
        }else if (cache_hit && shadow_cache_is_pf(cpu, line_addr)){
            if(spec_intructions_complete && this->debug_level >= 2)
            {
                std::cout <<"pc:"<<pc<<" ";
                std::cout << "offset:"<<offset<<" ";
                std::cout << "baddr:"<< line_addr<<" ";
                std::cout << "vpaddr:"<<page_number<<" ";
                std::cout << "PH" << std::endl;
            }
            at.insert(line_addr, pc, cycle);
            uint64_t latency = shadow_cache_latency(cpu, line_addr);
            at.add_way_conf(line_addr,pc);
            at.add_set_conf(line_addr, pc);
            at.update_stride(line_addr,pc, latency, cycle);

        }else{
            if(spec_intructions_complete && this->debug_level >= 2)
            {
                std::cout <<"pc:"<<pc<<" ";
                std::cout << "offset:"<<offset<<" ";
                std::cout << "baddr:"<< line_addr<<" ";
                std::cout << "vpaddr:"<<page_number<<" ";
                std::cout << "H" << std::endl;
            }
            shadow_cache_pf(cpu, line_addr);
        }   
        vector<Delta_info> strides;
        strides= at.get_conf_stride(line_addr,pc);
        return strides;
    }

     void cache_fill(uint64_t baddr, uint64_t pc,uint64_t latency, uint64_t cycle){
        at.add_way_conf(baddr,pc);
        at.add_set_conf(baddr, pc);
        at.update_stride(baddr,pc, latency, cycle);
    }

    float get_global_rate(){
        return this->pct.get_threshold();
    }


    void set_debug_level(int debug_level) { 
        this->debug_level = debug_level; 
        at.set_debug_level(debug_level);
        pct.set_debug_level(debug_level);
    }
    
    private:
        struct PAGE_SETTING setting;
        AccululateTable at;
        StrideCountTable pct;
        int debug_level = 0;

};

vector<MIX> prefetchers;


struct PAGE_SETTING setting;

void CACHE::l1d_prefetcher_initialize() 
{
    shadow_cache_init(cpu);
    latency_table_init(cpu);

    stat.reset();

    prefetchers = vector<MIX>(NUM_CPUS, MIX(setting));
    for(int i =0; i<NUM_CPUS; i++){
        prefetchers[i].set_debug_level(0);
    }
    
    
    spec_intructions_complete = false;

}
bool set_debug = false;
void CACHE::l1d_prefetcher_operate(uint64_t addr, uint64_t ip, uint8_t cache_hit,
        uint8_t type, uint8_t critical_ip_flag)
{
    if((!set_debug) && spec_intructions_complete == true){
        for(int i =0; i<NUM_CPUS; i++){
            prefetchers[i].set_debug_level(0);
        }

        set_debug = true;
    }
    
    assert(type == LOAD || type == RFO);

    if(warmup_complete[cpu] && warmup_flag_l1 == 0){
        stat.reset();
        warmup_flag_l1 = 1;
    }

    uint64_t line_addr = (addr >> LOG2_BLOCK_SIZE); // Line addr
    uint64_t pc = ip;
 
    vector<Delta_info> strides;
    // cerr<<"here"<<endl;
    // conf_stride = prefetchers[cpu].get_conf_stride(line_addr);
    strides = prefetchers[cpu].access(cpu, line_addr, cache_hit,pc);

    if((1.0 * MSHR.occupancy / (float) MSHR_SIZE) == 1 ){
        stat.mshr_occupancy++;
    }
    stat.access_times++;
    int total_prefetch = 0;

    int launched = 0;
    for ( auto& stride_info : strides) {
        if( launched >= setting.ALL_MAX_PF ){
            break;
        }    
        uint64_t p_addr = (line_addr + stride_info.stride) << LOG2_BLOCK_SIZE;
        uint64_t p_b_addr = (p_addr >> LOG2_BLOCK_SIZE);

        if (!latency_table_get(p_addr, cpu)){
            int fill_level = FILL_L1;
            float mshr_load = ((float) MSHR.occupancy / (float) MSHR_SIZE) * 100;
            if (stride_info.prefetch_level == L1 && mshr_load < MSHR_LIMIT){
                fill_level = FILL_L1;
            } else if (stride_info.prefetch_level == L2 ){ 
                fill_level = FILL_L2;
            } else  if ( stride_info.prefetch_level == L2R ){
                fill_level = FILL_LLC;
            }else{
                break;
            }

            if (prefetch_line(pc, addr, p_addr, fill_level, 1)){
                if(fill_level == FILL_L1){
                    prefetchers[cpu].insert_pct(static_cast<uint64_t>(stride_info.stride));
                    // if(spec_intructions_complete)
                    // {
                    //     cerr << "insert global stride: " << stride_info.stride << endl;
                    // }
                }
                launched++;
                total_prefetch++;
            }

        }
    }
    stat.page_prefetch_nums+=launched;
    if(launched!=0){
        stat.pages[launched]++;
    }
     
    int64_t global_stride = static_cast<int64_t>(prefetchers[cpu].get_pct());
    // if(spec_intructions_complete)
    // {
    //     cerr << "global stride: " << global_stride << endl;
    // }
    if(global_stride!=0 && (launched < setting.ALL_MAX_PF)){
        int fill_level = -1;
        if(prefetchers[cpu].get_global_rate() > setting.GLOBAL_STRIDE_THRESHOLD ){
             fill_level = FILL_L2;
        } else if(prefetchers[cpu].get_global_rate() > setting.GLOBAL_STRIDE_THRESHOLD_LLC ){
             fill_level = FILL_LLC;
        } 
    }
    stat.global_prefetch_nums+= total_prefetch - (launched);

    if(total_prefetch != 0){
        stat.prefetch_times++;
    }
    
}

void CACHE::l1d_prefetcher_notify_about_dtlb_eviction(uint64_t addr, 
        uint32_t set, uint32_t way, uint8_t prefetch, uint64_t evicted_addr, 
        uint32_t metadata_in)
{

}

void CACHE::l1d_prefetcher_cache_fill(uint64_t v_addr, uint64_t addr, 
        uint32_t set, uint32_t way, uint8_t prefetch, uint64_t v_evicted_addr, 
        uint64_t evicted_addr, uint32_t metadata_in)
{
    uint64_t line_addr = (v_addr >> LOG2_BLOCK_SIZE); // Line addr
    uint64_t line_evicted = (v_evicted_addr >> LOG2_BLOCK_SIZE); // Line addr

    // Remove @ from latency table
    uint64_t pc     = latency_table_get_ip(line_addr, cpu);
    uint64_t cycle   = latency_table_get(line_addr, cpu);
    uint64_t latency = latency_table_del(line_addr, cpu);

    if (latency > LAT_MASK) latency = 0;

    // Add to the shadow cache
    shadow_cache_add(cpu, set, way, line_addr, prefetch, latency);

    if (latency != 0 && !prefetch)
    {
        prefetchers[cpu].cache_fill(line_addr,pc, latency, cycle);
    }

}

void CACHE::l1d_prefetcher_final_stats()
{
    cout << "* CPU " << "0" << " ROI ip prefetch number: " << stat.ip_prefetch_nums << endl;
    cout << "* CPU " << "0" << " ROI page prefetch number: " << stat.page_prefetch_nums << endl;
    cout << "* CPU " << "0" << " ROI global prefetch number: " << stat.global_prefetch_nums << endl;
    cout << "* CPU " << "0" << " ROI prefetch times: " << stat.prefetch_times << endl;

    int maxIndex = 0;
    int maxValue = stat.ips[0];


    cout << "* CPU " << "0" << " ROI ip prefetch degree: " << stat.get_vector_max(stat.ips) << endl;

    cout << "* CPU " << "0" << " ROI page prefetch degree: " << stat.get_vector_max(stat.pages) << endl;

    cout << "* CPU " << "0" << " ROI mshr occupancy: " << (stat.mshr_occupancy) << endl;
    cout << "* CPU " << "0" << " ROI access times: " << (stat.access_times) << endl;

    cout << "* CPU " << "0" << "berti:" << stat.berti_long<<" "<<stat.berti_get<<" "<<stat.berti_access<<" "<<stat.berti_conf<<std::endl;
    cout << "* CPU " << "0" << "all:" << stat.all_long << " "<<stat.all_conf<<std::endl;
}








