
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'ADD ADD_TAGS DELETE DELETE_TAGS F FILENAME GET LIST Q T WORDinput : instructioninstruction : add_inst\n                   | query_inst\n                   | add_tags_inst\n                   | delete_tags_instadd_inst : ADD F file_list T tag_listquery_inst : inst Q tag_queryadd_tags_inst : ADD_TAGS Q tag_query T tag_listdelete_tags_inst : DELETE_TAGS Q tag_query T tag_listinst : DELETE\n            | LIST\n            | GETfile_list : FILENAME\n                 | FILENAME file_listtag_list : WORD\n                | WORD tag_listtag_query : WORD\n                 | WORD tag_query'
    
_lr_action_items = {'ADD':([0,],[7,]),'ADD_TAGS':([0,],[9,]),'DELETE_TAGS':([0,],[10,]),'DELETE':([0,],[11,]),'LIST':([0,],[12,]),'GET':([0,],[13,]),'$end':([1,2,3,4,5,6,20,21,26,29,30,31,32,33,],[0,-1,-2,-3,-4,-5,-7,-17,-18,-6,-15,-8,-9,-16,]),'F':([7,],[14,]),'Q':([8,9,10,11,12,13,],[15,16,17,-10,-11,-12,]),'FILENAME':([14,19,],[19,19,]),'WORD':([15,16,17,21,24,27,28,30,],[21,21,21,21,30,30,30,30,]),'T':([18,19,21,22,23,25,26,],[24,-13,-17,27,28,-14,-18,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'input':([0,],[1,]),'instruction':([0,],[2,]),'add_inst':([0,],[3,]),'query_inst':([0,],[4,]),'add_tags_inst':([0,],[5,]),'delete_tags_inst':([0,],[6,]),'inst':([0,],[8,]),'file_list':([14,19,],[18,25,]),'tag_query':([15,16,17,21,],[20,22,23,26,]),'tag_list':([24,27,28,30,],[29,31,32,33,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> input","S'",1,None,None,None),
  ('input -> instruction','input',1,'p_input','ply_parser.py',47),
  ('instruction -> add_inst','instruction',1,'p_instruction','ply_parser.py',51),
  ('instruction -> query_inst','instruction',1,'p_instruction','ply_parser.py',52),
  ('instruction -> add_tags_inst','instruction',1,'p_instruction','ply_parser.py',53),
  ('instruction -> delete_tags_inst','instruction',1,'p_instruction','ply_parser.py',54),
  ('add_inst -> ADD F file_list T tag_list','add_inst',5,'p_add_inst','ply_parser.py',58),
  ('query_inst -> inst Q tag_query','query_inst',3,'p_query_inst','ply_parser.py',64),
  ('add_tags_inst -> ADD_TAGS Q tag_query T tag_list','add_tags_inst',5,'p_add_tags_inst','ply_parser.py',70),
  ('delete_tags_inst -> DELETE_TAGS Q tag_query T tag_list','delete_tags_inst',5,'p_delete_tags_inst','ply_parser.py',76),
  ('inst -> DELETE','inst',1,'p_inst','ply_parser.py',82),
  ('inst -> LIST','inst',1,'p_inst','ply_parser.py',83),
  ('inst -> GET','inst',1,'p_inst','ply_parser.py',84),
  ('file_list -> FILENAME','file_list',1,'p_file_list','ply_parser.py',93),
  ('file_list -> FILENAME file_list','file_list',2,'p_file_list','ply_parser.py',94),
  ('tag_list -> WORD','tag_list',1,'p_tag_list','ply_parser.py',101),
  ('tag_list -> WORD tag_list','tag_list',2,'p_tag_list','ply_parser.py',102),
  ('tag_query -> WORD','tag_query',1,'p_tag_query','ply_parser.py',109),
  ('tag_query -> WORD tag_query','tag_query',2,'p_tag_query','ply_parser.py',110),
]