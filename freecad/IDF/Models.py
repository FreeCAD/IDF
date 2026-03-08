# SPDX-License-Identifier: LGPL-2.1-or-later
# SPDX-FileCopyrightText: 2012 Milos Koutny <milos.koutny@gmail.com>
# SPDX-FileNotice: Part of the IDF addon.


def split_records(line_record):
    """split_records(line_record)-> list of strings(records)

       standard separator list separator is space, records containing encapsulated by " """
    split_result=[]
    quote_pos=line_record.find('"')
    while quote_pos!=-1:
       if quote_pos>0:
          split_result.extend(line_record[ :quote_pos].split())
          line_record=line_record[quote_pos: ]
          quote_pos=line_record.find('"',1)
       else:
          quote_pos=line_record.find('"',1)
       if quote_pos!=-1:
          split_result.append(line_record[ :quote_pos+1])
          line_record=line_record[quote_pos+1: ]
       else:
          split_result.append(line_record)
          line_record=""
       quote_pos=line_record.find('"')
    split_result.extend(line_record.split())
    return split_result