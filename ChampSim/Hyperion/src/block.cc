#include "block.h"

//返回队列中地址相匹配的条目的索引
int PACKET_QUEUE::check_queue(PACKET *packet)
{
    if ((head == tail) && occupancy == 0)
        return -1;

    if (head < tail) {
        for (uint32_t i=head; i<tail; i++) {
            if (NAME == "L1D_WQ") {
                if (entry[i].full_addr == packet->full_addr) {
                    DP (if (warmup_complete[packet->cpu]) {
                    cout << "[" << NAME << "] " << __func__ << " cpu: " << packet->cpu << " instr_id: " << packet->instr_id << " same address: " << hex << packet->address;
                    cout << " full_addr: " << packet->full_addr << dec << " by instr_id: " << entry[i].instr_id << " index: " << i;
                    cout << " cycle " << packet->event_cycle << endl; });
                    return i;
                }
            }
            else {
                if (entry[i].address == packet->address) {
                //cout << "address = "<< packet->address << " size=" <<sizeof(packet->address) << endl;
                    DP (if (warmup_complete[packet->cpu]) {
                    cout << "[" << NAME << "] " << __func__ << " cpu: " << packet->cpu << " instr_id: " << packet->instr_id << " same address: " << hex << packet->address;
                    cout << " full_addr: " << packet->full_addr << dec << " by instr_id: " << entry[i].instr_id << " index: " << i;
                    cout << " cycle " << packet->event_cycle << endl; });
                    return i;
                }
            }
        }
    }
    else {
        for (uint32_t i=head; i<SIZE; i++) {
            if (NAME == "L1D_WQ") {
                if (entry[i].full_addr == packet->full_addr) {
                //cout << "full_addr = "<< packet->full_addr << "size=" << sizeof(packet->full_addr)<<endl;
                    DP (if (warmup_complete[packet->cpu]) {
                    cout << "[" << NAME << "] " << __func__ << " cpu: " << packet->cpu << " instr_id: " << packet->instr_id << " same address: " << hex << packet->address;
                    cout << " full_addr: " << packet->full_addr << dec << " by instr_id: " << entry[i].instr_id << " index: " << i;
                    cout << " cycle " << packet->event_cycle << endl; });
                    return i;
                }
            }
            else {
                if (entry[i].address == packet->address) {
                    DP (if (warmup_complete[packet->cpu]) {
                    cout << "[" << NAME << "] " << __func__ << " cpu: " << packet->cpu << " instr_id: " << packet->instr_id << " same address: " << hex << packet->address;
                    cout << " full_addr: " << packet->full_addr << dec << " by instr_id: " << entry[i].instr_id << " index: " << i;
                    cout << " cycle " << packet->event_cycle << endl; });
                    return i;
                }
            }
        }
        for (uint32_t i=0; i<tail; i++) {
            if (NAME == "L1D_WQ") {
                if (entry[i].full_addr == packet->full_addr) {
                    DP (if (warmup_complete[packet->cpu]) {
                    cout << "[" << NAME << "] " << __func__ << " cpu: " << packet->cpu << " instr_id: " << packet->instr_id << " same address: " << hex << packet->address;
                    cout << " full_addr: " << packet->full_addr << dec << " by instr_id: " << entry[i].instr_id << " index: " << i;
                    cout << " cycle " << packet->event_cycle << endl; });
                    return i;
                }
            }
            else {
                if (entry[i].address == packet->address) {
                    DP (if (warmup_complete[packet->cpu]) {
                    cout << "[" << NAME << "] " << __func__ << " cpu: " << packet->cpu << " instr_id: " << packet->instr_id << " same address: " << hex << packet->address;
                    cout << " full_addr: " << packet->full_addr << dec << " by instr_id: " << entry[i].instr_id << " index: " << i;
                    cout << " cycle " << packet->event_cycle << endl; });
                    return i;
                }
            }
        }
    }

    return -1;
}

void PACKET_QUEUE::add_queue(PACKET *packet)
{
#ifdef SANITY_CHECK
    if (occupancy && (head == tail))
        assert(0);
#endif

    // add entry
    entry[tail] = *packet;

    DP ( if (warmup_complete[packet->cpu]) {
    cout << "[" << NAME << "] " << __func__ << " cpu: " << packet->cpu << " instr_id: " << packet->instr_id;
    cout << " address: " << hex << entry[tail].address << " full_addr: " << entry[tail].full_addr << dec;
    cout << " head: " << head << " tail: " << tail << " occupancy: " << occupancy << " event_cycle: " << entry[tail].event_cycle << endl; });


#ifdef PRINT_QUEUE_TRACE
    if(packet->instr_id == QTRACE_INSTR_ID)
    {
        cout << "[" << NAME << "] " << __func__ << " cpu: " << packet->cpu << " instr_id: " << packet->instr_id;
        cout << " address: " << hex << entry[tail].address << " full_addr: " << entry[tail].full_addr << dec;
        cout << " head: " << head << " tail: " << tail << " occupancy: " << occupancy << " event_cycle: " << entry[tail].event_cycle <<endl;
    }
#endif



    occupancy++;
    tail++;
    if (tail >= SIZE)
        tail = 0;
}

void PACKET_QUEUE::remove_queue(PACKET *packet)
{
#ifdef SANITY_CHECK
    if ((occupancy == 0) && (head == tail))
        assert(0);
#endif

    DP ( if (warmup_complete[packet->cpu]) {
    cout << "[" << NAME << "] " << __func__ << " cpu: " << packet->cpu << " instr_id: " << packet->instr_id;
    cout << " address: " << hex << packet->address << " full_addr: " << packet->full_addr << dec << " fill_level: " << packet->fill_level;
    cout << " head: " << head << " tail: " << tail << " occupancy: " << occupancy << " event_cycle: " << packet->event_cycle << endl; });

#ifdef PRINT_QUEUE_TRACE
    if(packet->instr_id == QTRACE_INSTR_ID)
    {
        cout << "[" << NAME << "] " << __func__ << " cpu: " << packet->cpu << " instr_id: " << packet->instr_id;
        cout << " address: " << hex << packet->address << " full_addr: " << packet->full_addr << dec << " fill_level: " << packet->fill_level;
        cout << " head: " << head << " tail: " << tail << " occupancy: " << occupancy << " event_cycle: " << packet->event_cycle <<endl;
    }
#endif


    // reset entry
    PACKET empty_packet;
    *packet = empty_packet;

    occupancy--;
    head++;
    if (head >= SIZE)
        head = 0;
}
