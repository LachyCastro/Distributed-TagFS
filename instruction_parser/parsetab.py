
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'ADD ADD_TAGS AND DELETE DELETE_TAGS F FILENAME GET LIST LPAREN NOT OR Q RPAREN STAR T WORDinput : instructioninstruction : add_inst\n                   | query_inst\n                   | add_tags_inst\n                   | delete_tags_instadd_inst : ADD F file_list T tag_listquery_inst : inst Q tag_query_or_staradd_tags_inst : ADD_TAGS Q tag_query_or_star T tag_listdelete_tags_inst : DELETE_TAGS Q tag_query_or_star T tag_listinst : DELETE\n            | LIST\n            | GETfile_list : FILENAME\n                 | FILENAME file_listtag_list : WORD\n                | WORD tag_listtag_query_or_star : STAR\n                         | tag_query\n    tag_query : tag_query AND basic_tag_query\n                 | tag_query OR basic_tag_query\n                 | basic_tag_query\n    basic_tag_query : NOT basic_tag_query\n                       | WORD\n                       | LPAREN tag_query RPAREN'
    
_lr_action_items = {'ADD':([0,],[7,]),'ADD_TAGS':([0,],[9,]),'DELETE_TAGS':([0,],[10,]),'DELETE':([0,],[11,]),'LIST':([0,],[12,]),'GET':([0,],[13,]),'$end':([1,2,3,4,5,6,20,21,22,23,25,33,37,38,39,40,41,42,43,44,],[0,-1,-2,-3,-4,-5,-7,-17,-18,-21,-23,-22,-6,-15,-19,-20,-24,-8,-9,-16,]),'F':([7,],[14,]),'Q':([8,9,10,11,12,13,],[15,16,17,-10,-11,-12,]),'FILENAME':([14,19,],[19,19,]),'STAR':([15,16,17,],[21,21,21,]),'NOT':([15,16,17,24,26,31,32,],[24,24,24,24,24,24,24,]),'WORD':([15,16,17,24,26,29,31,32,35,36,38,],[25,25,25,25,25,38,25,25,38,38,38,]),'LPAREN':([15,16,17,24,26,31,32,],[26,26,26,26,26,26,26,]),'T':([18,19,21,22,23,25,27,28,30,33,39,40,41,],[29,-13,-17,-18,-21,-23,35,36,-14,-22,-19,-20,-24,]),'AND':([22,23,25,33,34,39,40,41,],[31,-21,-23,-22,31,-19,-20,-24,]),'OR':([22,23,25,33,34,39,40,41,],[32,-21,-23,-22,32,-19,-20,-24,]),'RPAREN':([23,25,33,34,39,40,41,],[-21,-23,-22,41,-19,-20,-24,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'input':([0,],[1,]),'instruction':([0,],[2,]),'add_inst':([0,],[3,]),'query_inst':([0,],[4,]),'add_tags_inst':([0,],[5,]),'delete_tags_inst':([0,],[6,]),'inst':([0,],[8,]),'file_list':([14,19,],[18,30,]),'tag_query_or_star':([15,16,17,],[20,27,28,]),'tag_query':([15,16,17,26,],[22,22,22,34,]),'basic_tag_query':([15,16,17,24,26,31,32,],[23,23,23,33,23,39,40,]),'tag_list':([29,35,36,38,],[37,42,43,44,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> input","S'",1,None,None,None),
  ('input -> instruction','input',1,'p_input','ply_parser.py',102),
  ('instruction -> add_inst','instruction',1,'p_instruction','ply_parser.py',106),
  ('instruction -> query_inst','instruction',1,'p_instruction','ply_parser.py',107),
  ('instruction -> add_tags_inst','instruction',1,'p_instruction','ply_parser.py',108),
  ('instruction -> delete_tags_inst','instruction',1,'p_instruction','ply_parser.py',109),
  ('add_inst -> ADD F file_list T tag_list','add_inst',5,'p_add_inst','ply_parser.py',113),
  ('query_inst -> inst Q tag_query_or_star','query_inst',3,'p_query_inst','ply_parser.py',119),
  ('add_tags_inst -> ADD_TAGS Q tag_query_or_star T tag_list','add_tags_inst',5,'p_add_tags_inst','ply_parser.py',125),
  ('delete_tags_inst -> DELETE_TAGS Q tag_query_or_star T tag_list','delete_tags_inst',5,'p_delete_tags_inst','ply_parser.py',131),
  ('inst -> DELETE','inst',1,'p_inst','ply_parser.py',137),
  ('inst -> LIST','inst',1,'p_inst','ply_parser.py',138),
  ('inst -> GET','inst',1,'p_inst','ply_parser.py',139),
  ('file_list -> FILENAME','file_list',1,'p_file_list','ply_parser.py',148),
  ('file_list -> FILENAME file_list','file_list',2,'p_file_list','ply_parser.py',149),
  ('tag_list -> WORD','tag_list',1,'p_tag_list','ply_parser.py',156),
  ('tag_list -> WORD tag_list','tag_list',2,'p_tag_list','ply_parser.py',157),
  ('tag_query_or_star -> STAR','tag_query_or_star',1,'p_tag_query_or_star','ply_parser.py',164),
  ('tag_query_or_star -> tag_query','tag_query_or_star',1,'p_tag_query_or_star','ply_parser.py',165),
  ('tag_query -> tag_query AND basic_tag_query','tag_query',3,'p_tag_query','ply_parser.py',173),
  ('tag_query -> tag_query OR basic_tag_query','tag_query',3,'p_tag_query','ply_parser.py',174),
  ('tag_query -> basic_tag_query','tag_query',1,'p_tag_query','ply_parser.py',175),
  ('basic_tag_query -> NOT basic_tag_query','basic_tag_query',2,'p_basic_tag_query','ply_parser.py',183),
  ('basic_tag_query -> WORD','basic_tag_query',1,'p_basic_tag_query','ply_parser.py',184),
  ('basic_tag_query -> LPAREN tag_query RPAREN','basic_tag_query',3,'p_basic_tag_query','ply_parser.py',185),
]
