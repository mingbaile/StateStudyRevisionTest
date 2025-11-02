import json
import os
from collections import defaultdict
import sys


def extract_state_variables_and_reassignments(ast_file):
    with open(ast_file, 'r', encoding='utf-8') as file:
        ast_data = json.load(file)
    state_variables = {
        'initialized': defaultdict(list),
        'reassigned': defaultdict(list),
        'mapping_dict': defaultdict(list)
    }

    def process_statement(statement):
        if statement.get('type') == 'ExpressionStatement':
            expression = statement.get('expression', {})
            if expression.get('type') == 'BinaryOperation' and expression.get('operator') in ('=', '+='):
                process_expression(expression.get('left', {}))

                if expression.get('left', {}).get('type') == 'IndexAccess':
                    left_exp = expression.get('left', {})
                    if left_exp.get('base', {}).get('type') == 'Identifier':
                        base_expr = left_exp.get('base', {})
                        mapping_name = base_expr.get('name')
                        right_expression = expression.get('right')
                        if right_expression.get('type') == "BooleanLiteral":
                            mapping_value = right_expression.get('value')
                            if mapping_value not in state_variables['mapping_dict'][mapping_name]:
                                state_variables['mapping_dict'][mapping_name].append(mapping_value)
                        if right_expression.get('type') == "Identifier":
                            mapping_value = right_expression.get('name')
                            if mapping_value not in state_variables['mapping_dict'][mapping_name]:
                                state_variables['mapping_dict'][mapping_name].append(mapping_value)
                        if right_expression.get('type') == 'FunctionCall':
                            function_sub = right_expression.get('expression', {})
                            if function_sub.get('type') == "Identifier" and function_sub.get('name') == "address":
                                for arg in right_expression.get('arguments', []):
                                    if arg.get('type') == 'NumberLiteral' and arg.get('number') == '0':
                                        if 'address(0)' not in state_variables['mapping_dict'][mapping_name]:
                                            state_variables['mapping_dict'][mapping_name].append('address(0)')

                if expression.get('right', {}).get('type') == 'UnaryOperation':
                    process_expression(expression.get('right', {}))

            elif expression.get('type') == 'FunctionCall':
                for arg in expression.get('arguments', []):
                    if arg.get('type') == 'UnaryOperation':
                        process_expression(arg.get('subExpression', {}))
                    if arg.get('type') == 'BinaryOperation' and arg.get('operator') in ('=', '+=', '=='):
                        process_expression(arg.get('left', {}))
                        if arg.get('right', {}).get('type') == 'UnaryOperation':
                            process_expression(arg.get('right', {}))
                member_access = expression.get('expression', {})
                if member_access.get('type') == 'MemberAccess':
                    base_expression = member_access.get('expression', {})
                    if base_expression.get('type') == 'FunctionCall':
                        base_expression = get_deepest_expression(base_expression)
                    process_expression(base_expression)

            elif expression.get('type') == 'UnaryOperation':

                if expression.get('operator') == 'delete':
                    del_map_expression = expression.get('subExpression', {})
                    if del_map_expression.get('type') == 'IndexAccess':
                        base_map_expression = del_map_expression.get('base', {})

                sub_expression = expression.get('subExpression', {})
                process_expression(sub_expression)

        elif statement.get('type') in ['ForStatement', 'WhileStatement', 'DoWhileStatement']:
            body = statement.get('body', {})
            for inner_statement in body.get('statements', []):
                process_statement(inner_statement)
        elif statement.get('type') == 'IfStatement':
            true_body = statement.get('trueBody', {})
            if true_body:
                for inner_statement in true_body.get('statements', []):
                    process_statement(inner_statement)
            false_body = statement.get('falseBody', {})
            if false_body:
                for inner_statement in false_body.get('statements', []):
                    process_statement(inner_statement)
        elif statement.get('type') == 'UncheckedStatement':
            unchecked_statement = statement.get('block', {})
            statements = unchecked_statement.get('statements', [])
            for inner_statement in statements:
                if inner_statement['type'] == 'ExpressionStatement':
                    process_statement(inner_statement)
                if inner_statement['type'] == 'IfStatement':
                    process_statement(inner_statement)
                if inner_statement['type'] == 'ReturnStatement':
                    process_expression(inner_statement.get('expression', {}))

        elif statement.get('type') == 'InlineAssemblyStatement':
            assembly_statement = statement.get('body', {})
            if assembly_statement.get('type') == 'AssemblyBlock':
                for operation in assembly_statement.get('operations', []):
                    if operation.get('type') == 'AssemblyCall':
                        if operation.get('functionName') == 'sstore':
                            arguments = operation.get('arguments', [])
                            if arguments:
                                first_argument = arguments[0]
                                if first_argument.get('type') == 'AssemblyMemberAccess':
                                    process_expression(first_argument.get('expression', {}))
        elif statement.get('type') == 'ReturnStatement':
            return_expression = statement.get('expression', {})
            if return_expression and isinstance(return_expression, dict):
                if return_expression.get('type') == 'FunctionCall':
                    return_expression = get_deepest_expression(return_expression)
                    process_expression(return_expression)

    def process_expression(expression):
        if expression.get('type') == 'Identifier':
            var_name = expression.get('name')
            if var_name in state_variables['initialized']:
                state_variables['reassigned'][var_name].append(ast_file)
            else:
                function_details = find_function_details_from_expression(ast_data, expression)
                if function_details:
                    function_name = function_details[0]
                    parameter_names = function_details[1]
                    if var_name in parameter_names:
                        param_index = parameter_names.index(var_name)
                        actual_args = find_actual_arguments_for_parameter(ast_data, function_name, param_index)
                        for actual_name in actual_args:
                            if actual_name in state_variables['initialized']:
                                state_variables['reassigned'][actual_name].append(ast_file)
        elif expression.get('type') == 'IndexAccess':
            base_expression = expression.get('base', {})
            process_expression(base_expression)
        elif expression.get('type') == 'UnaryOperation':
            sub_expression = expression.get('subExpression', {})
            process_expression(sub_expression)
        elif expression.get('type') == 'MemberAccess':
            mem_expression = get_deepest_expression(expression)
            process_expression(mem_expression)

    def get_deepest_expression(expression):
        if expression.get('type') == 'FunctionCall':
            return get_deepest_expression(expression.get('expression', {}))
        elif expression.get('type') == 'MemberAccess':
            return get_deepest_expression(expression.get('expression', {}))
        return expression

    def find_function_details_from_expression(ast, expression_node):
        parent_map = {}
        def build_parent_map(node, parent=None):
            if isinstance(node, dict):
                for key, value in node.items():
                    if isinstance(value, dict):
                        parent_map[id(value)] = node
                        build_parent_map(value, node)
                    elif isinstance(value, list):
                        for item in value:
                            if isinstance(item, dict):
                                parent_map[id(item)] = node
                                build_parent_map(item, node)

        def find_function_from_expression(expression, node):
            if node.get('type') == 'FunctionDefinition':
                return node
            parent = parent_map.get(id(node))
            if parent is None:
                return None
            return find_function_from_expression(expression, parent)

        def extract_parameters_from_function(function_node):
            parameters = function_node.get('parameters', [])
            return [param.get('name') for param in parameters if 'name' in param]

        build_parent_map(ast)
        function_node = find_function_from_expression(expression_node, parent_map[id(expression_node)])
        if function_node:
            function_name = function_node.get('name', None)
            parameter_names = extract_parameters_from_function(function_node)
            return (function_name, parameter_names)
        return ()

    def find_actual_arguments_for_parameter(ast, function_name, param_index):
        actual_arguments = []

        def traverse2(node):
            if isinstance(node, dict):
                if node.get('type') == 'FunctionCall':
                    expression = node.get('expression', {})
                    if expression.get('type') == 'Identifier' and expression.get('name') == function_name:
                        arguments = node.get('arguments', [])
                        if len(arguments) > param_index:
                            actual_argument = arguments[param_index]
                            if actual_argument.get('type') == 'Identifier':
                                actual_arguments.append(actual_argument.get('name'))
                            if actual_argument.get('type') == 'IndexAccess':
                                base_actual_expression = actual_argument.get('base', {})
                                actual_arguments.append(base_actual_expression.get('name'))
                                if base_actual_expression.get('type') == 'IndexAccess':
                                    base_actual_expression2 = base_actual_expression.get('base', {})
                                    actual_arguments.append(base_actual_expression2.get('name'))
                for key, value in node.items():
                    if isinstance(value, (dict, list)):
                        traverse2(value)
            elif isinstance(node, list):
                for item in node:
                    traverse2(item)
        traverse2(ast)
        return actual_arguments

    def traverse(node):
        if isinstance(node, dict):
            if node.get('type') == 'StateVariableDeclaration':
                for var in node.get('variables', []):
                    if not var.get('isDeclaredConst') and not var.get('isImmutable'):
                        var_name = var.get('name')
                        state_variables['initialized'][var_name].append(ast_file)

            if node.get('type') in ['FunctionDefinition', 'ModifierDefinition']:
                function_body = node.get('body', {})
                if isinstance(function_body, dict):
                    for statement in function_body.get('statements', []):
                        process_statement(statement)
            for key, value in node.items():
                if isinstance(value, (dict, list)):
                    traverse(value)
        elif isinstance(node, list):
            for item in node:
                traverse(item)
    traverse(ast_data)
    return state_variables

def process_project(project_folder):
    all_initialized = defaultdict(list)
    all_reassigned = defaultdict(list)
    all_mapping = defaultdict(list)

    for root, dirs, files in os.walk(project_folder):
        for file in files:
            if file.endswith('.json'):
                ast_file_path = os.path.join(root, file)
                state_variables = extract_state_variables_and_reassignments(ast_file_path)
                for var_name, files_list in state_variables['initialized'].items():
                    all_initialized[var_name].extend(files_list)
                for var_name, files_list in state_variables['reassigned'].items():
                    all_reassigned[var_name].extend(files_list)
                for mapping_name, mapping_value in state_variables['mapping_dict'].items():
                    all_mapping[mapping_name].extend(mapping_value)
    unmodified_vars = {}
    for var_name in all_initialized:
        if var_name not in all_reassigned:
            unmodified_vars[var_name] = all_initialized[var_name]

    return {
        'initialized': all_initialized,
        'reassigned': all_reassigned,
        'unmodified': unmodified_vars
    }

def process_directory(base_dir):
    for project in os.listdir(base_dir):
        project_folder = os.path.join(base_dir, project)
        if os.path.isdir(project_folder):
            print(f"Processing project: {project}\n")
            result = process_project(project_folder)

            if not result['unmodified']:
                print("This project has no problematic variables.\n")
            else:
                for var_name, files in result['unmodified'].items():
                    display_files = {fp.replace('_ast.json', '.sol') if fp.endswith('_ast.json') else fp
                                    for fp in files}
                    display_files = {fp.replace('ASTJsonFiles\\', '') for fp in display_files}
                    print(f"problematic state variable: \n {var_name} \n"
                        f"Declared in files: \n {', '.join(display_files)}\n")
                    # print(f"problematic state variable:  {var_name} (Declared in files: {', '.join(set(files))})\n")
            print(f"=" * 100 + "\n")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python process_state_variables.py <output_dir>")
        sys.exit(1)

    base_dir = sys.argv[1]
    process_directory(base_dir)
