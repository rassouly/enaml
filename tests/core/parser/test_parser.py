#------------------------------------------------------------------------------
# Copyright (c) 2018, Nucleic Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#------------------------------------------------------------------------------
import ast


def validate_ast(py_node, enaml_node, dump_ast=False, offset=0):
    """Validate each node of an ast against another ast.

    Typically used to compare an AST generated by the Python paser and one
    generated by the enaml parser.

    """
    if dump_ast:
        print('Python node:\n', ast.dump(py_node))
        print('Enaml node:\n', ast.dump(enaml_node))
    assert type(py_node) == type(enaml_node)
    if isinstance(py_node, ast.AST):
        for name, field in ast.iter_fields(py_node):
            if name == 'ctx':
                assert type(field) == type(getattr(enaml_node, name))
            elif name not in ('lineno', 'col_offset'):
                field2 = getattr(enaml_node, name, None)
                print('    '*offset, 'Validating:', name)
                validate_ast(field, field2, offset=offset+1)
    elif isinstance(py_node, list):
        if len(py_node) != len(enaml_node):
            return False
        for i, n1 in enumerate(py_node):
            print('    '*offset, 'Validating', i+1, 'th element')
            validate_ast(n1, enaml_node[i], offset=offset+1)
    else:
        assert py_node == enaml_node
