grammar command_parser_grammar;

input: instruction EOF;
instruction: add_inst | query_inst | add-tags_inst | delete-tags_inst;

add_inst: 'add' file_list tag_list;
query_inst: inst tag_query;
add_tags_inst: 'add-tags' tag_query tag_list;
delete_tags_inst: 'delete-tags' tag_query tag_list;
inst: 'delete' | 'list' | 'get';

file_list: '-f' FILENAME+;
tag_list: '-t' WORD+;
tag_query: '-q' WORD+;

FILENAME: ~[/\s]+;
WORD: [a-zA-Z0-9_-]+;