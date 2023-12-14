import ast

class PyCheckMate:
    def __init__(self, source_code):
        self.source_code = source_code#rf"""{source_code}""" #source_code
        self.compilable = False
        try:
            self.source_tree = ast.parse(self.source_code)
            self.compilable = True
        except SyntaxError:
            pass

    def does_compile(self):
        """Checks if the sourcecode has syntax errors returns dictionary with 'passed', which is a bool and 'note', which is a string"""
        valid: bool = True
        has_lineno: bool = False
        try:
            #ast.parse(self.source_code)
            compile(self.source_code, "<string>", "exec")
        except Exception as e:
            has_lineno = hasattr(e, "lineno")
            if has_lineno:
                error_line_number = e.lineno - 1
            error_type = e.__class__.__name__
            valid = False

        if not valid:
            if has_lineno:
                note = f"Code contains {error_type} at line {error_line_number}."
            else:
                note = f"Code contains {error_type}"
        else:
            note = "Code contains no syntax errors."

        return {
            'passed': valid,
            'note': note
        }

    def print_ast(self):
        """"Print the ast with an indendation of 4 spaces. Need to have at least Python 3.9 installed due to the indent param of ast.dump"""
        if self.compilable:
            print(ast.dump(self.source_tree, indent=4))
        else:
            return self.does_compile()

    def has_variable(self, variablename_to_check: str):
        if self.compilable:
            call_visitor = _CallVisitor()
            call_visitor.visit(self.source_tree)

            found = False
            for visited_assign in call_visitor.assigns:
                for assign_target in visited_assign.targets:
                    #single assign
                    if isinstance(assign_target, ast.Name):
                        if assign_target.id == variablename_to_check:
                            found = True
                    # tuple assign
                    elif isinstance(assign_target, ast.Tuple):
                        for assign_tuple in assign_target.elts:
                            if isinstance(assign_tuple, ast.Name):
                                if assign_tuple.id == variablename_to_check:
                                    found = True


            if found == False:
                note = f"Variable '{variablename_to_check}' not found."
            else:
                note = f"Variable '{variablename_to_check}' found."

            return {
                'passed': found,
                'note': note
            }

        else:
            return self.does_compile()

    def built_in_function_used(self, function_to_use: str):
        """Checks if the function_to_use is used in the sourcecode and returns dictionary with 'passed', which is a bool and 'note', which is a string"""
        if self.compilable:

            call_visitor = _CallVisitor()
            call_visitor.visit(self.source_tree)

            found = False

            for node in ast.walk(self.source_tree):
                if isinstance(node, ast.Expr) or isinstance(node, ast.Assign):
                    if isinstance(node, ast.Expr):
                        for visited_expr in call_visitor.expr:
                            call_visitor_expr = _CallVisitor()
                            call_visitor_expr.visit(visited_expr)
                            for visited_calls in call_visitor_expr.calls:
                                #check for a method
                                if isinstance(visited_calls.func, ast.Attribute) and visited_calls.func.attr == function_to_use:
                                    found = True
                                #check for a function
                                if isinstance(visited_calls.func, ast.Name) and visited_calls.func.id == function_to_use:
                                    found = True

                    else:
                        for visited_assign in call_visitor.assigns:
                            call_visitor_assign = _CallVisitor()
                            call_visitor_assign.visit(visited_assign)
                            for visited_calls in call_visitor_assign.calls:
                                # check for a method
                                if isinstance(visited_calls.func, ast.Attribute) and visited_calls.func.attr == function_to_use:
                                    found = True
                                # check for a function
                                if isinstance(visited_calls.func, ast.Name) and visited_calls.func.id == function_to_use:
                                    found = True
            #T.B.D.: Differentiate in feedbacknote between function and method
            if found == False:
                note = f"Function '{function_to_use}' was not used."
            else:
                note = f"Function '{function_to_use}' used."

            return {
                'passed': found,
                'note': note
            }

        else:
            return self.does_compile()

    def has_class(self, classname_to_check: str, number_of_parameters: int = None):
        """Checks if the class is defined in the sourcecode and returns dictionary with 'passed', which is a bool and 'note', which is a string"""
        if self.compilable:
            visitor = _DefinitionVisitor()
            visitor.visit(self.source_tree)

            found = False
            note = f"Class '{classname_to_check}' not found."
            for visited_classes in visitor.classes:
                if visited_classes.name == classname_to_check:
                    if number_of_parameters is not None:
                        note = f"Class '{classname_to_check}' found, but does not have the correct number of parameters."

                        class_args, class_vararg, class_kwarg = self._get_class_parameters(visited_classes)
                        if len(class_args) == number_of_parameters:
                            found = True
                            note = f"Class '{classname_to_check}' found."

                    else:
                        found = True
                        note = f"Class '{classname_to_check}' found."

            return {
                'passed': found,
                'note': note
            }
        else:
            return self.does_compile()

    def class_has_parameters(self, classname_to_check: str, required_args: dict, required_vararg: (str | bool) = None, required_kwarg: (str | bool) = None):
        """
        Checks if a class has specific types of parameters and checks their type and default value, returns dictionary with 'passed', which is a bool and 'note', which is a string

        Keyword arguments:
        classname_to_check -- the name as string of the function to check
        required_args -- dictionary of parameter definitions, has to follow structure as below:
        example_required_args = {
            'parameter_name': {
                'type': int
                'default': 3
            },
            'second_parameter_name': {
                'type': string
            },
            'third_parameter_name': {
            }
        }
        required_vararg -- bool or name of parameter to pass a variable number of arguments to the function. If None, vararg is not checked.
        required_kwarg -- bool or name of parameter to pass a variable number of keyworded arguments to the function. If None, kwarg is not checked.
        """
        if self.compilable:
            visitor = _DefinitionVisitor()
            visitor.visit(self.source_tree)

            if self.has_class(classname_to_check=classname_to_check)['passed'] is False:
                return {
                    'passed': False,
                    'note': f"Class '{classname_to_check}' not found."
                }

            for visited_classes in visitor.classes:
                if visited_classes.name == classname_to_check:
                    return self.function_has_parameters("__init__", required_args, required_vararg, required_kwarg)



        else:
            return self.does_compile()

    def class_has_attributes(self, classname_to_check: str, required_attributes: set):
        """
        Checks if a class has specific instance attributes (self.<...>), returns dictionary with 'passed', which is a bool and 'note', which is a string.
        Can not check for instance attributes that have been inherited.

        Keyword arguments:
        classname_to_check -- the name as string of the function to check
        required_attributes -- set of attribute names
        """
        if self.compilable:
            definition_visitor = _DefinitionVisitor()
            definition_visitor.visit(self.source_tree)

            if self.has_class(classname_to_check=classname_to_check)['passed'] is False:
                return {
                    'passed': False,
                    'note': f"Class '{classname_to_check}' not found."
                }

            for visited_classes in definition_visitor.classes:
                if visited_classes.name == classname_to_check:
                    call_visitor = _CallVisitor()
                    call_visitor.visit(visited_classes)

                    attributes = set()
                    for assign in call_visitor.assigns:
                        for target in assign.targets:
                            if isinstance(target, ast.Attribute):
                                if isinstance(target.value, ast.Name) and isinstance(target.attr, str):
                                    if target.value.id == "self":
                                        attributes.add(target.attr)

            missing_attributes = set()
            for attr in required_attributes:
                if attr not in attributes:
                    missing_attributes.add(attr)

            if len(missing_attributes) == 0:
                return {
                    'passed': True,
                    'note': f"Class '{classname_to_check}' has all required attributes."
                }
            else:
                return {
                    'passed': False,
                    'note': f"Class '{classname_to_check}' is missing the following attributes: {missing_attributes}"
                }


        else:
            return self.does_compile()

    def class_has_function(self, classname_to_check: str, functionname_to_check: str):
        """
        Checks if a class has a specific function, returns dictionary with 'passed', which is a bool and 'note', which is a string

        Keyword arguments:
        classname_to_check -- the name as string of the function to check
        required_attributes -- set of attribute names
        """
        if self.compilable:
            if self.has_class(classname_to_check=classname_to_check)['passed'] is False:
                return {
                    'passed': False,
                    'note': f"Class '{classname_to_check}' not found."
                }

            visitor = _DefinitionVisitor()
            visitor.visit(self.source_tree)
            found = False
            note =  f"Class '{classname_to_check}' has no function / method '{functionname_to_check}'."
            for visited_classes in visitor.classes:
                if visited_classes.name == classname_to_check:
                    function_visitor = _FunctionVisitor()
                    function_visitor.visit(visited_classes)

                    for visited_function in function_visitor.functions:
                        if visited_function.name == functionname_to_check:
                           found = True
                           note = f"Function / method '{functionname_to_check}' found in class '{classname_to_check}'."

            return {
                'passed': found,
                'note': note
            }

        else:
            return self.does_compile()

    def has_function(self, functionname_to_check: str, number_of_parameters: int = None):
        """Checks if the function is defined in the sourcecode and returns dictionary with 'passed', which is a bool and 'note', which is a string"""
        if self.compilable:
            visitor = _FunctionVisitor()
            visitor.visit(self.source_tree)
            found = False
            note = f"Function '{functionname_to_check}' not found."
            for visited_function in visitor.functions:
                if visited_function.name == functionname_to_check:
                    if number_of_parameters is not None:
                        note = f"Function '{functionname_to_check}' found, but does not have the correct number of parameters."
                        function_args, function_vararg, function_kwarg = self._get_function_parameters(visited_function)
                        if len(function_args) == number_of_parameters:
                            found = True
                            note = f"Function '{functionname_to_check}' found."
                    else:
                        found = True
                        note = f"Function '{functionname_to_check}' found."


            return {
                'passed': found,
                'note': note
            }
        else:
            return self.does_compile()

    def has_functions(self, function_definitions: set):
        """Checks if the functions are defined in the sourcecode and returns dictionary with 'passed', which is a bool and 'note', which is a string"""
        if self.compilable:
            functions_missing = []
            valid = True
            for function in function_definitions:
                #if (self.has_function(function, function_definitions[function])["passed"] == False):
                if (self.has_function(function)["passed"] == False):
                    functions_missing.append(function)

            if len(functions_missing):
                notes = []
                valid = False
                for function_missing in functions_missing:
                    notes.append(f"Function '{function_missing}' not found.")
                note = "\n".join(notes)
            else:
                note = "All functions found."

            return {
                'passed': valid,
                'note': note
            }
        else:
            return self.does_compile()

    def function_has_variable(self, functionname_to_check: str, variablename_to_check: str):
        """Checks if a variable is defined in a function and returns dictionary with 'passed', which is a bool and 'note', which is a string"""
        if self.compilable:
            function_visitor = _FunctionVisitor()
            function_visitor.visit(self.source_tree)

            if self.has_function(functionname_to_check=functionname_to_check)['passed'] is False:
                return {
                    'passed': False,
                    'note': f"Function '{functionname_to_check}' not found"
                }

            call_visitor = _CallVisitor()

            found = False

            for visited_function in function_visitor.functions:
                if visited_function.name == functionname_to_check:
                    call_visitor.visit(visited_function)
                    for visited_assign in call_visitor.assigns:
                        for assign_target in visited_assign.targets:
                            # single assign
                            if isinstance(assign_target, ast.Name):
                                if assign_target.id == variablename_to_check:
                                    found = True
                            # tuple assign
                            elif isinstance(assign_target, ast.Tuple):
                                for assign_tuple in assign_target.elts:
                                    if isinstance(assign_tuple, ast.Name):
                                        if assign_tuple.id == variablename_to_check:
                                            found = True

                    if found == False:
                        note = f"Variable '{variablename_to_check}' not found in function '{functionname_to_check}'."
                    else:
                        note = f"Variable '{variablename_to_check}' found in function '{functionname_to_check}'."

            return {
                'passed': found,
                'note': note
            }
        else:
            return self.does_compile()

    #def function_has_parameters(self, functionname_to_check: str, required_parameters: dict):
    def function_has_parameters(self, functionname_to_check: str, required_args: dict, required_vararg: (str | bool) = None, required_kwarg: (str | bool) = None):
        """
        Checks if a function has specific types of parameters and checks their type and default value, returns dictionary with 'passed', which is a bool and 'note', which is a string

        Keyword arguments:
        functionname_to_check -- the name as string of the function to check
        required_args -- dictionary of parameter definitions, has to follow structure as below:
        example_required_args = {
            'parameter_name': {
                'type': 'int'
                'default': 3
            },
            'second_parameter_name': {
                'type': 'string'
            },
            'third_parameter_name': {
            }
        }
        required_vararg -- bool or name of parameter to pass a variable number of arguments to the function. If None, vararg is not checked.
        required_kwarg -- bool or name of parameter to pass a variable number of keyworded arguments to the function. If None, kwarg is not checked.
        """
        if self.compilable:
            visitor = _FunctionVisitor()
            visitor.visit(self.source_tree)

            if self.has_function(functionname_to_check=functionname_to_check)['passed'] is False:
                return {
                    'passed': False,
                    'note': f"Function '{functionname_to_check}' not found."
                }

            missing_parameters = {}
            valid = True
            for visited_function in visitor.functions:
                if (visited_function.name == functionname_to_check):
                    function_args, function_vararg, function_kwarg = self._get_function_parameters(visited_function)

                    # check arguments
                    for required_parameter in required_args:
                        if required_parameter in function_args:
                            if 'type' in required_args[required_parameter]:
                                if required_args[required_parameter]['type'] != \
                                        function_args[required_parameter]['type']:
                                    missing_parameters[required_parameter] = {}
                                    missing_parameters[required_parameter]['type'] = \
                                    function_args[required_parameter]['type']
                                    valid = False
                                # else:
                                #    valid = True

                            if 'default' in required_args[required_parameter]:
                                if required_args[required_parameter]['default'] != \
                                        function_args[required_parameter]['default']:
                                    missing_parameters[required_parameter] = {}
                                    missing_parameters[required_parameter]['default'] = \
                                    function_args[required_parameter]['default']
                                    valid = False
                                # else:
                                #    valid = True
                        else:
                            missing_parameters[required_parameter] = {}
                            valid = False

            notes = []

            # generate feedback for arguments
            if len(missing_parameters):
                valid = False

                for wrongParameter in missing_parameters:
                    # parameter is not existing at all
                    if bool(missing_parameters[wrongParameter]) == False:
                        notes.append(
                            f"Parameter '{wrongParameter}' of function '{functionname_to_check}' is completly missing.")

                    # parameter existing, but wrong type or default value
                    elif 'type' in missing_parameters[wrongParameter] and 'default' in missing_parameters[
                        wrongParameter]:
                        expected_type = required_args[wrongParameter]['type']
                        is_type = missing_parameters[wrongParameter]['type']
                        expected_default = required_args[wrongParameter]['default']
                        isDefault = missing_parameters[wrongParameter]['default']
                        notes.append(
                            f"Parameter '{wrongParameter}' of function '{functionname_to_check}' has wrong default and type.\n Expected default: '{expected_default}', got '{isDefault}'.\n Expected  type: '{expected_type}', got '{is_type}'")

                    # parameter existing, but wrong type
                    elif 'type' in missing_parameters[wrongParameter]:
                        expected_type = required_args[wrongParameter]['type']
                        is_type = missing_parameters[wrongParameter]['type']
                        notes.append(
                            f"Parameter '{wrongParameter}' of function '{functionname_to_check}' is of wrong type, expected '{expected_type}', got '{is_type}'.")
                    # parameter existing, but wrong default
                    elif 'default' in missing_parameters[wrongParameter]:
                        expected_default = required_args[wrongParameter]['default']
                        isDefault = missing_parameters[wrongParameter]['default']
                        notes.append(
                            f"Parameter '{wrongParameter}' of function '{functionname_to_check}' has wrong default, expected '{expected_default}', got '{isDefault}'.")

            # generate feedback for vararg
            if required_vararg is not None:
                if isinstance(required_vararg, bool):
                    if required_vararg and function_vararg is None:
                        valid = False
                        notes.append(
                            "Your function is missing a parameter to pass a variable number of arguments to the function."
                        )
                    elif required_vararg is False and function_vararg is not None:
                        valid = False
                        notes.append(
                            "Your function has a parameter to pass a variable number of arguments to the function. Here you are not allowed to use this type of parameter."
                        )
                elif isinstance(required_vararg, str):
                    if function_vararg is None:
                        valid = False
                        notes.append(
                            "Your function is missing a parameter to pass a variable number of arguments to the function."
                        )
                    elif function_vararg != required_vararg:
                        valid = False
                        notes.append(
                            "Your function has a parameter to pass a variable number of arguments to the function, but it was named wrong."
                        )

            # generate feedback for kwarg
            if required_kwarg is not None:
                if isinstance(required_kwarg, bool):
                    if required_kwarg and function_kwarg is None:
                        valid = False
                        notes.append(
                            "Your function is missing a parameter to pass a variable number of keyworded arguments to the function."
                        )
                    elif required_kwarg is False and function_kwarg is not None:
                        valid = False
                        notes.append(
                            "Your function has a parameter to pass a variable number of keyworded arguments to the function. Here you are not allowed to use this type of parameter."
                        )
                elif isinstance(required_kwarg, str):
                    if function_kwarg is None:
                        valid = False
                        notes.append(
                            "Your function is missing a parameter to pass a variable number of keyworded arguments to the function."
                        )
                    elif function_kwarg!= required_kwarg:
                        valid = False
                        notes.append(
                            "Your function has a parameter to pass a variable number of keyworded arguments to the function, but it was named wrong."
                        )

            if len(notes) > 0:
                note = "\n".join(notes)
            else:
                note = f"All parameters of function '{functionname_to_check}' are correct."

            return {
                'passed': valid,
                'note': note
            }
        else:
            return self.does_compile()

    def function_uses_module_function(self, functionname_to_check: str, functions_to_use: list, from_module: str):
        """
        Checks if a fuction uses a function from a module and returns dictionary with 'passed', which is a bool and 'note', which is a string

        For example:
        Can find 'arange' and 'reshape' in 'numcheck = np.arange(15, dtype=np.int64).reshape(3, 5)',
        but cannot find 'reshape' in
        '
        numcheck = np.arange(15, dtype=np.int64)
        numcheck.reshape(3, 5)
        '

        Keyword arguments:
        functions_to_use -- list of string of function names to check for
        from_module -- module name the function has to be used from, hast to be the complete name, e.g. numpy instead of np
        """
        if self.compilable:
            module_name = self._get_module_alias(from_module)
            function_visitor = _FunctionVisitor()
            function_visitor.visit(self.source_tree)

            if self.has_function(functionname_to_check=functionname_to_check)['passed'] is False:
                return {
                    'passed': False,
                    'note': f"Function '{functionname_to_check}' not found."
                }

            call_visitor = _CallVisitor()

            valid = {key: False for key in functions_to_use}

            for visited_function in function_visitor.functions:
                if (visited_function.name == functionname_to_check):
                    functions_found = 0
                    call_visitor.visit(visited_function)
                    for function_to_use in functions_to_use:
                        for call in call_visitor.calls:

                            # check for standalone usage
                            if isinstance(call.func, ast.Attribute):
                                if isinstance(call.func.value, ast.Name):
                                    if call.func.value.id == module_name:
                                        if call.func.attr in function_to_use:
                                            valid[function_to_use] = True

                            # check for method chaining
                            if isinstance(call.func, ast.Attribute):
                                if isinstance(call.func.value, ast.Call):
                                    if isinstance(call.func.value.func, ast.Attribute):
                                        if call.func.value.func.value.id == module_name:
                                            if call.func.attr in function_to_use:
                                                valid[function_to_use] = True

                            # check for method was explicitly imported
                            if isinstance(call.func, ast.Name):
                                if (call.func.id == function_to_use) and \
                                        self.module_is_imported_from(function_to_use, from_module)['passed']:
                                    valid[function_to_use] = True
                                    functions_found += 1

                            # check for * import usage
                            if isinstance(call.func, ast.Name):
                                if (call.func.id == function_to_use) and \
                                        self.module_is_imported(from_module)['passed']:
                                    valid[function_to_use] = True
                                    functions_found += 1


            if all(x == True for x in valid.values()) == False:
                unused_functions = [k for k, v in valid.items() if v == False]
                note = f"Function '{functionname_to_check}' does not use {' or '.join(unused_functions)}."
            else:
                note = f"All module functions used in function '{functionname_to_check}'."

            return {
                'passed': all(x == True for x in valid.values()),
                'note': note
            }
        else:
            return self.does_compile()

    def function_uses_functions(self, functionname_to_check: str, functions_to_use: list):
        """
        Checks if a function uses specific functions and returns True if all functions are used or returns dictionary with 'passed', which is a bool and 'note', which is a string

        Keyword arguments:
        functions_to_use -- list of functions to check for, e.g.: ['append', 'type', 'len']
        """
        if self.compilable:
            function_visitor = _FunctionVisitor()
            function_visitor.visit(self.source_tree)

            if self.has_function(functionname_to_check=functionname_to_check)['passed'] is False:
                return {
                    'passed': False,
                    'note': f"Function '{functionname_to_check}' not found."
                }

            valid = False
            for visited_function in function_visitor.functions:
                if (visited_function.name == functionname_to_check):
                    functions_found = 0
                    function_calls = self._get_call_names_in_function(visited_function)
                    for function_to_use in functions_to_use:
                        if function_to_use in function_calls:
                            functions_found += 1

                    if functions_found == len(functions_to_use):
                        valid = True

            if valid == False:
                note = f"Function '{functionname_to_check}' does not use {' or'.join(functions_to_use)}."
            else:
                note = f"All module functions used in function '{functionname_to_check}'."

            return {
                'passed': valid,
                'note': note
            }
        else:
            return self.does_compile()

    def while_used(self):
        """Checks if a while loop has been used, returns dictionary with 'passed', which is a bool and 'note', which is a string"""
        if self.compilable:
            call_visitor = _CallVisitor()
            call_visitor.visit(self.source_tree)
            if len(call_visitor.whiles) != 0:
                uses_while = True
                #T.B.D.: also check for condition
            else:
                uses_while = False

            if uses_while == False:
                note = f"'while loop' was not used at all."

            else:
                note = f"'while loop' was used."

            return {
                'passed': uses_while,
                'note': note
            }

        else:
            return self.does_compile()


    def function_uses_while(self, functionname_to_check: str):
        """Checks if the function uses a while loop, returns dictionary with 'passed', which is a bool and 'note', which is a string"""
        if self.compilable:
            function_visitor = _FunctionVisitor()
            function_visitor.visit(self.source_tree)

            if self.has_function(functionname_to_check=functionname_to_check)['passed'] is False:
                return {
                    'passed': False,
                    'note': f"Function '{functionname_to_check}' not found."
                }

            call_visitor = _CallVisitor()

            uses_while: bool = False
            for visited_function in function_visitor.functions:
                if visited_function.name == functionname_to_check:
                    call_visitor.visit(visited_function)
                    if len(call_visitor.whiles) != 0:
                        uses_while = True
                        # T.B.D.: also check for condition
                    else:
                        uses_while = False

            if uses_while == False:
                note = f"Function '{functionname_to_check}' is not using 'while loop'."
            else:
                note = f"Function '{functionname_to_check}' is using 'while loop'."

            return {
                'passed': uses_while,
                'note': note
            }
        else:
            return self.does_compile()

    def for_used(self, iteration: dict = None, comprehension: bool = False):
        """
        Checks if a for loop with correct iteration, returns dictionary with 'passed', which is a bool and 'note', which is a string

        iteration can be for example:
        {
            'range': (1, 9)
        }
        or:
        {
            'variable': "exampleListToIterateIn"
        }
        """
        if self.compilable:
            call_visitor = _CallVisitor()
            call_visitor.visit(self.source_tree)



            valid = []
            note = []
            note_false = "'for loop' was not used at all."

            # raw for loops
            if len(call_visitor.fors) != 0:
                if iteration is not None:
                    if 'range' in iteration:
                        for for_loop in call_visitor.fors:
                            # T.B.D: Was passiert wenn mehrfach for loops im Studi Code sind?
                            if len(iteration["range"]) == 1:
                                #valid, note = self._has_correct_for_range(for_loop, 0, iteration["range"][1])
                                result = self._has_correct_for_range(for_loop, 0, iteration["range"][0])

                            elif len(iteration["range"]) == 2:
                                #valid, note = self._has_correct_for_range(for_loop, iteration["range"][0], iteration["range"][1])
                                result = self._has_correct_for_range(for_loop, iteration["range"][0], iteration["range"][1])
                            else:
                                #valid, note = self._has_correct_for_range(for_loop, iteration["range"][0], iteration["range"][1], iteration["range"][2])
                                result = self._has_correct_for_range(for_loop, iteration["range"][0], iteration["range"][1], iteration["range"][2])
                            valid.append(result[0])
                            note.append(result[1])
                    if 'variable' in iteration:
                        for for_loop in call_visitor.fors:
                            #valid, note = self._iterates_over_object(for_loop, iteration["variable"])
                            result = self._iterates_over_object(for_loop, iteration["variable"])
                            valid.append(result[0])
                            note.append(result[1])
                else:
                    #valid = True
                    #note = "'for loop' was used."
                    valid.append(True)
                    note.append("'for loop' was used.")
            else:
                valid.append(False)
                note.append(note_false)

            # for loops in comprehensions
            if comprehension and len(call_visitor.comprehensions) != 0:
                if iteration is not None:
                    if 'range' in iteration:
                        for compr in call_visitor.comprehensions:

                            if len(iteration["range"]) == 1:
                                #valid, note = self._has_correct_for_range(compr, 0, iteration["range"][1])
                                #note = note.replace("'for loop' was used", "'for loop' was used in comprehension")
                                result = self._has_correct_for_range(compr, 0, iteration["range"][0])
                                #result[1] = result[1] .replace("'for loop' was used", "'for loop' was used in comprehension")
                            elif len(iteration["range"]) == 2:
                                #valid, note = self._has_correct_for_range(compr, iteration["range"][0], iteration["range"][1])
                                #note = note.replace("'for loop' was used", "'for loop' was used in comprehension")
                                result = self._has_correct_for_range(compr, iteration["range"][0], iteration["range"][1])
                                #result[1] = result[1] .replace("'for loop' was used", "'for loop' was used in comprehension")
                            else:
                                #valid, note = self._has_correct_for_range(compr, iteration["range"][0], iteration["range"][1], iteration["range"][2])
                                #note = note.replace("'for loop' was used", "'for loop' was used in comprehension")
                                result = self._has_correct_for_range(compr, iteration["range"][0], iteration["range"][1], iteration["range"][2])
                                #result[1] = result[1].replace("'for loop' was used", "'for loop' was used in comprehension")
                            valid.append(result[0])
                            note.append(str(result[1]).replace("'for loop' was used", "'for loop' was used in comprehension"))
                    if 'variable' in iteration:
                        for compr in call_visitor.comprehensions:
                            #valid, note = self._iterates_over_object(compr, iteration["variable"])
                            #note = note.replace("'for loop' was used", "'for loop' was used in comprehension")
                            result = self._iterates_over_object(compr, iteration["variable"])
                            #result[1] = result[1].replace("'for loop' was used", "'for loop' was used in comprehension")
                            valid.append(result[0])
                            note.append(str(result[1]).replace("'for loop' was used", "'for loop' was used in comprehension"))
                else:
                    #valid = True
                    #note = "'for loop' was used in comprehension."
                    valid.append(True)
                    note.append("'for loop' was used in comprehension.")

            return {
                'passed': any(valid),
                'note': note[valid.index(True)] if any(valid) else note[0] #note
            }
        else:
            return self.does_compile()

    def function_uses_for(self, functionname_to_check: str, iteration: dict = None, comprehension: bool = False):
        """
        Checks if the function uses a for loop with correct iteration, returns dictionary with 'passed', which is a bool and 'note', which is a string

        iteration can be for example:
        {
            'range': (1, 9)
        }
        or:
        {
            'variable': "exampleListToIterateIn"
        }
        """
        if self.compilable:
            function_visitor = _FunctionVisitor()
            function_visitor.visit(self.source_tree)

            if self.has_function(functionname_to_check=functionname_to_check)['passed'] is False:
                return {
                    'passed': False,
                    'note': f"Function '{functionname_to_check}' not found."
                }

            call_visitor = _CallVisitor()

            valid = False
            note = f"Function '{functionname_to_check}' is not using 'for loop'."
            for visited_function in function_visitor.functions:
                if visited_function.name == functionname_to_check:
                    call_visitor.visit(visited_function)
                    # raw for loops
                    if len(call_visitor.fors) != 0:
                        if iteration is not None:
                            if 'range' in iteration:
                                note = "'for loop' was not used at all."
                                for for_loop in call_visitor.fors:
                                    # T.B.D: Was passiert wenn mehrfach for loops im Studi Code sind?
                                    if len(iteration["range"]) == 1:
                                        valid, note = self._has_correct_for_range(for_loop, 0, iteration["range"][0])
                                    elif len(iteration["range"]) == 2:
                                        valid, note = self._has_correct_for_range(for_loop, iteration["range"][0],
                                                                                  iteration["range"][1])
                                    else:
                                        valid, note = self._has_correct_for_range(for_loop, iteration["range"][0],
                                                                                  iteration["range"][1],
                                                                                  iteration["range"][2])
                            if 'variable' in iteration:
                                for for_loop in call_visitor.fors:
                                    valid, note = self._iterates_over_object(for_loop, iteration["variable"])
                        else:
                            valid = True
                            note = f"Function '{functionname_to_check}' is using 'for loop'."

                    # for loops in comprehensions
                    if comprehension and len(call_visitor.comprehensions) != 0:
                        if iteration is not None:
                            if 'range' in iteration:
                                for compr in call_visitor.comprehensions:
                                    if len(iteration["range"]) == 1:
                                        valid, note = self._has_correct_for_range(compr, 0, iteration["range"][0])
                                        note = note.replace("'for loop' was used", f"Function '{functionname_to_check}' is using 'for loop' in comprehension")
                                    elif len(iteration["range"]) == 2:
                                        valid, note = self._has_correct_for_range(compr, iteration["range"][0], iteration["range"][1])
                                        note = note.replace("'for loop' was used", f"Function '{functionname_to_check}' is using 'for loop' in comprehension")
                                    else:
                                        valid, note = self._has_correct_for_range(compr, iteration["range"][0], iteration["range"][1], iteration["range"][2])
                                        note = note.replace("'for loop' was used", f"Function '{functionname_to_check}' is using 'for loop' in comprehension")
                            if 'variable' in iteration:
                                for compr in call_visitor.comprehensions:
                                    valid, note = self._iterates_over_object(compr, iteration["variable"])
                                    note = note.replace("'for loop' was used", f"Function '{functionname_to_check}' is using 'for loop' in comprehension")
                        else:
                            valid = True
                            note = f"Function '{functionname_to_check}' is using 'for loop' in comprehension."

            return {
                'passed': valid,
                'note': note
            }
        else:
            return self.does_compile()


    def lambda_used(self, variablename_to_check: str = None, number_of_parameters: int = None):
        """Checks if a lambda expression exists, optionally stored in an object, returns dictionary with 'passed', which is a bool and 'note', which is a string"""
        if self.compilable:
            call_visitor = _CallVisitor()
            call_visitor.visit(self.source_tree)

            uses_lambda: bool = False
            note = f"'lambda expression' was not used at all."
            if variablename_to_check is not None:
                if self.has_variable(variablename_to_check)['passed'] is False:
                    return {
                        'passed': False,
                        'note': f"Variable '{variablename_to_check}' not found."
                    }
                note = f"Variable '{variablename_to_check}' exist, but is not a 'lambda expression'."
                for assign in call_visitor.assigns:

                    for target in assign.targets:
                        if isinstance(target, ast.Name):
                            if target.id == variablename_to_check and isinstance(assign.value, ast.Lambda):
                                if number_of_parameters is not None:
                                    note = f"Variable '{variablename_to_check}' is a 'lambda expression', but does not have the correct number of parameters."
                                    function_args, function_vararg, function_kwarg = self._get_lambda_parameters(
                                        assign.value)
                                    if len(function_args) == number_of_parameters:
                                        uses_lambda = True
                                        note = f"Variable '{variablename_to_check}' is a 'lambda expression'."
                                else:
                                    uses_lambda = True
                                    note = f"Variable '{variablename_to_check}' is a 'lambda expression'."
            else:
                if len(call_visitor.lambdas) != 0:
                    uses_lambda = True
                    note = f"'lambda expression' was used."

            return {
                'passed': uses_lambda,
                'note': note
            }
        else:
            return self.does_compile()

    def function_uses_lambda(self, functionname_to_check: str):
        """Checks if the function uses a lambda expression, returns dictionary with 'passed', which is a bool and 'note', which is a string"""
        if self.compilable:
            function_visitor = _FunctionVisitor()
            function_visitor.visit(self.source_tree)

            if self.has_function(functionname_to_check=functionname_to_check)['passed'] is False:
                return {
                    'passed': False,
                    'note': f"Function '{functionname_to_check}' not found."
                }

            call_visitor = _CallVisitor()

            uses_lambda: bool = False
            for visited_function in function_visitor.functions:
                if visited_function.name == functionname_to_check:
                    call_visitor.visit(visited_function)
                    if len(call_visitor.lambdas) != 0:
                        uses_lambda = True
                    else:
                        uses_lambda = False

            if uses_lambda == False:
                note = f"Function '{functionname_to_check}' is not using a 'lambda expression'."
            else:
                note = f"Function '{functionname_to_check}' is using a 'lambda expression'."

            return {
                'passed': uses_lambda,
                'note': note
            }
        else:
            return self.does_compile()

    def list_comprehension_used(self, variablename_to_check: str = None):
        """Checks if a list comprehension exists, optionally stored in an object, returns dictionary with 'passed', which is a bool and 'note', which is a string"""
        if self.compilable:
            call_visitor = _CallVisitor()
            call_visitor.visit(self.source_tree)

            uses_list_comprehension: bool = False
            note = f"'list comprehension' was not used at all."
            if variablename_to_check is not None:
                if self.has_variable(variablename_to_check)['passed'] is False:
                    return {
                        'passed': False,
                        'note': f"Variable '{variablename_to_check}' not found."
                    }
                note = f"Variable '{variablename_to_check}' exist, but is not a 'list comprehension'."

                for assign in call_visitor.assigns:
                    for target in assign.targets:
                        if isinstance(target, ast.Name):
                            if target.id == variablename_to_check and isinstance(assign.value, ast.ListComp):
                                uses_list_comprehension = True
                                note = f"Variable '{variablename_to_check}' is a 'list comprehension'."
            else:
                if len(call_visitor.list_comprehensions) != 0:
                    uses_list_comprehension = True
                    note = f"'list comprehension' was used."

            return {
                'passed': uses_list_comprehension,
                'note': note
            }
        else:
            return self.does_compile()

    def function_uses_list_comprehension(self, functionname_to_check: str):
        """Checks if the function uses list comprehension, returns dictionary with 'passed', which is a bool and 'note', which is a string"""
        if self.compilable:
            function_visitor = _FunctionVisitor()
            function_visitor.visit(self.source_tree)

            if self.has_function(functionname_to_check=functionname_to_check)['passed'] is False:
                return {
                    'passed': False,
                    'note': f"Function '{functionname_to_check}' not found."
                }

            call_visitor = _CallVisitor()

            uses_comprehension: bool = False
            for visited_function in function_visitor.functions:
                if visited_function.name == functionname_to_check:
                    call_visitor.visit(visited_function)
                    if len(call_visitor.list_comprehensions) != 0:
                        uses_comprehension = True
                    else:
                        uses_comprehension = False

            if uses_comprehension == False:
                note = f"{functionname_to_check} is not using a 'list comprehension'."
            else:
                note = f"{functionname_to_check} is using a 'list comprehension'."

            return {
                'passed': uses_comprehension,
                'note': note
            }
        else:
            return self.does_compile()

    def try_except_used(self, error_types: set = None):
        """Checks if a try except block has been used, returns dictionary with 'passed', which is a bool and 'note', which is a string"""
        #T.B.D.: Also check for error_types
        if self.compilable:
            call_visitor = _CallVisitor()
            call_visitor.visit(self.source_tree)

            uses_try_except: bool = False
            note = f"'try except' was not used at all."
            if len(call_visitor.tries) != 0:
                uses_try_except =  True
                note = f"'try except' was used."
            return {
                'passed': uses_try_except,
                'note': note
            }
        else:
            return self.does_compile()

    def function_uses_try_except(self, functionname_to_check: str, error_types: set = None):
        """Checks if the function uses a try except block, returns dictionary with 'passed', which is a bool and 'note', which is a string"""
        # T.B.D.: Also check for error_types
        if self.compilable:
            function_visitor = _FunctionVisitor()
            function_visitor.visit(self.source_tree)

            if self.has_function(functionname_to_check=functionname_to_check)['passed'] is False:
                return {
                    'passed': False,
                    'note': f"Function '{functionname_to_check}' not found."
                }

            call_visitor = _CallVisitor()

            uses_try_except: bool = False
            for visited_function in function_visitor.functions:
                if visited_function.name == functionname_to_check:
                    call_visitor.visit(visited_function)
                    if len(call_visitor.tries) != 0:
                        #for try_except in call_visitor.tries:
                        #    print(try_except.handlers)
                        #    for handler in try_except.handlers:
                        #        #multiple errors caught
                        #        if isinstance(handler.type, ast.Tuple):
                        #            caught_errors = [exc.id for exc in handler.type.elts if isinstance(exc, ast.Name)]
                        #            print("Caufghted Error: " + str(caught_errors))
                        #            #if caught_errors == error_types:
                        #            #    return True
                        #        #one error caught
                        #        elif isinstance(handler.type, ast.Name):# and handler.type.id in error_types:
                        #            print("Caufghted Error: " + str(handler.type.id))
                        #            #return True
                        uses_try_except = True
                    else:
                        uses_try_except = False

            if uses_try_except == False:
                note = f"Function '{functionname_to_check}' is not using 'try/except'."
            else:
                note = f"Function '{functionname_to_check}' is using 'try/except'."

            return {
                'passed': uses_try_except,
                'note': note
            }
        else:
            return self.does_compile()

    def function_is_recursive(self, functionname_to_check: str, allow_indirect: bool = True):
        """Checks if the function is recursive (direct and indirect), returns dictionary with 'passed', which is a bool and 'note', which is a string"""
        if self.compilable:
            function_visitor = _FunctionVisitor()
            function_visitor.visit(self.source_tree)

            if self.has_function(functionname_to_check=functionname_to_check)['passed'] is False:
                return {
                    'passed': False,
                    'note': f"Function '{functionname_to_check}' not found."
                }

            # check for direct recursion
            is_direct_recursive: bool = False
            for visited_function in function_visitor.functions:
                if visited_function.name == functionname_to_check:
                    function_calls = self._get_call_names_in_function(visited_function)
                    if functionname_to_check in function_calls:
                        is_direct_recursive = True

            # check for indirect recursion
            is_indirect_recursive: bool = False
            if not is_direct_recursive:
                call_graph_functions = self._generate_call_graph(function_visitor.functions)
                is_indirect_recursive = self._has_indirect_recursion(call_graph_functions, functionname_to_check)

            valid = False
            if is_direct_recursive == False and is_indirect_recursive == False:
                note = f"Function '{functionname_to_check}' is not recursive."
            elif is_direct_recursive:
                valid = True
                note = f"Function '{functionname_to_check}' is direct recursive."
            elif is_indirect_recursive and allow_indirect == True:
                valid = True
                note = f"Function '{functionname_to_check}' is indirect recursive."
            elif is_indirect_recursive and allow_indirect == False:
                valid = False
                note = f"Function '{functionname_to_check}' is indirect recursive, but you should implement a direct recursion."

            return {
                'passed': valid,
                'note': note
            }
        else:
            return self.does_compile()



    def function_opens_file(self, functionname_to_check: str, filename: str = None, mode: str = None):
        """Checks if the function opens a file using .open, returns dictionary with 'passed', which is a bool and 'note', which is a string"""
        if self.compilable:
            function_visitor = _FunctionVisitor()
            function_visitor.visit(self.source_tree)

            if self.has_function(functionname_to_check=functionname_to_check)['passed'] is False:
                return {
                    'passed': False,
                    'note': f"Function '{functionname_to_check}' not found."
                }

            call_visitor = _CallVisitor()

            found = False
            for visited_function in function_visitor.functions:
                if visited_function.name == functionname_to_check:
                    call_visitor.visit(visited_function)
                    for function_call in call_visitor.calls:
                        if type(function_call.func) == ast.Attribute:
                            call_name = function_call.func.attr
                        else:
                            call_name = function_call.func.id
                        if call_name == 'open':
                            found = True
                            if filename is not None and function_call.args[0].value != filename:
                                found = False
                            if mode is not None and function_call.args[1].value != mode:
                                found = False

            if found == False:
                note = f"{functionname_to_check} is not using 'open'."
            else:
                note = f"{functionname_to_check} is using 'open'."

            return {
                'passed': found,
                'note': note
            }
        else:
            return self.does_compile()

    def function_closes_file(self, functionname_to_check: str):
        """Checks if the function closes a file using .close, returns dictionary with 'passed', which is a bool and 'note', which is a string"""
        if self.compilable:
            function_visitor = _FunctionVisitor()
            function_visitor.visit(self.source_tree)

            if self.has_function(functionname_to_check=functionname_to_check)['passed'] is False:
                return {
                    'passed': False,
                    'note': f"Function '{functionname_to_check}' not found."
                }

            call_visitor = _CallVisitor()

            found = False
            for visited_function in function_visitor.functions:
                if visited_function.name == functionname_to_check:
                    call_visitor.visit(visited_function)
                    for function_call in call_visitor.calls:
                        if type(function_call.func) == ast.Attribute:
                            call_name = function_call.func.attr
                        else:
                            call_name = function_call.func.id
                        if call_name == 'close':
                            found = True

            if found == False:
                note = f"{functionname_to_check} is not using 'close'."
            else:
                note = f"{functionname_to_check} is using 'close'."

            return {
                'passed': found,
                'note': note
            }
        else:
            return self.does_compile()

    def function_uses_with(self, functionname_to_check: str):
        """Checks if the function uses a context manager, returns dictionary with 'passed', which is a bool and 'note', which is a string"""
        if self.compilable:
            function_visitor = _FunctionVisitor()
            function_visitor.visit(self.source_tree)

            if self.has_function(functionname_to_check=functionname_to_check)['passed'] is False:
                return {
                    'passed': False,
                    'note': f"Function '{functionname_to_check}' not found"
                }

            call_visitor = _CallVisitor()

            uses_with: bool = False
            for visited_function in function_visitor.functions:
                if visited_function.name == functionname_to_check:
                    call_visitor.visit(visited_function)
                    if len(call_visitor.withs) != 0:
                        uses_with = True

            if uses_with == False:
                note = f"{functionname_to_check} is not using 'with'."
            else:
                note = f"{functionname_to_check} is using 'with'."

            return {
                'passed': uses_with,
                'note': note
            }
        else:
            return self.does_compile()

    def module_is_imported(self, modulename_to_check: str):
        """Checks if a module is imported, returns dictionary with 'passed', which is a bool and 'note', which is a string"""
        if self.compilable:
            definition_visitor = _DefinitionVisitor()
            definition_visitor.visit(self.source_tree)

            is_imported = False
            #check for ast.Import
            for visited_imports in definition_visitor.imports:
                for import_names in visited_imports.names:
                    if import_names.name == modulename_to_check:
                        is_imported = True

            #check for ast.ImportFrom
            if not is_imported:
                for visited_importsFrom in definition_visitor.importsFrom:
                    if visited_importsFrom.module == modulename_to_check:
                        is_imported = True

            if is_imported == False:
                note = f"Module '{modulename_to_check}' is not imported."
            else:
                note = f"Module '{modulename_to_check}' is imported."

            return {
                'passed': is_imported,
                'note': note
            }
        else:
            return self.does_compile()

    def module_is_imported_from(self, functionname_to_check: str, imported_from: str):
        """Checks if a function is imported from a module, returns dictionary with 'passed', which is a bool and 'note', which is a string"""
        if self.compilable:
            definition_visitor = _DefinitionVisitor()
            definition_visitor.visit(self.source_tree)

            is_imported = False
            for visited_importsFrom in definition_visitor.importsFrom:
                if visited_importsFrom.module != imported_from:
                    continue
                for importFrom_names in visited_importsFrom.names:
                    if importFrom_names.name == functionname_to_check:
                        is_imported = True

            if is_imported == False:
                note = f"Function '{functionname_to_check}' is not imported from module '{imported_from}'."
            else:
                note = f"Function '{functionname_to_check}' is imported from module '{imported_from}'."

            return {
                'passed': is_imported,
                'note': note
            }
        else:
            return self.does_compile()

    def _get_call_names_in_function(self, function_definitions: ast.FunctionDef):
        """Helper function to get all calls in a function, returns a list of strings of the function calls used in the function"""
        function_calls = []

        call_visitor = _CallVisitor()
        call_visitor.visit(function_definitions)

        for call in call_visitor.calls:
            # function
            if type(call.func) == ast.Attribute:
                function_calls.append(call.func.attr)
            # method
            else:
                function_calls.append(call.func.id)

        return function_calls

    def _get_function_node_by_function_name(self, function_definitions: list[ast.FunctionDef], function_name: str):
        """Helper function to get node of a function by its name"""
        for elem in function_definitions:
            if elem.name == function_name:
                return elem

    def _get_function_parameters(self, function_definitions: ast.FunctionDef):
        """Helper function to get all parameters of a function, returns a dict of the parameters with their type and default value, if exists"""
        args = {}
        vararg = None
        kwarg = None

        # get args
        for arguments in function_definitions.args.args:
            parameter_type = None
            if arguments.annotation is not None:
                if isinstance(arguments.annotation, ast.Name):
                    parameter_type = eval(arguments.annotation.id)
            args[arguments.arg] = {
                'type': parameter_type,
                'default': None
            }

        i = -1
        for default in reversed(function_definitions.args.defaults):
            if isinstance(default, ast.Constant):
                args[list(args)[i]]['default'] = default.value
            elif isinstance(default, ast.Name):
                args[list(args)[i]]['default'] = default.id
            i = i - 1

        # get varagrs
        if isinstance(function_definitions.args.vararg, ast.arg):
            vararg = function_definitions.args.vararg.arg

        # get kwarg
        if isinstance(function_definitions.args.kwarg, ast.arg):
            kwarg = function_definitions.args.kwarg.arg

        return args, vararg, kwarg

    def _get_lambda_parameters(self, lambda_definition: ast.Lambda):
        """Helper function to get all parameters of a function, returns a dict of the parameters with their type and default value, if exists"""
        args = {}
        vararg = None
        kwarg = None

        # get args
        for arguments in lambda_definition.args.args:
            parameter_type = None
            if arguments.annotation is not None:
                parameter_type = arguments.annotation.id
            args[arguments.arg] = {
                'type': parameter_type,
                'default': None
            }

        i = -1
        for default in reversed(lambda_definition.args.defaults):
            if isinstance(default, ast.Constant):
                args[list(args)[i]]['default'] = default.value
            elif isinstance(default, ast.Name):
                args[list(args)[i]]['default'] = default.id
            i = i - 1

        # get varagrs
        if isinstance(lambda_definition.args.vararg, ast.arg):
            vararg = lambda_definition.args.vararg.arg

        # get kwarg
        if isinstance(lambda_definition.args.kwarg, ast.arg):
            kwarg = lambda_definition.args.kwarg.arg

        return args, vararg, kwarg

    def _get_class_parameters(self, class_definition: ast.ClassDef):
        args = {}
        vararg = None
        kwarg = None

        function_visitor = _FunctionVisitor()
        function_visitor.visit(class_definition)

        for visited_function in function_visitor.functions:
            if visited_function.name == "__init__":
                # get args
                for arguments in visited_function.args.args:
                    parameter_type = None
                    if arguments.annotation is not None:
                        parameter_type = arguments.annotation.id
                    args[arguments.arg] = {
                        'type': parameter_type,
                        'default': None
                    }

                i = -1
                for default in reversed(visited_function.args.defaults):
                    if isinstance(default, ast.Constant):
                        args[list(args)[i]]['default'] = default.value
                    elif isinstance(default, ast.Name):
                        args[list(args)[i]]['default'] = default.id
                    i = i - 1

                # get varagrs
                if isinstance(visited_function.args.vararg, ast.arg):
                    vararg = visited_function.args.vararg.arg

                # get kwarg
                if isinstance(visited_function.args.kwarg, ast.arg):
                    kwarg = visited_function.args.kwarg.arg

        return args, vararg, kwarg

    def _get_module_alias(self, module_name: str):
        """Helper function to get the alias name of an imported module, returns the alias name as a string"""
        definition_visitor = _DefinitionVisitor()
        definition_visitor.visit(self.source_tree)

        for visited_imports in definition_visitor.imports:
            for import_names in visited_imports.names:
                if import_names.name == module_name:
                    if import_names.asname is not None:
                        return import_names.asname
                    return import_names.name
        return False

    def _has_correct_for_range(self, ast_for, start, stop, step=1):
        note = f"'for loop' was used, but without range()."
        ranges_valid = [False, False, False]

        if isinstance(ast_for.iter, ast.Call) and isinstance(ast_for.iter.func, ast.Name) and \
                ast_for.iter.func.id == "range" and len(ast_for.iter.args) >= 1 and len(ast_for.iter.args) <= 3:
            range_args = [arg.n for arg in ast_for.iter.args]

            if len(range_args) == 1:
                range_start, range_stop, range_step = 0, range_args[0], 1
            elif len(range_args) == 2:
                range_start, range_stop, range_step = range_args[0], range_args[1], 1
            else:
                range_start, range_stop, range_step = range_args

            if range_start == start:
                ranges_valid[0] = True
            if range_stop == stop:
                ranges_valid[1] = True
            if range_step == step:
                ranges_valid[2] = True
            if not all(ranges_valid):
                note = f"'for loop' was used, but some ranges are not correct:"
                note_help = ["start", "stop", "step"]
                note_solutions = [start, stop, step]
                note_students = [range_start, range_stop, range_step]
                for i, elem in enumerate(ranges_valid):
                    if not elem:
                        note += f"\n{note_help[i]} should be {note_solutions[i]} and not {note_students[i]}"

        return all(ranges_valid), note

    def _iterates_over_object(self, ast_for, variable):
        note = f"'for loop' was used, but it did not iterate over the correct object."
        valid = False
        # iterates directly over the object
        if isinstance(ast_for.iter, ast.Name):
            if ast_for.iter.id == variable:
                valid = True
                note = f"'for loop' was used on object {variable}."
        # iterates over a method call on the object
        elif isinstance(ast_for.iter, ast.Call) and isinstance(ast_for.iter.func, ast.Attribute) and isinstance(ast_for.iter.func.value, ast.Name):
            if ast_for.iter.func.value.id == variable:
                valid = True
                note = f"'for loop' was used on object {variable}."


        return valid, note

    def _has_indirect_recursion(self, call_graph, target_function, visited=None):
        if visited is None:
            visited = set()
        if target_function in visited:
            return True
        visited.add(target_function)
        if target_function in call_graph:
            for callee in call_graph[target_function]:
                if self._has_indirect_recursion(call_graph, callee, visited.copy()):
                    return True
        return False

    def _generate_call_graph(self, function_definitions: list[ast.FunctionDef]):
        call_graph_functions = {}
        for visited_function in function_definitions:
            call_graph_functions[visited_function.name] = set(self._get_call_names_in_function(visited_function))
        return call_graph_functions

class _LastAssignmentVisitor(ast.NodeVisitor):
    def __init__(self, target_object):
        self.target_object = target_object
        self.last_assignment = None

    def visit_Assign(self, node):
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id == self.target_object:
                self.last_assignment = node.value

    def node_equal(self, node1, node2):
        return ast.dump(node1) == ast.dump(node2)


class _DefinitionVisitor(ast.NodeVisitor):
    def __init__(self):
        self.classes: list[ast.ClassDef] = []
        self.imports: list[ast.Import] = []
        self.importsFrom: list[ast.ImportFrom] = []

    def visit_ClassDef(self, node: ast.ClassDef):
        self.classes.append(node)

    def visit_Import(self, node: ast.Import):
        self.imports.append(node)

    def visit_ImportFrom(self, node: ast.ImportFrom):
        self.importsFrom.append(node)


class _FunctionVisitor(ast.NodeVisitor):
    def __init__(self):
        self.functions: list[ast.FunctionDef] = []

    def visit_FunctionDef(self, node: ast.FunctionDef):
        self.functions.append(node)


class _CallVisitor(ast.NodeVisitor):
    def __init__(self):
        self.calls: list[ast.Call] = []
        self.whiles: list[ast.While] = []
        self.fors: list[ast.For] = []
        self.lambdas: list[ast.Lambda] = []
        self.ifs: list[ast.If] = []
        self.comprehensions: list[ast.comprehension] = []
        self.list_comprehensions: list(ast.ListComp) = []
        self.set_comprehensions: list(ast.SetComp) = []
        self.dict_comprehensions: list(ast.DictComp) = []
        self.assigns: list[ast.Assign] = []
        self.tries: list[ast.Try] = []
        self.withs: list[ast.With] = []
        self.expr: list[ast.Expr] = []

    def visit_Call(self, node: ast.Call):
        self.calls.append(node)
        self.generic_visit(node)

    def visit_While(self, node: ast.While):
        self.whiles.append(node)
        self.generic_visit(node)

    def visit_For(self, node: ast.For):
        self.fors.append(node)
        self.generic_visit(node)

    def visit_Lambda(self, node: ast.Lambda):
        self.lambdas.append(node)
        self.generic_visit(node)

    def visit_If(self, node: ast.If):
        self.ifs.append(node)
        self.generic_visit(node)

    def visit_comprehension(self, node: ast.comprehension):
        self.comprehensions.append(node)
        self.generic_visit(node)

    def visit_ListComp(self, node: ast.ListComp):
        self.list_comprehensions.append(node)
        self.generic_visit(node)

    def visit_SetComp(self, node: ast.SetComp):
        self.set_comprehensions.append(node)
        self.generic_visit(node)

    def visit_DictComp(self, node: ast.DictComp):
        self.dict_comprehensions.append(node)
        self.generic_visit(node)

    def visit_Assign(self, node: ast.Assign):
        self.assigns.append(node)
        self.generic_visit(node)

    def visit_Try(self, node: ast.Try):
        self.tries.append(node)
        self.generic_visit(node)

    def visit_With(self, node: ast.With):
        self.withs.append(node)
        self.generic_visit(node)

    def visit_Expr(self, node: ast.Expr):
        self.expr.append(node)
        self.generic_visit(node)