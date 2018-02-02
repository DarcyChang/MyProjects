__author__ = 'akhanov'

import ast
import os
import glob


def __get_var_path(attribute_node):
    # We need to drill down into nested Attribute nodes. When we reach a Name node, we're done.
    node = attribute_node
    chain = []

    # If we see an attribute, we need to go deeper
    while isinstance(node, ast.Attribute):
        # The nesting order is reversed, so we un-reverse it by inserting namespace names to the beginning of the list
        chain.insert(0, node.attr)
        # Set the level to the current one
        node = node.value

    # We reach the name node
    if isinstance(node, ast.Name):
        chain.insert(0, node.id)

    return ".".join(chain)


def __get_decorator_names(ast_node):
    ret = []
    # Fetch list of procedures
    procs = []

    for i in ast.walk(ast_node):
        if isinstance(i, ast.FunctionDef):
            procs.append(i)

    # Look at decorator list of each procedure
    for i in procs:
        # Retrieve the name of the decorator
        for dec in i.decorator_list:
            name = ""
            # A decorator can be either a Name (name of function)
            # or a Call (decorator generator)

            if isinstance(dec, ast.Name):
                name = dec.id
            elif isinstance(dec, ast.Call):
                name = __get_var_path(dec.func)

            ret.append(name)

    return ret


def __get_cafe_aliases(ast_node):
    ret = ["cafe.test_suite", "cafe.runner.decorators.test_suite"]

    for i in ast.walk(ast_node):
        if isinstance(i, ast.Import):
            pass
        elif isinstance(i, ast.ImportFrom):
            for alias in i.names:
                if (i.module == "cafe" or i.module == "cafe.runner.decorators") and alias.name == "test_suite":
                    if alias.asname is None:
                        ret.append(alias.name)
                    else:
                        ret.append(alias.asname)

        elif isinstance(i, ast.Assign):
            val = ""

            if isinstance(i.value, ast.Call):
                val = __get_var_path(i.value.func)

            elif isinstance(i.value, ast.Name) or isinstance(i.value, ast.Attribute):
                val = __get_var_path(i.value)

            # We need to compare ret, not a static list, because there might be several levels of assignment!
            if val in ret:
                for target in i.targets:
                    ret.append(__get_var_path(target))

    return ret


def has_test_suite(filename):
    with open(filename, 'r') as f:
        src = f.read()

    # Module-level AST node
    try:
        syntax_tree = ast.parse(src, os.path.basename(filename))
    except SyntaxError as e:
        print("ERROR: Could not analyze file '%s' for test suites due to syntax errors in the file." % filename)
        return False

    cafe_aliases = __get_cafe_aliases(syntax_tree)
    used_decorators = __get_decorator_names(syntax_tree)

    ret = False

    for i in used_decorators:
        if i in cafe_aliases:
            ret = True
            break

    return ret


if __name__ == "__main__":
    path = os.path.abspath(os.path.expanduser("../demo"))

    for node in os.walk(path):
        subdir = node[0]

        for tc_file in glob.glob(subdir + os.path.sep + "*.py"):
            print("%s: %s" % (tc_file, has_test_suite(tc_file)))


