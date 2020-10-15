# -*- coding: utf-8 -*-
# author: Tiancheng Zhao

from simdial.agent.user import User
from simdial.agent.system import System
from simdial.channel import ActionChannel, WordChannel
from simdial.agent.nlg import SysNlg, UserNlg
from simdial.complexity import Complexity
from simdial.domain import Domain
import progressbar
import json
import numpy as np
import sys
import os
import re
import pdb

class Generator(object):
    """
    The generator class used to generate synthetic slot-filling human-computer conversation in any domain. 
    The generator can be configured to generate data with varying complexity at: propositional, interaction and social 
    level. 
    
    The required input is a domain specification dictionary + a configuration dict.
    """

    @staticmethod
    def pack_msg(speaker, utt, **kwargs):
        resp = {k: v for k, v in kwargs.items()}
        resp["speaker"] = speaker
        resp["utt"] = utt
        return resp

    @staticmethod
    def pprint(dialogs, in_json, domain_spec, output_file=None):
        """
        Print the dailog to a file or STDOUT
        
        :param dialogs: a list of dialogs generated
        :param output_file: None if print to STDOUT. Otherwise write the file in the path
        """
        f = sys.stdout if output_file is None else open(output_file, "w")

        if in_json:
            # combo = {'dialogs': dialogs, 'meta': domain_spec.to_dict()}
            json.dump(dialogs, f, indent=4)
        else:
            for idx, d in enumerate(dialogs):
                f.write("## DIALOG %d ##\n" % idx)
                for turn in d:
                    speaker, utt, actions = turn["speaker"], turn["utt"], turn["actions"]
                    if utt:
                        str_actions = utt
                    else:
                        str_actions = " ".join([a.dump_string() for a in actions])
                    if speaker == "USR":
                        f.write("%s(%f)-> %s\n" % (speaker, turn['conf'], str_actions))
                    else:
                        f.write("%s -> %s\n" % (speaker, str_actions))

        if output_file is not None:
            f.close()

    @staticmethod
    def print_db(database, in_json, domain_spec, output_file=None):
        """
        print the database to a file or STDOUT

        :param database: a database class generated in database.py
        """
        f = sys.stdout if output_file is None else open(output_file, "w")

        if in_json:
            combo = []
            for idx, entry in enumerate(database.sys_table):
                usr_table_entry = database.table[idx]
                tmp_dict = {
                            "type" : domain_spec.name,
                            "name"   : str(idx)
                            }
                for i in range(database.num_sys_slots):
                    tmp_dict[domain_spec.sys_slots[i][0]] = domain_spec.sys_slots[i][2][entry[i + 1]]

                for i in range(database.num_usr_slots):
                    tmp_dict[domain_spec.usr_slots[i][0]] = domain_spec.usr_slots[i][2][usr_table_entry[i]]

                combo.append(tmp_dict)

            json.dump(combo, f, indent=4)

        if output_file is not None:
            f.close()

    @staticmethod
    def print_OTGY(domain_spec, in_json, output_file=None):
        f = sys.stdout if output_file is None else open(output_file, "w")

        if in_json:
            info_dict = {}

            for usr_slot in domain_spec.usr_slots:
                info_dict[usr_slot[0]] = usr_slot[-1]
            for sys_slot in domain_spec.sys_slots:
                info_dict[sys_slot[0]] = sys_slot[-1]

            combo = {"informable" : info_dict}
        json.dump(combo, f, indent=4)

        if output_file is not None:
            f.close()

    @staticmethod
    def print_stats(dialogs):
        """
        Print some basic stats of the dialog.
        
        :param dialogs: A list of dialogs generated.
        """
        print("%d dialogs" % len(dialogs))
        all_lens = [len(d) for d in dialogs]
        print("Avg len {} Max Len {}".format(np.mean(all_lens), np.max(all_lens)))

        total_cnt = 0.
        kb_cnt = 0.
        ratio = []
        for d in dialogs:
            local_cnt = 0.
            for t in d:
                total_cnt +=1
                if 'QUERY' in t['utt']:
                    kb_cnt += 1
                    local_cnt += 1
            ratio.append(local_cnt/len(d))
        print(kb_cnt/total_cnt)
        print(np.mean(ratio))

    def gen(self, domain, complexity, num_sess=1):
        """
        Generate synthetic dialogs in the given domain. 

        :param domain: a domain specification dictionary
        :param complexity: an implmenetaiton of Complexity
        :param num_sess: how dialogs to generate
        :return: a list of dialogs. Each dialog is a list of turns.
        """
        dialogs = []
        action_channel = ActionChannel(domain, complexity)
        word_channel = WordChannel(domain, complexity)

        # natural language generators
        sys_nlg = SysNlg(domain, complexity)
        usr_nlg = UserNlg(domain, complexity)

        sys_slots_list = [slot.name for slot in domain.sys_slots if slot.name != '#default']

        bar = progressbar.ProgressBar(maxval=num_sess)
        bar.start()

        for i in range(num_sess):
            bar.update(i)
            usr = User(domain, complexity)
            sys = System(domain, complexity)

            # begin conversation
            noisy_usr_as = []
            dialog = []
            conf = 1.0
            turn_num = 0

            sys_r, sys_t, sys_as, sys_s = sys.step(noisy_usr_as, conf)
            sys_utt, sys_str_as = sys_nlg.generate_sent(sys_as, domain=domain)

            # set domain name
            domain_name = domain.name
            if domain_name == "rest_pitt" or \
                domain_name == "restaurant_style":
                domain_name = "restaurant"

            while True:

                if sys_t:
                    break

                usr_r, usr_t, usr_as = usr.step(sys_as)

                # passing through noise, nlg and noise!
                noisy_usr_as, conf = action_channel.transmit2sys(usr_as)
                usr_utt = usr_nlg.generate_sent(noisy_usr_as)
                noisy_usr_utt = word_channel.transmit2sys(usr_utt)
                # dialog.append(self.pack_msg("USR", noisy_usr_utt, actions=noisy_usr_as, conf=conf, domain=domain.name))

                # make a decision
                sys_r, sys_t, sys_as, sys_s = sys.step(noisy_usr_as, conf)
                sys_utt, sys_str_as = sys_nlg.generate_sent(sys_as, domain=domain)
                # dialog.append(self.pack_msg("SYS", sys_utt, actions=sys_str_as, domain=domain.name, state=state))

                if "\"RET\"" in noisy_usr_utt:
                    # change the last dialogue

                    dialog[-1]["sys"]["sent"] = sys_utt

                else:
                    # append a new dialogue

                    usr_tmp_dict = {
                                    # "transcript" : domain_name + " " + noisy_usr_utt,
                                    "transcript" : noisy_usr_utt,
                                    "slu"        : [] 
                                    }
                    for inform_dict in sys_s["usr_slots"]:
                        if inform_dict["max_val"] != None:
                            usr_tmp_dict["slu"].append({
                                                        "act"   : "inform",
                                                        "slots" : [[
                                                                    inform_dict["name"][1:],
                                                                    inform_dict["max_val"]
                                                                    ]]    
    
                                                        })
                    for action_dict in noisy_usr_as:
                        if action_dict["act"] == "request" and  \
                            action_dict["parameters"][0][0] in sys_slots_list:
                        
                            usr_tmp_dict["slu"].insert(0, {
                                                           "act"   : "request",
                                                           "slots" : [[
                                                                       "slot",
                                                                       action_dict["parameters"][0][0][1:]]]
    
                    })


                    sys_tmp_dict = {
                                    # "sent" : domain_name + " " + sys_utt
                                    "sent" : sys_utt
                                    }

                    dialog.append({
                                   "turn" : turn_num,
                                   "usr"  : usr_tmp_dict,
                                   "sys"  : sys_tmp_dict
                                  })
    
                    turn_num += 1

            # print("turn_num: ", turn_num, '\n')


            dialogs.append({"dial" : dialog})       

        return dialogs

    def gen_corpus(self, name, domain_spec, complexity_spec, size):
        if not os.path.exists(name):
            os.mkdir(name)

        # create meta specifications
        domain = Domain(domain_spec)

        # generate the database file
        db_json_file_name = "{}-{}-{}-DB.{}".format(domain_spec.name,
                                         complexity_spec.__name__,
                                         size, 'json')

        db_json_file_path = os.path.join(name, db_json_file_name)
        self.print_db(domain.db, True, domain_spec, db_json_file_path)

        # generate the entity file(OTGY.json)
        OTGY_json_file_name = "{}-{}-{}-OTGY.{}".format(domain_spec.name,
                                         complexity_spec.__name__,
                                         size, 'json')

        OTGY_json_file_path = os.path.join(name, OTGY_json_file_name)
        self.print_OTGY(domain_spec, True, OTGY_json_file_path)               



        complex = Complexity(complexity_spec)

        # generate the corpus conditioned on domain & complexity
        corpus = self.gen(domain, complex, num_sess=size)

        # txt_file = "{}-{}-{}.{}".format(domain_spec.name,
        #                                complexity_spec.__name__,
        #                                size, 'txt')

        json_file = "{}-{}-{}.{}".format(domain_spec.name,
                                         complexity_spec.__name__,
                                         size, 'json')

        json_file = os.path.join(name, json_file)
        self.pprint(corpus, True, domain_spec, json_file)
        print("\nfinishing generating %s dialogue in domain: %s with complexity: %s \n" \
             %(size, domain_spec.name, complexity_spec.__name__))
        # self.print_stats(corpus)
