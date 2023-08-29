#include "vbertim.h"
#include <sstream>
#include <iostream> //reocrd
#include <fstream>//record

#include <bits/stdc++.h>
#include <mutex> //atom ops
#include <unordered_map>
#include <unordered_set>

//******debug开关********//
#define RECORD_IP_ADDR false
#define RECORD_DELTAS false
#define LANZAR_INT 8

//******预取器开关*********//
//#define BERTI_IP_ON
//#define BERTI_PAGES_ON
//#define BINGO_BOP_ON
//#define MLOP_ON


//#define BOP_ON
#ifdef BINGO_BOP_ON
    #define CONSTRAIN_BOP
    //#define CP_BINGO_BOP_ON
    #define BOP_L1
    //#define BOP_L2
    //#define BOP_DEBUG
#endif


std::mutex mtx;
#ifdef MLOP_ON
namespace L1D_PREF_2 {

/**
 * A class for printing beautiful data tables.
 * It's useful for logging the information contained in tabular structures.
 */
class Table {
  public:
    Table(int width, int height) : width(width), height(height), cells(height, vector<string>(width)) {}

    void set_row(int row, const vector<string> &data, int start_col = 0) {
        // assert(data.size() + start_col == this->width);
        for (unsigned col = start_col; col < this->width; col += 1)
            this->set_cell(row, col, data[col]);
    }

    void set_col(int col, const vector<string> &data, int start_row = 0) {
        // assert(data.size() + start_row == this->height);
        for (unsigned row = start_row; row < this->height; row += 1)
            this->set_cell(row, col, data[row]);
    }

    void set_cell(int row, int col, string data) {
        // assert(0 <= row && row < (int)this->height);
        // assert(0 <= col && col < (int)this->width);
        this->cells[row][col] = data;
    }

    void set_cell(int row, int col, double data) {
        ostringstream oss;
        oss << setw(11) << fixed << setprecision(8) << data;
        this->set_cell(row, col, oss.str());
    }

    void set_cell(int row, int col, int64_t data) {
        ostringstream oss;
        oss << setw(11) << std::left << data;
        this->set_cell(row, col, oss.str());
    }

    void set_cell(int row, int col, int data) { this->set_cell(row, col, (int64_t)data); }

    void set_cell(int row, int col, uint64_t data) {
        ostringstream oss;
        oss << "0x" << setfill('0') << setw(16) << hex << data;
        this->set_cell(row, col, oss.str());
    }

    /**
     * @return The entire table as a string
     */
    string to_string() {
        vector<int> widths;
        for (unsigned i = 0; i < this->width; i += 1) {
            int max_width = 0;
            for (unsigned j = 0; j < this->height; j += 1)
                max_width = max(max_width, (int)this->cells[j][i].size());
            widths.push_back(max_width + 2);
        }
        string out;
        out += Table::top_line(widths);
        out += this->data_row(0, widths);
        for (unsigned i = 1; i < this->height; i += 1) {
            out += Table::mid_line(widths);
            out += this->data_row(i, widths);
        }
        out += Table::bot_line(widths);
        return out;
    }

    string data_row(int row, const vector<int> &widths) {
        string out;
        for (unsigned i = 0; i < this->width; i += 1) {
            string data = this->cells[row][i];
            data.resize(widths[i] - 2, ' ');
            out += " | " + data;
        }
        out += " |\n";
        return out;
    }

    static string top_line(const vector<int> &widths) { return Table::line(widths, "┌", "┬", "┐"); }

    static string mid_line(const vector<int> &widths) { return Table::line(widths, "├", "┼", "┤"); }

    static string bot_line(const vector<int> &widths) { return Table::line(widths, "└", "┴", "┘"); }

    static string line(const vector<int> &widths, string left, string mid, string right) {
        string out = " " + left;
        for (unsigned i = 0; i < widths.size(); i += 1) {
            int w = widths[i];
            for (int j = 0; j < w; j += 1)
                out += "─";
            if (i != widths.size() - 1)
                out += mid;
            else
                out += right;
        }
        return out + "\n";
    }

  private:
    unsigned width;
    unsigned height;
    vector<vector<string>> cells;
};

template <class T> class SetAssociativeCache {
  public:
    class Entry {
      public:
        uint64_t key;
        uint64_t index;
        uint64_t tag;
        bool valid;
        T data;
    };

    SetAssociativeCache(int size, int num_ways, int debug_level = 0)
        : size(size), num_ways(num_ways), num_sets(size / num_ways), entries(num_sets, vector<Entry>(num_ways)),
          cams(num_sets), debug_level(debug_level) {
        // assert(size % num_ways == 0);
        for (int i = 0; i < num_sets; i += 1)
            for (int j = 0; j < num_ways; j += 1)
                entries[i][j].valid = false;
        /* calculate `index_len` (number of bits required to store the index) */
        for (int max_index = num_sets - 1; max_index > 0; max_index >>= 1)
            this->index_len += 1;
    }

    /**
     * Invalidates the entry corresponding to the given key.
     * @return A pointer to the invalidated entry
     */
    Entry *erase(uint64_t key) {
        Entry *entry = this->find(key);
        uint64_t index = key % this->num_sets;
        uint64_t tag = key / this->num_sets;
        auto &cam = cams[index];
        int num_erased = cam.erase(tag);
        if (entry)
            entry->valid = false;
        // assert(entry ? num_erased == 1 : num_erased == 0);
        return entry;
    }

    /**
     * @return The old state of the entry that was updated
     */
    Entry insert(uint64_t key, const T &data) {
        Entry *entry = this->find(key);
        if (entry != nullptr) {
            Entry old_entry = *entry;
            entry->data = data;
            return old_entry;
        }
        uint64_t index = key % this->num_sets;
        uint64_t tag = key / this->num_sets;
        vector<Entry> &set = this->entries[index];
        int victim_way = -1;
        for (int i = 0; i < this->num_ways; i += 1)
            if (!set[i].valid) {
                victim_way = i;
                break;
            }
        if (victim_way == -1) {
            victim_way = this->select_victim(index);
        }
        Entry &victim = set[victim_way];
        Entry old_entry = victim;
        victim = {key, index, tag, true, data};
        auto &cam = cams[index];
        if (old_entry.valid) {
            int num_erased = cam.erase(old_entry.tag);
            // assert(num_erased == 1);
        }
        cam[tag] = victim_way;
        return old_entry;
    }

    Entry *find(uint64_t key) {
        uint64_t index = key % this->num_sets;
        uint64_t tag = key / this->num_sets;
        auto &cam = cams[index];
        if (cam.find(tag) == cam.end())
            return nullptr;
        int way = cam[tag];
        Entry &entry = this->entries[index][way];
        // assert(entry.tag == tag && entry.valid);
        return &entry;
    }

    /**
     * Creates a table with the given headers and populates the rows by calling `write_data` on all
     * valid entries contained in the cache. This function makes it easy to visualize the contents
     * of a cache.
     * @return The constructed table as a string
     */
    string log(vector<string> headers) {
        vector<Entry> valid_entries = this->get_valid_entries();
        Table table(headers.size(), valid_entries.size() + 1);
        table.set_row(0, headers);
        for (unsigned i = 0; i < valid_entries.size(); i += 1)
            this->write_data(valid_entries[i], table, i + 1);
        return table.to_string();
    }

    int get_index_len() { return this->index_len; }

    void set_debug_level(int debug_level) { this->debug_level = debug_level; }

  protected:
    /* should be overriden in children */
    virtual void write_data(Entry &entry, Table &table, int row) {}

    /**
     * @return The way of the selected victim
     */
    virtual int select_victim(uint64_t index) {
        /* random eviction policy if not overriden */
        return rand() % this->num_ways;
    }

    vector<Entry> get_valid_entries() {
        vector<Entry> valid_entries;
        for (int i = 0; i < num_sets; i += 1)
            for (int j = 0; j < num_ways; j += 1)
                if (entries[i][j].valid)
                    valid_entries.push_back(entries[i][j]);
        return valid_entries;
    }

    int size;
    int num_ways;
    int num_sets;
    int index_len = 0; /* in bits */
    vector<vector<Entry>> entries;
    vector<unordered_map<uint64_t, int>> cams;
    int debug_level = 0;
};

template <class T> class LRUSetAssociativeCache : public SetAssociativeCache<T> {
    typedef SetAssociativeCache<T> Super;

  public:
    LRUSetAssociativeCache(int size, int num_ways, int debug_level = 0)
        : Super(size, num_ways, debug_level), lru(this->num_sets, vector<uint64_t>(num_ways)) {}

    void set_mru(uint64_t key) { *this->get_lru(key) = this->t++; }

    void set_lru(uint64_t key) { *this->get_lru(key) = 0; }

  protected:
    /* @override */
    int select_victim(uint64_t index) {
        vector<uint64_t> &lru_set = this->lru[index];
        return min_element(lru_set.begin(), lru_set.end()) - lru_set.begin();
    }

    uint64_t *get_lru(uint64_t key) {
        uint64_t index = key % this->num_sets;
        uint64_t tag = key / this->num_sets;
        // assert(this->cams[index].count(tag) == 1);
        int way = this->cams[index][tag];
        return &this->lru[index][way];
    }

    vector<vector<uint64_t>> lru;
    uint64_t t = 1;
};

/**
 * A very simple and efficient hash function that:
 * 1) Splits key into blocks of length `index_len` bits and computes the XOR of all blocks.
 * 2) Replaces the least significant block of key with computed block.
 * With this hash function, the index will depend on all bits in the key. As a consequence, entries
 * will be more randomly distributed among the sets.
 * NOTE: Applying this hash function twice with the same `index_len` acts as the identity function.
 */ 
uint64_t hash_index(uint64_t key, int index_len) {
    if (index_len == 0)
        return key;
    for (uint64_t tag = (key >> index_len); tag > 0; tag >>= index_len)
        key ^= tag & ((1 << index_len) - 1);
    return key;
}

/*=== End Of Cache Framework ===*/

/**
 * The access map table records blocks as being in one of 3 general states:
 * ACCESS, PREFETCH, or INIT.
 * The PREFETCH state is actually composed of up to 3 sub-states:
 * L1-PREFETCH, L2-PREFETCH, or L3-PREFETCH.
 * This version of MLOP does not prefetch into L3 so there are 4 states in total (2-bit states).
 */
enum State { INIT = 0, ACCESS = 1, PREFTCH = 2 };
char state_char[] = {'I', 'A', 'P'};

string map_to_string(const vector<State> &access_map, const vector<int> &prefetch_map) {
    ostringstream oss;
    for (unsigned i = 0; i < access_map.size(); i += 1)
        if (access_map[i] == State::PREFTCH) {
            oss << prefetch_map[i];
        } else {
            oss << state_char[access_map[i]];
        }
    return oss.str();
}

class AccessMapData {
  public:
    /* block states are represented with a `State` and an `int` in this software implementation but
     * in a hardware implementation, they'd be represented with only 2 bits. */
    vector<State> access_map;
    vector<int> prefetch_map;

    deque<int> hist_queue;
};

class AccessMapTable : public LRUSetAssociativeCache<AccessMapData> {
    typedef LRUSetAssociativeCache<AccessMapData> Super;

  public:
    /* NOTE: zones are equivalent to pages (64 blocks) in this implementation */
    AccessMapTable(int size, int blocks_in_zone, int queue_size, int debug_level = 0, int num_ways = 16)
        : Super(size, num_ways, debug_level), blocks_in_zone(blocks_in_zone), queue_size(queue_size) {
        if (this->debug_level >= 1)
            cerr << "AccessMapTable::AccessMapTable(size=" << size << ", blocks_in_zone=" << blocks_in_zone
                 << ", queue_size=" << queue_size << ", debug_level=" << debug_level << ", num_ways=" << num_ways << ")"
                 << endl;
    }

    /**
     * Sets specified block to given state. If new state is ACCESS, the block will also be pushed in the zone's queue.
     */
    void set_state(uint64_t block_number, State new_state, int new_fill_level = 0) {
        if (this->debug_level >= 2)
            cerr << "AccessMapTable::set_state(block_number=0x" << hex << block_number
                 << ", new_state=" << state_char[new_state] << ", new_fill_level=" << new_fill_level << ")" << dec
                 << endl;

        // if (new_state != State::PREFTCH)
        //     assert(new_fill_level == 0);
        // else
        //     assert(new_fill_level == FILL_L1 || new_fill_level == FILL_L2 || new_fill_level == FILL_LLC);

        uint64_t zone_number = block_number / this->blocks_in_zone;
        int zone_offset = block_number % this->blocks_in_zone;

        uint64_t key = this->build_key(zone_number);
        Entry *entry = Super::find(key);
        if (!entry) {
            // assert(new_state != State::PREFTCH);
            if (new_state == State::INIT)
                return;
            Super::insert(key, {vector<State>(blocks_in_zone, State::INIT), vector<int>(blocks_in_zone, 0)});
            entry = Super::find(key);
            // assert(entry->data.hist_queue.empty());
        }

        auto &access_map = entry->data.access_map;
        auto &prefetch_map = entry->data.prefetch_map;
        auto &hist_queue = entry->data.hist_queue;

        if (new_state == State::ACCESS) {
            Super::set_mru(key);

            /* insert access into queue */
            hist_queue.push_front(zone_offset);
            if (hist_queue.size() > this->queue_size)
                hist_queue.pop_back();
        }

        State old_state = access_map[zone_offset];
        int old_fill_level = prefetch_map[zone_offset];

        vector<State> old_access_map = access_map;
        vector<int> old_prefetch_map = prefetch_map;

        access_map[zone_offset] = new_state;
        prefetch_map[zone_offset] = new_fill_level;

        if (new_state == State::INIT) {
            /* delete entry if access map is empty (all in state INIT) */
            bool all_init = true;
            for (unsigned i = 0; i < this->blocks_in_zone; i += 1)
                if (access_map[i] != State::INIT) {
                    all_init = false;
                    break;
                }
            if (all_init)
                Super::erase(key);
        }

        if (this->debug_level >= 2) {
            cerr << "[AccessMapTable::set_state] zone_number=0x" << hex << zone_number << dec
                 << ", zone_offset=" << setw(2) << zone_offset << ": state transition from " << state_char[old_state]
                 << " to " << state_char[new_state] << endl;
            if (old_state != new_state || old_fill_level != new_fill_level) {
                cerr << "[AccessMapTable::set_state] old_access_map=" << map_to_string(old_access_map, old_prefetch_map)
                     << endl;
                cerr << "[AccessMapTable::set_state] new_access_map=" << map_to_string(access_map, prefetch_map)
                     << endl;
            }
        }
    }

    Entry *find(uint64_t zone_number) {
        if (this->debug_level >= 2)
            cerr << "AccessMapTable::find(zone_number=0x" << hex << zone_number << ")" << dec << endl;
        uint64_t key = this->build_key(zone_number);
        return Super::find(key);
    }

    string log() {
        vector<string> headers({"Zone", "Access Map"});
        return Super::log(headers);
    }

  private:
    /* @override */
    void write_data(Entry &entry, Table &table, int row) {
        uint64_t zone_number = hash_index(entry.key, this->index_len);
        table.set_cell(row, 0, zone_number);
        table.set_cell(row, 1, map_to_string(entry.data.access_map, entry.data.prefetch_map));
    }

    uint64_t build_key(uint64_t zone_number) {
        uint64_t key = zone_number; /* no truncation (52 bits) */
        return hash_index(key, this->index_len);
    }

    unsigned blocks_in_zone;
    unsigned queue_size;

    /*===================================================================*/
    /* Entry   = [tag, map, queue, valid, LRU]                           */
    /* Storage = size * (52 - lg(sets) + 64 * 2 + 15 * 6 + 1 + lg(ways)) */
    /* L1D: 256 * (52 - lg(16) + 128 + 90 + 1 + lg(16)) = 8672 Bytes     */
    /*===================================================================*/
};

template <class T> inline T square(T x) { return x * x; }

class MLOP {
  public:
    MLOP(int blocks_in_zone, int amt_size, const int PF_DEGREE, const int NUM_UPDATES, const double L1D_THRESH,
        const double L2C_THRESH, const double LLC_THRESH, int debug_level)
        : PF_DEGREE(PF_DEGREE), NUM_UPDATES(NUM_UPDATES), L1D_THRESH(L1D_THRESH * NUM_UPDATES),
          L2C_THRESH(L2C_THRESH * NUM_UPDATES), LLC_THRESH(LLC_THRESH * NUM_UPDATES), ORIGIN(blocks_in_zone - 1),
          MAX_OFFSET(blocks_in_zone - 1), NUM_OFFSETS(2 * blocks_in_zone - 1), blocks_in_zone(blocks_in_zone),
          access_map_table(amt_size, blocks_in_zone, PF_DEGREE - 1, debug_level), pf_offset(PF_DEGREE, vector<int>()),
          offset_scores(PF_DEGREE, vector<int>(2 * blocks_in_zone - 1, 0)), pf_level(PF_DEGREE, 0),
          debug_level(debug_level) {
        if (this->debug_level >= 1)
            cerr << "MLOP::MLOP(blocks_in_zone=" << blocks_in_zone << ", amt_size=" << amt_size
                 << ", PF_DEGREE=" << PF_DEGREE << ", NUM_UPDATES=" << NUM_UPDATES << ", L1D_THRESH=" << L1D_THRESH
                 << ", L2C_THRESH=" << L2C_THRESH << ", LLC_THRESH=" << LLC_THRESH << ", debug_level=" << debug_level
                 << ")" << endl;
        // assert(ORIGIN == MAX_OFFSET);
        // assert(NUM_OFFSETS == MAX_OFFSET * 2 + 1);
        // assert((int)offset_scores[0].size() == NUM_OFFSETS);
    }

    /**
     * Updates MLOP's state based on the most recent trigger access (LOAD miss/prefetch-hit).
     * @param block_number The block address of the most recent trigger access
     */
    void access(uint64_t block_number) {
        if (this->debug_level >= 2)
            cerr << "MLOP::access(block_number=0x" << hex << block_number << ")" << dec << endl;

        uint64_t zone_number = block_number / this->blocks_in_zone;
        int zone_offset = block_number % this->blocks_in_zone;

        if (this->debug_level >= 2)
            cerr << "[MLOP::access] zone_number=0x" << hex << zone_number << dec << ", zone_offset=" << zone_offset
                 << endl;

        // for (int i = 0; i < PF_DEGREE; i += 1)
        //     assert(this->offset_scores[i][ORIGIN] == 0);

        /* update scores */
        AccessMapTable::Entry *entry = this->access_map_table.find(zone_number);
        if (!entry) {
            /* stats */
            this->zone_cnt += 1;
            if (this->zone_cnt == TRACKED_ZONE_CNT) {
                this->tracked_zone_number = zone_number;
                this->tracking = true;
                this->zone_life.push_back(string(this->blocks_in_zone, state_char[State::INIT]));
            }
            /* ===== */
            return;
        }
        vector<State> access_map = entry->data.access_map;
        if (access_map[zone_offset] == State::ACCESS)
            return; /* ignore repeated trigger access */
        this->update_cnt += 1;
        const deque<int> &queue = entry->data.hist_queue;
        for (int d = 0; d <= (int)queue.size(); d += 1) {
            /* unmark latest access to increase prediction depth */
            if (d != 0) {
                int idx = queue[d - 1];
                // assert(0 <= idx && idx < this->blocks_in_zone);
                access_map[idx] = State::INIT;
            }
            for (int i = 0; i < this->blocks_in_zone; i += 1) {
                if (access_map[i] == State::ACCESS) {
                    int offset = zone_offset - i;
                    if (-MAX_OFFSET <= offset && offset <= +MAX_OFFSET && offset != 0)
                        this->offset_scores[d][ORIGIN + offset] += 1;
                }
            }
        }

        /* update prefetching offsets if round is finished */
        if (this->update_cnt == NUM_UPDATES) {
            if (this->debug_level >= 1)
                cerr << "[MLOP::access] Round finished!" << endl;

            /* reset `update_cnt` and clear `pf_level` and `pf_offset` */
            this->update_cnt = 0;
            this->pf_level = vector<int>(PF_DEGREE, 0);
            this->pf_offset = vector<vector<int>>(PF_DEGREE, vector<int>());

            /* calculate maximum score for all degrees */
            vector<int> max_scores(PF_DEGREE, 0);
            for (int i = 0; i < PF_DEGREE; i += 1) {
                max_scores[i] = *max_element(this->offset_scores[i].begin(), this->offset_scores[i].end());
                /* `max_scores` should be decreasing */
                // if (i > 0)
                //     assert(max_scores[i] <= max_scores[i - 1]);
            }

            int fill_level = 0;
            vector<bool> pf_offset_map(NUM_OFFSETS, false);
            for (int d = PF_DEGREE - 1; d >= 0; d -= 1) {
                /* check thresholds */
                if (max_scores[d] >= L1D_THRESH)
                    fill_level = FILL_L1;
                else if (max_scores[d] >= L2C_THRESH)
                    fill_level = FILL_L2;
                else if (max_scores[d] >= LLC_THRESH)
                    fill_level = FILL_LLC;
                else
                    continue;

                /* select offsets with highest score */
                vector<int> best_offsets;
                for (int i = -MAX_OFFSET; i <= +MAX_OFFSET; i += 1) {
                    int &cur_score = this->offset_scores[d][ORIGIN + i];
                    // assert(0 <= cur_score && cur_score <= NUM_UPDATES);
                    if (cur_score == max_scores[d] && !pf_offset_map[ORIGIN + i])
                        best_offsets.push_back(i);
                }

                this->pf_level[d] = fill_level;
                this->pf_offset[d] = best_offsets;

                /* mark in `pf_offset_map` to avoid duplicate prefetch offsets */
                for (int i = 0; i < (int)best_offsets.size(); i += 1)
                    pf_offset_map[ORIGIN + best_offsets[i]] = true;
            }

            /* reset `offset_scores` */
            this->offset_scores = vector<vector<int>>(PF_DEGREE, vector<int>(NUM_OFFSETS, 0));

            /* print selected prefetching offsets if debug is on */
            if (this->debug_level >= 1) {
                for (int d = 0; d < PF_DEGREE; d += 1) {
                    cerr << "[MLOP::access] Degree=" << setw(2) << d + 1 << ", Level=";

                    if (this->pf_level[d] == 0)
                        cerr << "No";
                    if (this->pf_level[d] == FILL_L1)
                        cerr << "L1";
                    if (this->pf_level[d] == FILL_L2)
                        cerr << "L2";
                    if (this->pf_level[d] == FILL_LLC)
                        cerr << "L3";

                    cerr << ", Offsets: ";
                    if (this->pf_offset[d].size() == 0)
                        cerr << "None";
                    for (int i = 0; i < (int)this->pf_offset[d].size(); i += 1) {
                        cerr << this->pf_offset[d][i];
                        if (i < (int)this->pf_offset[d].size() - 1)
                            cerr << ", ";
                    }
                    cerr << endl;
                }
            }

            /* stats */
            this->round_cnt += 1;

            int cur_pf_degree = 0;
            for (const bool &x : pf_offset_map)
                cur_pf_degree += (x ? 1 : 0);
            this->pf_degree_sum += cur_pf_degree;
            this->pf_degree_sqr_sum += square(cur_pf_degree);

            uint64_t max_score_le = max_scores[PF_DEGREE - 1];
            uint64_t max_score_ri = max_scores[0];
            this->max_score_le_sum += max_score_le;
            this->max_score_ri_sum += max_score_ri;
            this->max_score_le_sqr_sum += square(max_score_le);
            this->max_score_ri_sqr_sum += square(max_score_ri);
            /* ===== */
        }
    }

    /**
     * @param block_number The block address of the most recent LOAD access
     */
    void prefetch(CACHE *cache, uint64_t block_number) {
        if (this->debug_level >= 2) {
            cerr << "MLOP::prefetch(cache=" << cache->NAME << "-" << cache->cpu << ", block_number=0x" << hex
                 << block_number << dec << ")" << endl;
        }
        int pf_issued = 0;
        uint64_t zone_number = block_number / this->blocks_in_zone;
        int zone_offset = block_number % this->blocks_in_zone;
        AccessMapTable::Entry *entry = this->access_map_table.find(zone_number);
        // assert(entry); /* I expect `mark` to have been called before `prefetch` */
        const vector<State> &access_map = entry->data.access_map;
        const vector<int> &prefetch_map = entry->data.prefetch_map;
        if (this->debug_level >= 2) {
            cerr << "[MLOP::prefetch] old_access_map=" << map_to_string(access_map, prefetch_map) << endl;
        }
        for (int d = 0; d < PF_DEGREE; d += 1) {
            for (auto &cur_pf_offset : this->pf_offset[d]) {
                // assert(this->pf_level[d] > 0);
                int offset_to_prefetch = zone_offset + cur_pf_offset;

                /* use `access_map` to filter prefetches */
                if (access_map[offset_to_prefetch] == State::ACCESS)
                    continue;
                if (access_map[offset_to_prefetch] == State::PREFTCH &&
                    prefetch_map[offset_to_prefetch] <= this->pf_level[d])
                    continue;

                if (this->is_inside_zone(offset_to_prefetch) && cache->PQ.occupancy < cache->PQ.SIZE &&
                    cache->PQ.occupancy + cache->MSHR.occupancy < cache->MSHR.SIZE - 1) {
                    uint64_t pf_block_number = block_number + cur_pf_offset;
                    uint64_t base_addr = block_number << LOG2_BLOCK_SIZE;
                    uint64_t pf_addr = pf_block_number << LOG2_BLOCK_SIZE;
                    int ok = cache->prefetch_line(0, base_addr, pf_addr, this->pf_level[d], 0);
                    // assert(ok == 1);
                    this->mark(pf_block_number, State::PREFTCH, this->pf_level[d]);
                    pf_issued += 1;
                }
            }
        }
        if (this->debug_level >= 2) {
            cerr << "[MLOP::prefetch] new_access_map=" << map_to_string(access_map, prefetch_map) << endl;
            cerr << "[MLOP::prefetch] issued " << pf_issued << " prefetch(es)" << endl;
        }
    }

    void mark(uint64_t block_number, State state, int fill_level = 0) {
        this->access_map_table.set_state(block_number, state, fill_level);
    }

    void set_debug_level(int debug_level) {
        this->debug_level = debug_level;
        this->access_map_table.set_debug_level(debug_level);
    }

    string log_offset_scores() {
        Table table(1 + PF_DEGREE, this->offset_scores.size() + 1);
        vector<string> headers = {"Offset"};
        for (int d = 0; d < PF_DEGREE; d += 1) {
            ostringstream oss;
            oss << "Score[d=" << d + 1 << "]";
            headers.push_back(oss.str());
        }
        table.set_row(0, headers);
        for (int i = -(this->blocks_in_zone - 1); i <= +(this->blocks_in_zone - 1); i += 1) {
            table.set_cell(i + this->blocks_in_zone, 0, i);
            for (int d = 0; d < PF_DEGREE; d += 1)
                table.set_cell(i + this->blocks_in_zone, d + 1, this->offset_scores[d][ORIGIN + i]);
        }
        return table.to_string();
    }

    void log() {
        cerr << "Access Map Table:" << dec << endl;
        cerr << this->access_map_table.log();

        cerr << "Offset Scores:" << endl;
        cerr << this->log_offset_scores();
    }

    /*========== stats ==========*/

    void track(uint64_t block_number) {
        uint64_t zone_number = block_number / this->blocks_in_zone;
        if (this->tracking && zone_number == this->tracked_zone_number) {
            AccessMapTable::Entry *entry = this->access_map_table.find(zone_number);
            if (!entry) {
                this->tracking = false; /* end of zone lifetime, stop tracking */
                this->zone_life.push_back(string(this->blocks_in_zone, state_char[State::INIT]));
                return;
            }
            const vector<State> &access_map = entry->data.access_map;
            const vector<int> &prefetch_map = entry->data.prefetch_map;
            string s = map_to_string(access_map, prefetch_map);
            if (s != this->zone_life.back())
                this->zone_life.push_back(s);
        }
    }

    void reset_stats() {
        this->tracking = false;
        this->zone_cnt = 0;
        this->zone_life.clear();

        this->round_cnt = 0;
        this->pf_degree_sum = 0;
        this->pf_degree_sqr_sum = 0;
        this->max_score_le_sum = 0;
        this->max_score_le_sqr_sum = 0;
        this->max_score_ri_sum = 0;
        this->max_score_ri_sqr_sum = 0;
    }

    void print_stats() {
        cout << "[MLOP] History of tracked zone:" << endl;
        for (auto &x : this->zone_life)
            cout << x << endl;

        double pf_degree_mean = 1.0 * this->pf_degree_sum / this->round_cnt;
        double pf_degree_sqr_mean = 1.0 * this->pf_degree_sqr_sum / this->round_cnt;
        double pf_degree_sd = sqrt(pf_degree_sqr_mean - square(pf_degree_mean));
        cout << "[MLOP] Prefetch Degree Mean: " << pf_degree_mean << endl;
        cout << "[MLOP] Prefetch Degree SD: " << pf_degree_sd << endl;

        double max_score_le_mean = 1.0 * this->max_score_le_sum / this->round_cnt;
        double max_score_le_sqr_mean = 1.0 * this->max_score_le_sqr_sum / this->round_cnt;
        double max_score_le_sd = sqrt(max_score_le_sqr_mean - square(max_score_le_mean));
        cout << "[MLOP] Max Score Left Mean (%): " << 100.0 * max_score_le_mean / NUM_UPDATES << endl;
        cout << "[MLOP] Max Score Left SD (%): " << 100.0 * max_score_le_sd / NUM_UPDATES << endl;

        double max_score_ri_mean = 1.0 * this->max_score_ri_sum / this->round_cnt;
        double max_score_ri_sqr_mean = 1.0 * this->max_score_ri_sqr_sum / this->round_cnt;
        double max_score_ri_sd = sqrt(max_score_ri_sqr_mean - square(max_score_ri_mean));
        cout << "[MLOP] Max Score Right Mean (%): " << 100.0 * max_score_ri_mean / NUM_UPDATES << endl;
        cout << "[MLOP] Max Score Right SD (%): " << 100.0 * max_score_ri_sd / NUM_UPDATES << endl;
    }

  private:
    bool is_inside_zone(int zone_offset) { return (0 <= zone_offset && zone_offset < this->blocks_in_zone); }

    const int PF_DEGREE;
    const int NUM_UPDATES;
    const int L1D_THRESH;
    const int L2C_THRESH;
    const int LLC_THRESH;
    const int ORIGIN;
    const int MAX_OFFSET;
    const int NUM_OFFSETS;

    int blocks_in_zone;
    AccessMapTable access_map_table;

    /**
     * Contains best offsets for each degree of prefetching. A degree will have several offsets if
     * they all had maximum score (thus, a vector of vectors). A degree won't have any offsets if
     * all best offsets were redundant (already selected in previous degrees).
     */
    vector<vector<int>> pf_offset;

    vector<vector<int>> offset_scores;
    vector<int> pf_level; /* the prefetching level for each degree of prefetching offsets */
    int update_cnt = 0;  /* tracks the number of score updates, round is over when `update_cnt == NUM_UPDATES` */

    int debug_level = 0;

    /* stats */
    const uint64_t TRACKED_ZONE_CNT = 100;
    bool tracking = false;
    uint64_t tracked_zone_number = 0;
    uint64_t zone_cnt = 0;
    vector<string> zone_life;

    uint64_t round_cnt = 0;
    uint64_t pf_degree_sum = 0, pf_degree_sqr_sum = 0;
    uint64_t max_score_le_sum = 0, max_score_le_sqr_sum = 0;
    uint64_t max_score_ri_sum = 0, max_score_ri_sqr_sum = 0;

    /*=======================================================*/
    /*======== Storage required for `offset_scores` =========*/
    /* pf_degree * (blocks_in_page - 1) * 2 * SCORE_BITS     */
    /* 16 * (64 - 1) * 2 * 9 = 2268 Bytes                    */
    /*=======================================================*/

    /*=======================================================*/
    /*=== Storage required for `pf_offsets` & `pf_levels` ===*/
    /* (blocks_in_page - 1) * 2 * (FILL_BITS + OFFSET_BITS)  */
    /* (64 - 1) * 2 * (1 + 6) = 882 Bits                     */
    /*=======================================================*/
};

/**
 * The global debug level. Higher values will print more information.
 * NOTE: The size of the output file can become very large (~GBs).
 */
const int DEBUG_LEVEL = 0;

vector<MLOP> prefetchers;
}
#endif

#ifdef BINGO_BOP_ON
class Table {
  public:
    Table(int width, int height) : width(width), height(height), cells(height, vector<string>(width)) {}

    void set_row(int row, const vector<string> &data, int start_col = 0) {
        assert(data.size() + start_col == this->width);
        for (unsigned col = start_col; col < this->width; col += 1)
            this->set_cell(row, col, data[col]);
    }

    void set_col(int col, const vector<string> &data, int start_row = 0) {
        assert(data.size() + start_row == this->height);
        for (unsigned row = start_row; row < this->height; row += 1)
            this->set_cell(row, col, data[row]);
    }

    void set_cell(int row, int col, string data) {
        assert(0 <= row && row < (int)this->height);
        assert(0 <= col && col < (int)this->width);
        this->cells[row][col] = data;
    }

    void set_cell(int row, int col, double data) {
        this->oss.str("");
        this->oss << setw(11) << fixed << setprecision(8) << data;
        this->set_cell(row, col, this->oss.str());
    }

    void set_cell(int row, int col, int64_t data) {
        this->oss.str("");
        this->oss << setw(11) << std::left << data;
        this->set_cell(row, col, this->oss.str());
    }

    void set_cell(int row, int col, int data) { this->set_cell(row, col, (int64_t)data); }

    void set_cell(int row, int col, uint64_t data) { this->set_cell(row, col, (int64_t)data); }

    string to_string() {
        vector<int> widths;
        for (unsigned i = 0; i < this->width; i += 1) {
            int max_width = 0;
            for (unsigned j = 0; j < this->height; j += 1)
                max_width = max(max_width, (int)this->cells[j][i].size());
            widths.push_back(max_width + 2);
        }
        string out;
        out += Table::top_line(widths);
        out += this->data_row(0, widths);
        for (unsigned i = 1; i < this->height; i += 1) {
            out += Table::mid_line(widths);
            out += this->data_row(i, widths);
        }
        out += Table::bot_line(widths);
        return out;
    }

    string data_row(int row, const vector<int> &widths) {
        string out;
        for (unsigned i = 0; i < this->width; i += 1) {
            string data = this->cells[row][i];
            data.resize(widths[i] - 2, ' ');
            out += " | " + data;
        }
        out += " |\n";
        return out;
    }

    static string top_line(const vector<int> &widths) { return Table::line(widths, "┌", "┬", "┐"); }

    static string mid_line(const vector<int> &widths) { return Table::line(widths, "├", "┼", "┤"); }

    static string bot_line(const vector<int> &widths) { return Table::line(widths, "└", "┴", "┘"); }

    static string line(const vector<int> &widths, string left, string mid, string right) {
        string out = " " + left;
        for (unsigned i = 0; i < widths.size(); i += 1) {
            int w = widths[i];
            for (int j = 0; j < w; j += 1)
                out += "─";
            if (i != widths.size() - 1)
                out += mid;
            else
                out += right;
        }
        return out + "\n";
    }

  private:
    unsigned width;
    unsigned height;
    vector<vector<string>> cells;
    ostringstream oss;
};
//##############定义BINGO_BOP中的RR Table采用的是一个直接映射的cache，这个cache的相连度为1#########
//组相连cache
template <class T> class SetAssociativeCache {
  public:
    class Entry {
      public:
        uint64_t key; //key的作用是什么？
        uint64_t index;
        uint64_t tag;
        bool valid;
        T data;
    };

    //初始化cache
    SetAssociativeCache(int size, int num_ways)
        : size(size), num_ways(num_ways), num_sets(size / num_ways), entries(num_sets, vector<Entry>(num_ways)),
          cams(num_sets) {
        assert(size % num_ways == 0);
        for (int i = 0; i < num_sets; i += 1)
            for (int j = 0; j < num_ways; j += 1)
                entries[i][j].valid = false;
    }

    Entry *erase(uint64_t key) {
        Entry *entry = this->find(key);
        uint64_t index = key % this->num_sets; //index是组索引？
        uint64_t tag = key / this->num_sets;   //tag是行tag？
        auto &cam = cams[index];
        int num_erased = cam.erase(tag);
        if (entry)
            entry->valid = false;
        assert(entry ? num_erased == 1 : num_erased == 0);
        return entry;
    }

    /**
     * @return The old state of the entry that was written to.
     */
    Entry insert(uint64_t key, const T &data) {
        Entry *entry = this->find(key);
        if (entry != nullptr) {
            Entry old_entry = *entry;
            entry->data = data;
            return old_entry;
        }
        uint64_t index = key % this->num_sets;
        uint64_t tag = key / this->num_sets;
        vector<Entry> &set = this->entries[index];
        int victim_way = -1;
        for (int i = 0; i < this->num_ways; i += 1)
            if (!set[i].valid) {
                victim_way = i;
                break;
            }
        if (victim_way == -1) {
            victim_way = this->select_victim(index);
        }
        Entry &victim = set[victim_way];
        Entry old_entry = victim;
        victim = {key, index, tag, true, data};
        auto &cam = cams[index];
        if (old_entry.valid) {
            int num_erased = cam.erase(old_entry.tag);
            assert(num_erased == 1);
        }
        cam[tag] = victim_way;
        return old_entry;
    }

    Entry *find(uint64_t key) {
        uint64_t index = key % this->num_sets;
        uint64_t tag = key / this->num_sets;
        auto &cam = cams[index];
        if (cam.find(tag) == cam.end())
            return nullptr;
        int way = cam[tag];
        Entry &entry = this->entries[index][way];
        assert(entry.tag == tag && entry.valid);
        return &entry;
    }

      /**
     * For debugging purposes.
     */
    string log(vector<string> headers, function<void(Entry &, Table &, int)> write_data) {
        vector<Entry> valid_entries = this->get_valid_entries();
        Table table(headers.size(), valid_entries.size() + 1);
        table.set_row(0, headers);
        for (unsigned i = 0; i < valid_entries.size(); i += 1)
            write_data(valid_entries[i], table, i + 1);
        return table.to_string();
    }



    void set_debug_mode(bool enable) { this->debug = enable; }

  protected:
    /**
     * @return The way of the selected victim.
     */
    virtual int select_victim(uint64_t index) {
        /* random eviction policy if not overriden */
        return rand() % this->num_ways;
    }

    vector<Entry> get_valid_entries() {
        vector<Entry> valid_entries;
        for (int i = 0; i < num_sets; i += 1)
            for (int j = 0; j < num_ways; j += 1)
                if (entries[i][j].valid)
                    valid_entries.push_back(entries[i][j]);
        return valid_entries;
    }

    int size;
    int num_ways;
    int num_sets;
    vector<vector<Entry>> entries;
    vector<unordered_map<uint64_t, int>> cams;
    bool debug = false;
};
//直接映射cache，继承自组相连cache
template <class T> class DirectMappedCache : public SetAssociativeCache<T> {
    typedef SetAssociativeCache<T> Super;

  public:
    DirectMappedCache(int size) : Super(size, 1) {}
};

/** End Of Cache Framework **/

class RecentRequestsTableData {
  public:
    uint64_t base_address;
};

//继承自直接映射cache，直接映射cache是组相连cache的一个特殊例子，组内的条目为1
class RecentRequestsTable : public DirectMappedCache<RecentRequestsTableData> {
    typedef DirectMappedCache<RecentRequestsTableData> Super;

  public:
    RecentRequestsTable(int size) : Super(size) {
        assert(__builtin_popcount(size) == 1);
        this->hash_w = __builtin_ctz(size);
    }

    Entry insert(uint64_t base_address) {
        uint64_t key = this->hash(base_address);
        return Super::insert(key, {base_address});
    }

    bool find(uint64_t base_address) {
        uint64_t key = this->hash(base_address);
        return (Super::find(key) != nullptr);
    }

    string log() {
        vector<string> headers({"Hash", "Base Address"});
        return Super::log(headers, this->write_data);
    }

  private:
    static void write_data(Entry &entry, Table &table, int row) {
        table.set_cell(row, 0, bitset<20>(entry.key).to_string());
        table.set_cell(row, 1, entry.data.base_address);
    }

    /* The RR table is accessed through a simple hash function. For instance, for a 256-entry RR table, we XOR the 8
     * least significant line address bits with the next 8 bits to obtain the table index. For 12-bit tags, we skip the
     * 8 least significant line address bits and extract the next 12 bits. */
    uint64_t hash(uint64_t input) {
        int next_w_bits = ((1 << hash_w) - 1) & (input >> hash_w);
        uint64_t output = ((1 << 20) - 1) & (next_w_bits ^ input);
        if (this->debug) {
            cerr << "[RR] hash( " << bitset<32>(input).to_string() << " ) = " << bitset<20>(output).to_string() << endl;
        }
        return output;
    }

    int hash_w;
};


//#################定义类 BOP和 Bestoffsetlearning#######################
class BestOffsetLearning {
  public:
    BestOffsetLearning(int blocks_in_page) : blocks_in_page(blocks_in_page) {
        /* Useful offset values depend on the memory page size, as the BO prefetcher does not prefetch across page
         * boundaries. For instance, assuming 4KB pages and 64B lines, a page contains 64 lines, and there is no point
         * in considering offset values greater than 63. However, it may be useful to consider offsets greater than 63
         * for systems having superpages. */
        /* We propose a method for offset sampling that is algorithmic and not totally arbitrary: we include in our list
         * all the offsets between 1 and 256 whose prime factorization does not contain primes greater than 5. */
        /* Nothing prevents a BO prefetcher to use negative offset values. Although some applications might benefit from
         * negative offsets, we did not observe any benefit in our experiments. Hence we consider only positive offsets
         * in this study. */

         //初始化offset，选取一系列素数
        for (int i = 1; i < blocks_in_page; i += 1) {
            int n = i;
            for (int j = 2; j <= 5; j += 1)
                while (n % j == 0)
                    n /= j;
            if (n == 1)
                offset_list.push_back({i, 0});
        }
    }

    /**
     * @return The current best offset.
     */
    int test_offset(uint64_t block_number, RecentRequestsTable &recent_requests_table) {
        int page_offset = block_number % this->blocks_in_page;
        //每次访问都对index_to_test加1，对不同的offset进行遍历测试
        Entry &entry = this->offset_list[this->index_to_test];
        //由于预取不会超过页面的大小，所以这个地方的寻找的X和X+D也应该在同一个页面，后续在L1中使用的时候，需要做一些改进
        #ifdef BINGO_BOP_ON
            bool found =
                is_inside_page(page_offset - entry.offset) && recent_requests_table.find(block_number - entry.offset);
        #endif
        #ifdef CP_BINGO_BOP_ON
            bool found = recent_requests_table.find(block_number - entry.offset);            
        #endif
        if (this->debug) {
            cerr << "[BOL] testing offset=" << entry.offset << " with score=" << entry.score << endl;
            cerr << "[BOL] match=" << found << endl;
        }
        if (found) {
            entry.score += 1;
            if (entry.score > this->best_score) {
                this->best_score = entry.score;
                this->local_best_offset = entry.offset;
            }
        }
        this->index_to_test = (this->index_to_test + 1) % this->offset_list.size();
        /* test round termination */
        if (this->index_to_test == 0) {
            if (this->debug) {
                cerr << "[BOL] round=" << this->round << " finished" << endl;
            }
            this->round += 1;
            /* The current learning phase finishes at the end of a round when either of the two following events happens
             * first: one of the scores equals SCOREMAX, or the number of rounds equals ROUNDMAX (a fixed parameter). */
            if (this->best_score >= SCORE_MAX || this->round == ROUND_MAX) {
                #ifdef CONSTRAIN_BOP
                    if (this->best_score <= BAD_SCORE || (this->best_score < SCORE_MAX && this->round == ROUND_MAX)){
                        this->global_best_offset = 0; /* turn off prefetching */
                        #ifdef BOP_DEBUG
                            std::cout << "OFF BOP: " << this->best_score << " "<< this->global_best_offset << std::endl;
                        #endif
                    }
                    else{
                        this->global_best_offset = this->local_best_offset;
                        #ifdef BOP_DEBUG
                            std::cout<< "BOP ON: " << this->best_score << " "<< this->global_best_offset << std::endl;
                        #endif
                    }
                #else
                    if (this->best_score <= BAD_SCORE)
                        this->global_best_offset = 0; /* turn off prefetching */
                    else
                        this->global_best_offset = this->local_best_offset;
                #endif

                if (this->debug) {
                    cerr << "[BOL] learning phase finished, winner=" << this->global_best_offset << endl;
                    cerr << this->log();
                }
                /* reset all internal state */
                for (auto &entry : this->offset_list)
                    entry.score = 0;
                this->local_best_offset = 0;
                this->best_score = 0;
                this->round = 0;
            }
        }
        return this->global_best_offset;
    }

    string log() {
        Table table(2, offset_list.size() + 1);
        table.set_row(0, {"Offset", "Score"});
        for (unsigned i = 0; i < offset_list.size(); i += 1) {
            table.set_cell(i + 1, 0, offset_list[i].offset);
            table.set_cell(i + 1, 1, offset_list[i].score);
        }
        return table.to_string();
    }

    void set_debug_mode(bool enable) { this->debug = enable; }

  private:
    bool is_inside_page(int page_offset) { return (0 <= page_offset && page_offset < this->blocks_in_page); }

    class Entry {
      public:
        int offset;
        int score;
    };

    int blocks_in_page;
    vector<Entry> offset_list;

    int round = 0;
    int best_score = 0;
    int index_to_test = 0;
    int local_best_offset = 0;
    int global_best_offset = 1;

    const int SCORE_MAX = 20; //默认32
    const int ROUND_MAX = 100;
    const int BAD_SCORE = 1;

    bool debug = false;
};

class BOP {
  public:
    //prefetchers = vector<BOP>(NUM_CPUS, BOP(PAGE_SIZE / BLOCK_SIZE, RR_TABLE_SIZE, DEGREE));
    //初始化的配置，blocks_in_page是一个页面内的blocks数目
    BOP(int blocks_in_page, int recent_requests_table_size, int degree)
        : blocks_in_page(blocks_in_page), best_offset_learning(blocks_in_page),
          recent_requests_table(recent_requests_table_size), degree(degree) {}

    /**
     * @return A vector of block numbers that should be prefetched.
     */
    vector<uint64_t> access(uint64_t block_number) {
        uint64_t page_number = block_number / this->blocks_in_page;
        int page_offset = block_number % this->blocks_in_page;
        /* ... and if X and X + D lie in the same memory page, a prefetch request for line X + D is sent to the L3
         * cache. */
        if (this->debug) {
            cerr << "[BOP] block_number=" << block_number << endl;
            cerr << "[BOP] page_number=" << page_number << endl;
            cerr << "[BOP] page_offset=" << page_offset << endl;
            cerr << "[BOP] best_offset=" << this->prefetch_offset << endl;
        }

        vector<uint64_t> pred;
        for (int i = 1; i <= this->degree; i += 1) {
            #ifdef BINGO_BOP_ON
                if (this->prefetch_offset != 0 && is_inside_page(page_offset + i * this->prefetch_offset))
                {
                    pred.push_back(block_number + i * this->prefetch_offset);
                }
                else {
                if (this->debug)
                    cerr << "[BOP] X and X + " << i << " * D do not lie in the same memory page, no prefetch issued"
                         << endl;
                break;
            }
            #endif
            #ifdef CP_BINGO_BOP_ON
                 if (this->prefetch_offset != 0)
                {
                    pred.push_back(block_number + i * this->prefetch_offset);
                }
                else {
                    if (this->debug)
                        cerr << "[BOP] X and X + " << i << " * D do not lie in the same memory page, no prefetch issued"
                            << endl;
                    break;
                }
            #endif
            
        }

        int old_offset = this->prefetch_offset;
        /* On every eligible L2 read access (miss or prefetched hit), we test an offset di from the list. */
        this->prefetch_offset = this->best_offset_learning.test_offset(block_number, recent_requests_table);
        if (this->debug) {
            if (old_offset != this->prefetch_offset)
                cerr << "[BOP] offset changed from " << old_offset << " to " << this->prefetch_offset << endl;
            cerr << this->recent_requests_table.log();
            cerr << this->best_offset_learning.log();
        }
        return pred;
    }

    void cache_fill(uint64_t block_number, bool prefetch) {
        int page_offset = block_number % this->blocks_in_page;
        if (this->prefetch_offset == 0 && prefetch)
            return;
        if (this->prefetch_offset != 0 && !prefetch)
            return;
        #ifdef BINGO_BOP_ON
            if (!this->is_inside_page(page_offset - this->prefetch_offset))
                return;
        #endif
        //当预取回来的时候，会向RR Table中插入发出预取访问的基地址
        this->recent_requests_table.insert(block_number - this->prefetch_offset);
    }

    void set_debug_level(int debug_level) {
        bool enable = (bool)debug_level;
        this->debug = enable;
        this->best_offset_learning.set_debug_mode(enable);
        this->recent_requests_table.set_debug_mode(enable);
    }

  private:
    bool is_inside_page(int page_offset) { return (0 <= page_offset && page_offset < this->blocks_in_page); }

    int blocks_in_page;
    int prefetch_offset = 0;

    BestOffsetLearning best_offset_learning;
    RecentRequestsTable recent_requests_table;
    int degree;

    bool debug = false;
};

vector<BOP> prefetchers;

#endif

// Last edit: 27 - Sept - 2021 12:10

// FIFO queue
//#define SIZE_RR 16
//uint64_t RR[NUM_CPUS][SIZE_RR] = {0};
//uint64_t RR_cycle[NUM_CPUS][SIZE_RR] = {0};
//uint64_t RR_dx[NUM_CPUS] = {0};

//how to get the pages_addr: pages_addr = (line_addr & ADDR_MASK) >> LOG2_BLOCKS_PER_PAGE
//addr used to search latency table is w/o ADDR_MASK
//对于pf这一标记，用来指明是否是demand miss，但是目前的理解是针对real cache access miss和 prefetch miss时做的标记
//这样两个miss时，只有第一次需要进行latency计算，后续如果在cache中就不需要再继续进行latency计算了。

void notify_prefetch(uint64_t addr, uint64_t tag, uint32_t cpu, uint64_t cycle)
{
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
     *  - line_addr: address without ADDR——MASK
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


/******************************************************************************/
/*                       History Table functions                               */
/******************************************************************************/
// Auxiliar history table functions
void history_table_init(uint32_t cpu)
{
    /*
     * Initialize history table pointers
     *
     * Parameters:
     *      - cpu: cpu
     */
    for (uint32_t i = 0; i < HISTORY_TABLE_SET; i++) 
    {
        // Pointer to the first element
        history_pointers[cpu][i] = historyt[cpu][i];

        for (uint32_t ii = 0; ii < HISTORY_TABLE_WAY; ii++) 
        {
            historyt[cpu][i][ii].tag = 0;
            historyt[cpu][i][ii].time = 0;
            historyt[cpu][i][ii].addr = 0;
        }
    }
}

void history_table_add(uint64_t tag, uint32_t cpu, uint64_t addr)
{
    /*
     * Save the new information into the history table
     *
     * Parameters:
     *  - tag: PC tag
     *  - cpu: actual cpu
     *  - addr: line addr w/o ADDR_MASK
     */
    uint16_t set = tag & TABLE_SET_MASK;
    addr &= ADDR_MASK;

    uint64_t cycle = current_core_cycle[cpu] & TIME_MASK;
    // Save new element into the history table
    history_pointers[cpu][set]->tag       = tag;
    history_pointers[cpu][set]->time      = cycle;
    history_pointers[cpu][set]->addr      = addr;

    if (history_pointers[cpu][set] == &historyt[cpu][set][HISTORY_TABLE_WAY - 1])
    {
        history_pointers[cpu][set] = &historyt[cpu][set][0]; // End the cycle
    } else history_pointers[cpu][set]++; // Pointer to the next (oldest) entry
}

uint16_t history_table_get_aux(uint32_t cpu, uint32_t latency, 
        uint64_t tag, uint64_t act_addr, uint64_t ip[HISTORY_TABLE_WAY],
        uint64_t addr[HISTORY_TABLE_WAY], uint64_t cycle)
{
    //**********
    //line addr with ADDR_MASK
    //**********
    uint16_t num_on_time = 0;
    uint16_t set = tag & TABLE_SET_MASK;

    // The IPs that is launch in this cycle will be able to launch this prefetch
    if (cycle < latency) return num_on_time;
    cycle -= latency; 

    // Pointer to guide
    history_table_t *pointer = history_pointers[cpu][set];

    do
    {
        // Look for the IPs that can launch this prefetch
        if (pointer->tag == tag && pointer->time <= cycle)
        {
            // Test that addr is not duplicated
            if (pointer->addr == act_addr) return num_on_time;

            int found = 0;
            for (int i = 0; i < num_on_time; i++)
            {
                if (pointer->addr == addr[i]) return num_on_time;
            }

            // This IP can launch the prefetch
            ip[num_on_time]   = pointer->tag;
            addr[num_on_time] = pointer->addr;
            num_on_time++;
        }

        if (pointer == historyt[cpu][set])
        {
            pointer = &historyt[cpu][set][HISTORY_TABLE_WAY - 1];
        } else pointer--;
    } while (pointer != history_pointers[cpu][set]);

    return num_on_time;
}

uint16_t history_table_get(uint32_t cpu, uint32_t latency, 
        uint64_t tag, uint64_t act_addr,
        uint64_t ip[HISTORY_TABLE_WAY],
        uint64_t addr[HISTORY_TABLE_WAY], 
        uint64_t cycle)
{
    /*
     * Return an array (by parameter) with all the possible PC that can launch
     * an on-time and late prefetch
     *
     * Parameters:
     *  - tag: PC tag
     *  - cpu: actual cpu
     *  - latency: latency of the processor
     *  - on_time_ip (out): ips that can launch an on-time prefetch
     *  - on_time_addr (out): addr that can launch an on-time prefetch
     *  - num_on_time (out): number of ips that can launch an on-time prefetch
     *  - addr: line addr w/o ADDR_MASK
     */

    act_addr &= ADDR_MASK;

    uint16_t num_on_time = history_table_get_aux(cpu, latency, tag, act_addr, 
            ip, addr, cycle);

    // We found on-time prefetchs
    return num_on_time;
}


uint16_t history_table_pages_get(uint32_t cpu, uint32_t latency, 
        uint64_t act_addr,
        uint64_t addr[HISTORY_TABLE_WAY*HISTORY_TABLE_SET], 
        uint64_t cycle)
{
    /*
    *  - act_addr : line addr w/o ADDR_MASK
    */
    act_addr &= ADDR_MASK;
    uint16_t cur_addr = (act_addr >> LOG2_BLOCKS_PER_PAGE);

    uint16_t num_on_time = 0;

    // The IPs that is launch in this cycle will be able to launch this prefetch
    if (cycle < latency) return num_on_time;
    cycle -= latency; 

    // Pointer to guide
    for(int idx_his = 0; idx_his < HISTORY_TABLE_SET ; idx_his++)
    {
        history_table_t *pointer = history_pointers[cpu][idx_his];
        do
        {
            // Look for the IPs that can launch this prefetch
            if (pointer->time <= cycle)
            {
                uint64_t his_addr = ((pointer->addr)>>LOG2_BLOCKS_PER_PAGE);
                if (his_addr == cur_addr)
                {
                    for (int i = 0; i < num_on_time; i++)
                    {
                        if (pointer->addr == addr[i]) continue;
                    }
                    addr[num_on_time] = pointer->addr;
                    num_on_time++;
                }
            }

            if (pointer == historyt[cpu][idx_his])
            {
                pointer = &historyt[cpu][idx_his][HISTORY_TABLE_WAY - 1];
            } else pointer--;
        } while (pointer != history_pointers[cpu][idx_his]);
    }
    return num_on_time;

    // We found on-time prefetchs
}

uint16_t history_table_bop_get(uint32_t cpu, uint32_t latency, 
        uint64_t act_addr,
        uint64_t timely_addr[HISTORY_TABLE_WAY*HISTORY_TABLE_SET], 
        uint64_t cycle)
{
    /*
    *  - act_addr : line addr w/o ADDR_MASK
    */
    act_addr &= ADDR_MASK;

    uint16_t num_on_time = 0;

    // The IPs that is launch in this cycle will be able to launch this prefetch
    if (cycle < latency) return num_on_time;
    cycle -= latency; 

    // Pointer to guide
    for(int idx_his = 0; idx_his < HISTORY_TABLE_SET ; idx_his++)
    {
        history_table_t *pointer = history_pointers[cpu][idx_his];
        do
        {
            // Look for the IPs that can launch this prefetch
            if (pointer->time <= cycle)
            {
                uint64_t his_addr = pointer->addr;
                if (his_addr != act_addr && ((act_addr - his_addr)<256))
                {
                    for (int i = 0; i < num_on_time; i++)
                    {
                        if (pointer->addr == timely_addr[i]) continue;
                    }
                    timely_addr[num_on_time] = pointer->addr;
                    num_on_time++;
                }
            }

            if (pointer == historyt[cpu][idx_his])
            {
                pointer = &historyt[cpu][idx_his][HISTORY_TABLE_WAY - 1];
            } else pointer--;
        } while (pointer != history_pointers[cpu][idx_his]);
    }
    return num_on_time;

    // We found on-time prefetchs
}


/******************************************************************************/
/*                      Latency table functions                               */
/******************************************************************************/
// Auxiliar history table functions
void vberti_increase_conf_ip(uint64_t tag, uint32_t cpu)
{
    if (vbertit[cpu].find(tag) == vbertit[cpu].end()) return;

    vberti_t *tmp = vbertit[cpu][tag];
    stride_t *aux = tmp->stride;

    tmp->conf += CONFIDENCE_INC;

    if (tmp->conf == CONFIDENCE_MAX) 
    {

        // Max confidence achieve
        for(int i = 0; i < BERTI_TABLE_STRIDE_SIZE; i++)
        {
            float temp = (float) aux[i].conf / (float) tmp->conf;
            uint64_t aux_conf   = (uint64_t) (temp * 100);

            // Set bits
            if (aux_conf > CONFIDENCE_L1) aux[i].rpl = L1;
            else if (aux_conf > CONFIDENCE_L2) aux[i].rpl = L2;
            else if (aux_conf > CONFIDENCE_L2R) aux[i].rpl = L2R;
            else aux[i].rpl = R;
            
            aux[i].conf = 0;
        }

        tmp->conf = 0;
    }
}

void pages_berti_increase_conf_ip(uint64_t page_addr, uint32_t cpu)
{
    if (pages_bertit[cpu].find(page_addr) == pages_bertit[cpu].end()) return;

    pages_berti_t *tmp = pages_bertit[cpu][page_addr];
    stride_t *aux = tmp->stride;

    tmp->conf += CONFIDENCE_INC;

    if (tmp->conf == CONFIDENCE_MAX) 
    {

        // Max confidence achieve
        for(int i = 0; i < BERTI_TABLE_STRIDE_SIZE; i++)
        {
            float temp = (float) aux[i].conf / (float) tmp->conf;
            uint64_t aux_conf   = (uint64_t) (temp * 100);

            // Set bits
            if (aux_conf > CONFIDENCE_L1) aux[i].rpl = L1;
            else if (aux_conf > CONFIDENCE_L2) aux[i].rpl = L2;
            else if (aux_conf > CONFIDENCE_L2R) aux[i].rpl = L2R;
            else aux[i].rpl = R;
            
            aux[i].conf = 0;
        }

        tmp->conf = 0;
    }
}


void vberti_table_add(uint64_t tag, uint32_t cpu, int64_t stride)
{
    /*
     * Save the new information into the history table
     *
     * Parameters:
     *  - tag: PC tag
     *  - cpu: actual cpu
     *  - stride: actual cpu
     */
    if (vbertit[cpu].find(tag) == vbertit[cpu].end())
    {
        // FIFO MAP
        if (vbertit_queue[cpu].size() > BERTI_TABLE_SIZE)
        {
            uint64_t key = vbertit_queue[cpu].front();
            vberti_t *tmp = vbertit[cpu][key];
            delete tmp->stride;
            delete tmp;
            vbertit[cpu].erase(vbertit_queue[cpu].front());
            vbertit_queue[cpu].pop();
        }
        vbertit_queue[cpu].push(tag);

        assert(vbertit[cpu].size() <= BERTI_TABLE_SIZE);

        vberti_t *tmp = new vberti_t;
        tmp->stride = new stride_t[BERTI_TABLE_STRIDE_SIZE]();
        
        // Confidence IP
        tmp->conf = CONFIDENCE_INC;

        // Create new stride
        tmp->stride[0].stride = stride;
        tmp->stride[0].conf = CONFIDENCE_INIT;
        tmp->stride[0].rpl = R;

        // Save value
        vbertit[cpu].insert(make_pair(tag, tmp));
        return;
    }

    vberti_t *tmp = vbertit[cpu][tag];
    stride_t *aux = tmp->stride;

    // Increase IP confidence
    uint8_t max = 0;

    for (int i = 0; i < BERTI_TABLE_STRIDE_SIZE; i++)
    {
        if (aux[i].stride == stride)
        {
            aux[i].conf += CONFIDENCE_INC;
            if (aux[i].conf > CONFIDENCE_MAX) aux[i].conf = CONFIDENCE_MAX;
            return;
        }
    }

    uint8_t dx_conf = 100;
    int dx_remove = -1;
    for (int i = 0; i < BERTI_TABLE_STRIDE_SIZE; i++)
    {
        if (aux[i].rpl == R && aux[i].conf < dx_conf)
        {
            dx_conf = aux[i].conf;
            dx_remove = i;
        }
    }

    if (dx_remove > -1)
    {
        tmp->stride[dx_remove].stride = stride;
        tmp->stride[dx_remove].conf   = CONFIDENCE_INIT;
        tmp->stride[dx_remove].rpl    = R;
        return;
    } else
    {
        for (int i = 0; i < BERTI_TABLE_STRIDE_SIZE; i++)
        {
            if (aux[i].rpl == L2R && aux[i].conf < dx_conf)
            {
                dx_conf = aux[i].conf;
                dx_remove = i;
            }
            //if (aux[i].rpl == L2R)
            //{
            //    tmp->stride[i].stride = stride;
            //    tmp->stride[i].conf   = CONFIDENCE_INIT;
            //    tmp->stride[i].rpl    = R;
            //    return;
            //}
        }
        if (dx_remove > -1)
        {
            tmp->stride[dx_remove].stride = stride;
            tmp->stride[dx_remove].conf   = CONFIDENCE_INIT;
            tmp->stride[dx_remove].rpl    = R;
            return;
        }
    }
}

void pages_berti_table_add(uint64_t page_addr, uint32_t cpu, int64_t stride)
{
    /*
     * Save the new information into the history table
     *
     * Parameters:
     *  - tag: PC tag
     *  - cpu: actual cpu
     *  - stride: actual cpu
     */
    if (pages_bertit[cpu].find(page_addr) == pages_bertit[cpu].end())
    {
        // FIFO MAP
        if (pages_bertit_queue[cpu].size() > BERTI_TABLE_SIZE)
        {
            uint64_t key = pages_bertit_queue[cpu].front();
            pages_berti_t *tmp = pages_bertit[cpu][key];
            delete tmp->stride;
            delete tmp;
            pages_bertit[cpu].erase(pages_bertit_queue[cpu].front());
            pages_bertit_queue[cpu].pop();
        }
        pages_bertit_queue[cpu].push(page_addr);

        assert(pages_bertit[cpu].size() <= BERTI_TABLE_SIZE);

        pages_berti_t *tmp = new pages_berti_t;
        tmp->stride = new stride_t[BERTI_TABLE_STRIDE_SIZE]();
        
        // Confidence IP
        tmp->conf = CONFIDENCE_INC;

        // Create new stride
        tmp->stride[0].stride = stride;
        tmp->stride[0].conf = CONFIDENCE_INIT;
        tmp->stride[0].rpl = R;

        // Save value
        pages_bertit[cpu].insert(make_pair(page_addr, tmp));
        return;
    }

    pages_berti_t *tmp = pages_bertit[cpu][page_addr];
    stride_t *aux = tmp->stride;

    // Increase IP confidence
    uint8_t max = 0;

    for (int i = 0; i < BERTI_TABLE_STRIDE_SIZE; i++)
    {
        if (aux[i].stride == stride)
        {
            aux[i].conf += CONFIDENCE_INC;
            if (aux[i].conf > CONFIDENCE_MAX) aux[i].conf = CONFIDENCE_MAX;
            return;
        }
    }

    uint8_t dx_conf = 100;
    int dx_remove = -1;
    for (int i = 0; i < BERTI_TABLE_STRIDE_SIZE; i++)
    {
        if (aux[i].rpl == R && aux[i].conf < dx_conf)
        {
            dx_conf = aux[i].conf;
            dx_remove = i;
        }
    }

    if (dx_remove > -1)
    {
        tmp->stride[dx_remove].stride = stride;
        tmp->stride[dx_remove].conf   = CONFIDENCE_INIT;
        tmp->stride[dx_remove].rpl    = R;
        return;
    } else
    {
        for (int i = 0; i < BERTI_TABLE_STRIDE_SIZE; i++)
        {
            if (aux[i].rpl == L2R && aux[i].conf < dx_conf)
            {
                dx_conf = aux[i].conf;
                dx_remove = i;
            }
            //if (aux[i].rpl == L2R)
            //{
            //    tmp->stride[i].stride = stride;
            //    tmp->stride[i].conf   = CONFIDENCE_INIT;
            //    tmp->stride[i].rpl    = R;
            //    return;
            //}
        }
        if (dx_remove > -1)
        {
            tmp->stride[dx_remove].stride = stride;
            tmp->stride[dx_remove].conf   = CONFIDENCE_INIT;
            tmp->stride[dx_remove].rpl    = R;
            return;
        }
    }
}

uint8_t vberti_table_get(uint64_t tag, uint32_t cpu, stride_t res[MAX_PF])
{
    /*
     * Save the new information into the history table
     *
     * Parameters:
     *  - tag: PC tag
     *  - cpu: actual cpu
     *
     * Return: the stride to prefetch
     */
    if (!vbertit[cpu].count(tag)) return 0;

    vberti_t *tmp = vbertit[cpu][tag];
    stride_t *aux = tmp->stride;
    uint64_t max_conf = 0;
    uint16_t dx = 0;
    
    for (int i = 0; i < BERTI_TABLE_STRIDE_SIZE; i++)
    {
        if (aux[i].stride != 0 && aux[i].rpl)
        {
            // Substitue min confidence for the next one
            res[dx].stride = aux[i].stride;
            res[dx].rpl = aux[i].rpl;
            dx++;
        }
    }

    if (dx == 0 && tmp->conf >= LANZAR_INT)
    {
        for (int i = 0; i < BERTI_TABLE_STRIDE_SIZE; i++)
        {
            if (aux[i].stride != 0)
            {
                // Substitue min confidence for the next one
                res[dx].stride = aux[i].stride;
                float temp = (float) aux[i].conf / (float) tmp->conf;
                uint64_t aux_conf   = (uint64_t) (temp * 100);
                res[dx].per = aux_conf;
                dx++;
            }
        }
        sort(res, res + MAX_PF, compare_greater_stride_t_per);

        for (int i = 0; i < MAX_PF; i++)
        {
            if (res[i].per > 80) res[i].rpl = L1;
            else if (res[i].per > 35) res[i].rpl = L2;
            //if (res[i].per > 80) res[i].rpl = L2;
            else res[i].rpl = R;
        }
        sort(res, res + MAX_PF, compare_greater_stride_t);
        return 1;
    }

    sort(res, res + MAX_PF, compare_greater_stride_t);

    return 1;
}


uint8_t pages_berti_table_get(uint64_t page_addr, uint32_t cpu, stride_t res[MAX_PF])
{
    /*
     * Save the new information into the history table
     *
     * Parameters:
     *  - page_addrt: (line_addr & ADDR_MASK) >> LOG2_BLOCKS_PER_PAGE
     *  - cpu: actual cpu
     *
     * Return: the stride to prefetch
     */
    if (!pages_bertit[cpu].count(page_addr)) return 0;

    pages_berti_t *tmp = pages_bertit[cpu][page_addr];
    stride_t *aux = tmp->stride;
    uint64_t max_conf = 0;
    uint16_t dx = 0;
    
    for (int i = 0; i < BERTI_TABLE_STRIDE_SIZE; i++)
    {
        if (aux[i].stride != 0 && aux[i].rpl)
        {
            // Substitue min confidence for the next one
            res[dx].stride = aux[i].stride;
            res[dx].rpl = aux[i].rpl;
            dx++;
        }
    }

    if (dx == 0 && tmp->conf >= LANZAR_INT)
    {
        for (int i = 0; i < BERTI_TABLE_STRIDE_SIZE; i++)
        {
            if (aux[i].stride != 0)
            {
                // Substitue min confidence for the next one
                res[dx].stride = aux[i].stride;
                float temp = (float) aux[i].conf / (float) tmp->conf;
                uint64_t aux_conf   = (uint64_t) (temp * 100);
                res[dx].per = aux_conf;
                dx++;
            }
        }
        sort(res, res + MAX_PF, compare_greater_stride_t_per);

        for (int i = 0; i < MAX_PF; i++)
        {
            if (res[i].per > 80) res[i].rpl = L1;
            else if (res[i].per > 35) res[i].rpl = L2;
            //if (res[i].per > 80) res[i].rpl = L2;
            else res[i].rpl = R;
        }
        sort(res, res + MAX_PF, compare_greater_stride_t);
        return 1;
    }

    sort(res, res + MAX_PF, compare_greater_stride_t);

    return 1;
}

void bop_deltas_table_init(uint32_t cpu)
{
    bop_local_best_delta[cpu].score = 0;
    bop_local_best_delta[cpu].delta = 0;
    bop_global_best_delta[cpu] = 0;
    bop_pf_init_finish[cpu] = false;
    int idx = 0;
    for (int i = 1; i < 256; i += 1)
    {
        int n = i;
        for (int j = 2; j <= 5; j += 1)
        {
            while (n % j == 0)
            {
                n /= j;
            }
        }
        if (n == 1)
        {
            bop_deltas_table[cpu][idx].delta=i;
            bop_deltas_table[cpu][idx].score=0;
            idx++;
        }       
    }

}

void bop_deltas_table_update(uint32_t cpu, int64_t delta)
{
    bool phase_end = false;
    for(int i = 0; i < BOP_DELTAS_NUM; i++)
    {
        bop_delta_entry &a = bop_deltas_table[cpu][i];
        if(a.delta == delta)
        {
            a.score++;
        }
        if(a.score > bop_local_best_delta[cpu].score)
        {
            bop_local_best_delta[cpu] = a;
        }
        if(a.score == BOP_MAX_SCORE)
        {
            phase_end = true;
        }
    }
    bop_learning_round[cpu]++;
    if(phase_end == true && bop_learning_round[cpu] == BOP_MAX_ROUND)
    {
        bop_pf_init_finish[cpu]=true;
        for(int i = 0; i < BOP_DELTAS_NUM; i++)
        {
            bop_delta_entry &b = bop_deltas_table[cpu][i];
            b.score = 0;
        }
        bop_global_best_delta[cpu] = bop_local_best_delta[cpu].delta;
    }
}

void find_and_update(uint32_t cpu, uint64_t latency, uint64_t tag, 
        uint64_t cycle, uint64_t line_addr)
{ 
    //************
    //line addr : line addr w/o ADDR_MASK

    //***************
    // We were tracking this miss
    uint64_t ip[HISTORY_TABLE_WAY];
    uint64_t addr[HISTORY_TABLE_WAY];
    uint16_t num_on_time = 0;

    #ifdef BERTI_IP_ON
    // Get the IPs that can launch a prefetch
    num_on_time = history_table_get(cpu, latency, tag, line_addr, ip, addr, cycle);
        //***********************ip*****************************//
    for (uint32_t i = 0; i < num_on_time; i++)
    {
        // Increase conf ip
        if (i == 0) vberti_increase_conf_ip(tag, cpu);
        
        // Max number of strides that we can find
        if (i >= MAX_HISTORY_IP) break;

        // Add information into berti table
        int64_t stride;
        line_addr &= ADDR_MASK;

        // Usually applications go from lower to higher memory position.
        // The operation order is important (mainly because we allow
        // negative strides)
        stride = (int64_t) (line_addr - addr[i]);

        if ((std::abs(stride) < (1 << STRIDE_MASK)))
        {
            // Only useful strides
            vberti_table_add(ip[i], cpu, stride);
        }
    }
    #endif

    #ifdef BERTI_PAGES_ON
    uint16_t pages_num_on_time = 0;
    uint64_t pages_addr[HISTORY_TABLE_SET*HISTORY_TABLE_WAY];
    pages_num_on_time = history_table_pages_get(cpu, latency, line_addr, pages_addr, cycle);
    //***********************pages*****************************//
    //access cache的时候还是需要更新pages_bertit的，只不过是在预取的时候，如果没有ip匹配的，那就使用pages_bertit
    for(uint32_t i = 0; i < pages_num_on_time ; i++)
    {
        if(i == 0) pages_berti_increase_conf_ip(((line_addr&ADDR_MASK)>>LOG2_BLOCKS_PER_PAGE),cpu);
        //if(i == 0) pages_berti_increase_conf_ip((line_addr>>LOG2_BLOCKS_PER_PAGE),cpu);
        if (i >= MAX_HISTORY_IP) break;

        // Add information into berti table
        int64_t stride;
        //line_addr &= ADDR_MASK;

        // Usually applications go from lower to higher memory position.
        // The operation order is important (mainly because we allow
        // negative strides)
        stride = (int64_t) ((ADDR_MASK&line_addr)- pages_addr[i]);

        if ((std::abs(stride) < (1 << STRIDE_MASK)))
        {
            // Only useful strides
            pages_berti_table_add(((line_addr&ADDR_MASK)>>LOG2_BLOCKS_PER_PAGE), cpu, stride);
            //pages_berti_table_add((line_addr>>LOG2_BLOCKS_PER_PAGE), cpu, stride);
        }
    }
    #else
    #endif

    #ifdef BOP_ON
    uint16_t bop_num_on_time;
    uint64_t timely_addr[HISTORY_TABLE_SET*HISTORY_TABLE_WAY];
    bop_num_on_time = history_table_bop_get(cpu, latency, line_addr, timely_addr, cycle);

    //***********************bop*****************************//
    for(uint32_t i = 0; i < bop_num_on_time ; i++)
    {
        int64_t delta = (line_addr & ADDR_MASK)-timely_addr[i];
        bop_deltas_table_update(cpu, delta);
    }
    #endif

}

void CACHE::l1d_prefetcher_initialize() 
{
    shadow_cache_init(cpu);
    latency_table_init(cpu);
    history_table_init(cpu);
    bop_deltas_table_init(cpu);
    #ifdef BINGO_BOP_ON
        prefetchers = vector<BOP>(NUM_CPUS, BOP((1 << LOG2_BLOCKS_PER_PAGE), RR_TABLE_SIZE, DEGREE));
    #endif
    std::cout << "History Sets: " << HISTORY_TABLE_SET << std::endl;
    std::cout << "History Ways: " << HISTORY_TABLE_WAY << std::endl;
    std::cout << "BERTI Size: " << BERTI_TABLE_SIZE << std::endl;
    std::cout << "BERTI Stride Size: " << BERTI_TABLE_STRIDE_SIZE << std::endl;
    #ifdef MLOP_ON
        /*=== MLOP Settings ===*/
        const int BLOCKS_IN_CACHE = CACHE::NUM_SET * CACHE::NUM_WAY;
        const int BLOCKS_IN_ZONE = PAGE_SIZE / BLOCK_SIZE;
        const int AMT_SIZE = 32 * BLOCKS_IN_CACHE / BLOCKS_IN_ZONE; /* size of access map table */

        /* maximum possible prefetch degree (the actual prefetch degree is usually much smaller) */
        const int PREFETCH_DEGREE = 16;

        /* number of score updates before selecting prefetch offsets (thus, it is also the maximum possible score) */
        const int NUM_UPDATES = 500;

        /* prefetch offsets with `score >= LX_THRESH * NUM_UPDATES` into LX */
        const double L1D_THRESH = 0.40; 
        const double L2C_THRESH = 0.30;
        const double LLC_THRESH = 2.00; /* off */
        /*======================*/

        /* construct prefetcher for all cores */
        L1D_PREF_2::prefetchers =
            vector<L1D_PREF_2::MLOP>(NUM_CPUS, L1D_PREF_2::MLOP(BLOCKS_IN_ZONE, AMT_SIZE, PREFETCH_DEGREE, NUM_UPDATES,
                                                L1D_THRESH, L2C_THRESH, LLC_THRESH, L1D_PREF_2::DEBUG_LEVEL));
    #endif
}

void CACHE::l1d_prefetcher_operate(uint64_t addr,uint64_t physical_addr, uint64_t ip, uint8_t cache_hit,
        uint8_t type, uint8_t critical_ip_flag)
{ 
    #ifdef MEMORY_ACCESS_PATTERN_DEBUG
        bool trigger_miss = false;
    #endif
    #ifdef BOP_DEBUG
        mtx.lock();
    #endif
    if(RECORD_IP_ADDR)
    {
        std::cout << "A access:" << std::endl;
    }
    assert(type == LOAD || type == RFO);  
    uint64_t line_addr = (addr >> LOG2_BLOCK_SIZE); // Line addr  
    uint64_t pc = ip;
    ip = ((ip >> 1) ^ (ip >> 4));
    //ip = (ip >> 1) ^ (ip >> 4) ^ (ip >> 8);
    ip = ip & IP_MASK;

    #ifdef BINGO_BOP_ON
      bool bingo_bop_triger = false;      
    #endif

    if (!cache_hit)
    {
        #ifdef MEMORY_ACCESS_PATTERN_DEBUG
            trigger_miss = true;
        #endif
        // This is a miss
    
        // Add @ to latency table
        latency_table_add(line_addr, ip, cpu, 1);

        // Add to history table
        history_table_add(ip, cpu, line_addr);
        if(RECORD_IP_ADDR)
        {
            std::cout << "cache miss" << std::endl;
        }
        #ifdef BINGO_BOP_ON
            bingo_bop_triger = true;
        #endif
        #ifdef MLOP_ON
            L1D_PREF_2::prefetchers[cpu].access(line_addr);
        #endif

    } else if (cache_hit && shadow_cache_is_pf(cpu, line_addr))
    {
        #ifdef MEMORY_ACCESS_PATTERN_DEBUG
            trigger_miss = true;
        #endif
        if(RECORD_IP_ADDR)
        {
            std::cout << "cache hit && is pf" << std::endl;
        }
        // Cache line access
        shadow_cache_pf(cpu, line_addr);

        // Buscar strides Y actualizar
        uint64_t latency = shadow_cache_latency(cpu, line_addr);
        find_and_update(cpu, latency, ip, current_core_cycle[cpu] & TIME_MASK, 
                line_addr);

        history_table_add(ip, cpu, line_addr); 
        #ifdef BINGO_BOP_ON
            bingo_bop_triger = true;
        #endif

        #ifdef MLOP_ON
            L1D_PREF_2::prefetchers[cpu].access(line_addr);
        #endif
    } else
    {
        // Cache line access
        shadow_cache_pf(cpu, line_addr);
        if(RECORD_IP_ADDR)
        {
            std::cout << "cache hit && no pf" << std::endl;
        }
        // No pf in hit
        //return;
    }
    #ifdef MEMORY_ACCESS_PATTERN_DEBUG
    //这里的地址应该为物理地址，因为用来索引cache了
    //full_addr为虚拟地址，full_physical_address为物理地址，address为虚拟的块地址
        //uint64_t line_addr_debug = (RQ.entry[RQ.head].full_addr >> LOG2_BLOCK_SIZE); // Line addr  
        uint64_t line_addr_debug = (physical_addr >> LOG2_BLOCK_SIZE);//物理地址
        uint64_t page_addr_debug = (line_addr_debug >> LOG2_BLOCKS_PER_PAGE);
        uint64_t page_addr_offset = (line_addr_debug %(1 << LOG2_BLOCKS_PER_PAGE));
        if(cache_type == IS_L1D && (type == RFO || type == LOAD) && (warmup_complete[cpu]==1) && trigger_miss)
        {
            // std::cout<<RQ.entry[index].ip << ' '<<page_addr_debug << ' '<<page_addr_offset<<' '<<line_addr_debug << std::endl;
            // std::cout << RQ.entry[RQ.head].address << " "<< RQ.entry[RQ.head].full_addr <<std::endl;
            // std::cout << (RQ.entry[RQ.head].full_addr >> LOG2_BLOCK_SIZE) << std::endl;
            act_ValuePair value;
            value.offset = page_addr_offset;
            value.ppaddr = page_addr_debug;
            value.vpaddr = line_addr >> LOG2_BLOCKS_PER_PAGE;
            // std::cout<<(RQ.entry[RQ.head].full_addr >> LOG2_BLOCK_SIZE)<< " "<<line_addr_debug<< std::endl;
            // std::cout << RQ.entry[index].address<< std::endl;
            insertEntry(act_dict,pc,value);
        }
    #endif
    // Get stride to prefetch
    stride_t stride[MAX_PF];
    for (int i = 0; i < MAX_PF; i++) 
    {
        stride[i].conf = 0;
        stride[i].stride = 0;
        stride[i].rpl = R;
    }

    
    // 打开文件流
    // 运行过程中的信息
    //******************IP prefetch**************
    if(RECORD_IP_ADDR)
    {
        std::cout << "PC is:"<< pc << " IP is: "<< ip <<" ADDR is:"<< addr << std::endl;
        std::cout << "IP hex is:"<< std::hex << ip <<" Line ADDR is:"<< std::hex << line_addr << std::dec << std::endl;
        std::cout << "Pages Addr is:"<< std::hex << ((line_addr&ADDR_MASK)>>LOG2_BLOCKS_PER_PAGE) << std::dec << std::endl;
    }
    int launched_ip = 0;
    #ifdef BERTI_IP_ON 
    if(!vberti_table_get(ip, cpu, stride))
    {
        if(RECORD_DELTAS)
        {
            std::cout << "IP berti deltas no found" << std::endl;
        }
    }
    else
    {
        if(RECORD_DELTAS)
        {
                std::cout << "IP berti deltas:" << std::endl;
        }
        for (int i = 0; i < MAX_PF_LAUNCH; i++)
        {
            uint64_t p_addr = (line_addr + stride[i].stride) << LOG2_BLOCK_SIZE;
            uint64_t p_b_addr = (p_addr >> LOG2_BLOCK_SIZE);

            //if (!shadow_cache_get(cpu, p_b_addr)
            if (!latency_table_get(p_addr, cpu))
            {

                int fill_level = FILL_L1;
                float mshr_load = ((float) MSHR.occupancy / (float) MSHR_SIZE) * 100;
                #ifdef BOP_DEBUG
                    std::cout << "IP MSHR: "<< mshr_load <<"sconf: " << stride[i].conf << "stride: "<< stride[i].stride <<std::endl;
                #endif

                // Level of prefetching depends son CONFIDENCE
                if (stride[i].rpl == L1 && mshr_load < MSHR_LIMIT)
                {
                    fill_level = FILL_L1;
                    if(RECORD_DELTAS)
                    {
                        std::cout << "deltas:"<< stride[i].stride << " L1" << " pref_addr:" \
                        <<std::hex << p_b_addr << std::dec<< std::endl;
                    }
                } else if (stride[i].rpl == L1 || stride[i].rpl == L2 
                        || stride[i].rpl == L2R ){
                    fill_level = FILL_L2;
                    if(RECORD_DELTAS)
                    {
                        std::cout << "deltas:"<< stride[i].stride << " L2" << " pref_addr:" \
                        <<std::hex << p_b_addr << std::dec<< std::endl;
                    }
                } else
                {
                    //return;
                    break;
                }
                
                //0b01:IP
                #ifdef PREFETCHER_CLASS_DEBUG
                uint32_t pf_metadata_encode_ip = metadata_encode(1,0b01);
                    if (prefetch_line(ip, addr, p_addr, fill_level, pf_metadata_encode_ip))
                #else
                    if (prefetch_line(ip, addr, p_addr, fill_level,1))
                #endif
                {
                    if(RECORD_DELTAS)
                    {
                        std::cout << "prefetch"<< std::endl;
                    }
                    launched_ip++;
                }
            }
        }
        #ifdef BOP_DEBUG
            std::cout << "IP NUMS: "<< launched_ip <<std::endl;
        #endif
    }
    #endif

    #ifdef BERTI_PAGES_ON
    for (int i = 0; i < MAX_PF; i++) 
    {
        stride[i].conf = 0;
        stride[i].stride = 0;
        stride[i].rpl = R;
    }
    int launched_pages = 0;
    //*********************pages prefetch*********************//
    if (!pages_berti_table_get(((line_addr&ADDR_MASK)>>LOG2_BLOCKS_PER_PAGE), cpu, stride)) 
    {
        if(RECORD_DELTAS)
        {
            std::cout << "Pages berti deltas no found" << std::endl;
        }
    }
    else
    {        
        if(RECORD_DELTAS)
        {
            std::cout << "Pages berti deltas:" << std::endl;
        }
        for (int i = 0; i < MAX_PF_LAUNCH; i++)
        {
            uint64_t p_addr = (line_addr + stride[i].stride) << LOG2_BLOCK_SIZE;
            uint64_t p_b_addr = (p_addr >> LOG2_BLOCK_SIZE);

            if (!latency_table_get(p_addr, cpu))
            {

                int fill_level = FILL_L1;
                float mshr_load = ((float) MSHR.occupancy / (float) MSHR_SIZE) * 100;
                #ifdef BOP_DEBUG
                    std::cout << "PAGES MSHR: "<< mshr_load <<"sconf: " << stride[i].conf << "stride: "<< stride[i].stride <<std::endl;
                #endif

                // Level of prefetching depends son CONFIDENCE
                if (stride[i].rpl == L1 && mshr_load < MSHR_LIMIT)
                {
                    fill_level = FILL_L1;
                    if(RECORD_DELTAS)
                    {
                        std::cout << "deltas:"<< stride[i].stride << " L1" << " pref_addr:" \
                        <<std::hex << p_b_addr << std::dec<< std::endl;
                    }
                } else if (stride[i].rpl == L1 || stride[i].rpl == L2 
                        || stride[i].rpl == L2R ){
                    fill_level = FILL_L2;
                    if(RECORD_DELTAS)
                    {
                        std::cout << "deltas:"<< stride[i].stride << " L2" << " pref_addr:" \
                        <<std::hex << p_b_addr << std::dec<< std::endl;
                    }
                } else
                {
                    //return;
                    break;
                }

                //0b10:Pages
                #ifdef PREFETCHER_CLASS_DEBUG
                uint32_t pf_metadata_encode_pages = metadata_encode(1,0b10);
                
                if (prefetch_line(ip, addr, p_addr, fill_level, pf_metadata_encode_pages))
                #else
                    if (prefetch_line(ip, addr, p_addr, fill_level, 1))
                #endif
                {
                    if(RECORD_DELTAS)
                    {
                        std::cout << "prefetch"<< std::endl;
                    }
                    launched_pages++;
                }
            }

        }
        #ifdef BOP_DEBUG
            std::cout << "PAGES NUMS: "<< launched_pages <<std::endl;
        #endif
    }
    #endif

    #ifdef BOP_ON
    int launched_bop = 0;
    //***************bop prefetch******************//
    if(bop_pf_init_finish[cpu] == true)
    {
        uint64_t p_addr = (line_addr + bop_global_best_delta[cpu]) << LOG2_BLOCK_SIZE;
        uint64_t p_b_addr = (p_addr >> LOG2_BLOCK_SIZE);
        if (prefetch_line(ip, addr, p_addr, FILL_L1, 1))
        {
            launched++;
        }
    }
    #endif

    #ifdef BINGO_BOP_ON
    int launched_bop = 0;
        if(bingo_bop_triger == true)
        {
            /* call prefetcher and send prefetches */
            //prefetchers是BOP类的一个数组，在CACHE初始化的时候同时进行初始化
            vector<uint64_t> to_prefetch = prefetchers[cpu].access(line_addr);
            for (auto &pf_block_number : to_prefetch) {
                uint64_t pf_address = pf_block_number << LOG2_BLOCK_SIZE;
                prefetch_line(ip, addr, pf_address, FILL_L1,1);
                // /* champsim automatically ignores prefetches that cross page boundaries */
                // float mshr_load = ((float) MSHR.occupancy / (float) MSHR_SIZE) * 100;
                // #ifdef BOP_DEBUG
                //     std::cout << "BOP L1 " << "MSHR: " << mshr_load <<std::endl;
                // #endif
                // //0b11:bop
                // #ifdef PREFETCHER_CLASS_DEBUG
                // uint32_t pf_metadata_encode_bop = metadata_encode(1,0b11);
                // #endif
                // if (!latency_table_get(pf_address, cpu)){
                    
                //     if((mshr_load < (MSHR_LIMIT + 10)) && ((launched_ip + launched_pages)< MAX_PF_LAUNCH))
                //     {   
                //         #ifdef PREFETCHER_CLASS_DEBUG
                //         prefetch_line(ip, addr, pf_address, FILL_L1,pf_metadata_encode_bop);
                //         #else
                //         prefetch_line(ip, addr, pf_address, FILL_L1,1);
                //         #endif
                //     }
                //     else
                //     {
                //         #ifdef PREFETCHER_CLASS_DEBUG
                //         prefetch_line(ip, addr, pf_address, FILL_L1,pf_metadata_encode_bop);
                //         #else
                //         prefetch_line(ip, addr, pf_address, FILL_L1,1);
                //         #endif
                //     }
                //     launched_bop++;
                // }               
            }
        }
        #ifdef BOP_DEBUG
            std::cout << "BOP NUMS " << launched_bop <<std::endl;
        #endif
    #endif

    #ifdef BOP_DEBUG
        mtx.unlock();
    #endif

    #ifdef MLOP_ON
        L1D_PREF_2::prefetchers[cpu].mark(line_addr, L1D_PREF_2::State::ACCESS);
        L1D_PREF_2::prefetchers[cpu].prefetch(this, line_addr);
        L1D_PREF_2::prefetchers[cpu].track(line_addr);
    #endif

    return;
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
    uint64_t tag     = latency_table_get_ip(line_addr, cpu);
    uint64_t cycle   = latency_table_get(line_addr, cpu);
    uint64_t latency = latency_table_del(line_addr, cpu);

    if (latency > LAT_MASK) latency = 0;

    // Add to the shadow cache
    shadow_cache_add(cpu, set, way, line_addr, prefetch, latency);

    if (latency != 0 && !prefetch)
    {
        find_and_update(cpu, latency, tag, cycle, line_addr);
    }

    #ifdef BINGO_BOP_ON
        prefetchers[cpu].cache_fill(line_addr, (bool)prefetch);
    #endif
}

void CACHE::l1d_prefetcher_final_stats()
{
}


#ifdef PREFETCHER_CLASS_DEBUG
//对应的decode版本定义在cache.cc和cache.h中
//metadata[8:7]来做标记：01：IP， 10：Pages 11：bop
    uint32_t metadata_encode(uint32_t metadata_origin, uint32_t prefetcher_type)
    {
        uint32_t mask = ~(0b11 << 7); // 屏蔽位，位8和位7为0，其它位为1
        uint32_t setting = (prefetcher_type & 0b11) << 7; // 设定值，位8和位7为你所需要的值，其它位为0
        return (metadata_origin & mask) | setting; // 清除位8和位7并设置为新值
    }
#endif