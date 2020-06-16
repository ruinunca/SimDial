#!/usr/bin/env python3
#
import sys, os
import pdb
import json
import argparse



def combine_log():
    pass

def combine_db():
    pass

def combine_otgy(source_domain, target_domain, datasize, data_path):

    all_slots = {'informable':{}}
    combined_otgy_name = []

    # # # source domain
    for dom in source_domain:
        # pdb.set_trace()
        with open(os.path.join(data_path, dom+'-MixSpec-1500-OTGY.json'), 'r', encoding='utf-8') as otgy:
            slots = json.loads(otgy.read().lower())
        for slot_type in slots['informable']:
            # pdb.set_trace()
            if slot_type in all_slots['informable']:
                all_slots['informable'][slot_type] += slots['informable'][slot_type]
            else:
                all_slots['informable'][slot_type] = slots['informable'][slot_type]

        combined_otgy_name.append(dom[0])

    # # # target domain
    if target_domain != '':
        with open(os.path.join(data_path, target_domain+'-MixSpec-'+str(datasize)+'-OTGY.json'), 'r', encoding='utf-8') as otgy:
            slots = json.loads(otgy.read().lower())
        for slot_type in slots['informable']:
            if slot_type in all_slots['informable']:
                all_slots['informable'][slot_type] += slots['informable'][slot_type]
            else:
                all_slots['informable'][slot_type] = slots['informable'][slot_type]

        combined_otgy_name.append(str(datasize) + target_domain[0])

    combined_otgy_path = os.path.join(data_path, '_'.join(combined_otgy_name)+'-OTGY.json')

    with open(combined_otgy_path, 'w') as co:
        json.dump(all_slots, co, indent=2)



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-log', default=True)
    parser.add_argument('-db',   default=True)
    parser.add_argument('-otgy', default=True)
    parser.add_argument('-source_domain', default=['restaurant', 'weather', 'bus'])
    parser.add_argument('-target_domain', default='movie')
    parser.add_argument('-data_path', default='./1500_data_fixed_0/')
    parser.add_argument('-datasize', default=15)
    args = parser.parse_args()


    if args.log:
        combine_log()
    if args.db:
        combine_db()
    if args.otgy:
        combine_otgy(args.source_domain, args.target_domain, args.datasize, args.data_path)

if __name__ == "__main__":
    main()