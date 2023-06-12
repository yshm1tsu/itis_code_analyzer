import ast


def check_attributes_assignment_inside_init(objects: dict, restriction_type=0):
    classes = objects["classes"]
    classes_bodies = [class_object.body for class_object in classes]
    class_methods = [
        value
        for method in classes_bodies
        for value in method
        if isinstance(value, (ast.FunctionDef, ast.AsyncFunctionDef))
    ]
    init_methods = [value for value in class_methods if value.name == "__init__"]
    for init_method in init_methods:
        init_method_body = init_method.body
        object_types = [type(obj) for obj in init_method_body]
        if ast.Assign not in object_types and restriction_type == 1:
            return "Атрибуты не объявляются внутри __init__"
        if ast.Assign not in object_types and restriction_type == 0:
            return "Атрибуты не объявляются внутри __init__"


def check_inheritance_usage(objects: dict, restriction_type=0):
    classes = objects["classes"]
    violating_lines = []
    classes_bases = [{class_object: class_object.bases} for class_object in classes]
    classes_keywords = [
        {class_object: class_object.keywords} for class_object in classes
    ]
    for class_bases in classes_bases:
        for key in class_bases.keys():
            if len(class_bases[key]) == 0:
                violating_lines.append(key.lineno)
    for class_keywords in classes_keywords:
        for key in class_keywords.keys():
            keyword_types = [type(obj.value) for obj in class_keywords[key]]
            if ast.Name not in keyword_types:
                violating_lines.append(key.lineno)
    if len(violating_lines) != 0 and restriction_type == 1:
        return f"Классы на строках {set(violating_lines)} не используют наследование"
    if len(violating_lines) != 0 and restriction_type == 0:
        return f"Классы на строках {set(violating_lines)} используют наследование. Это запрещено"


def check_class_methods_count(objects: dict, count: int, restriction_type=0):
    classes = objects["classes"]
    violating_lanes = []
    classes_bodies = [{class_object: class_object.body} for class_object in classes]
    for class_body in classes_bodies:
        for key in class_body.keys():
            methods = [
                method
                for method in class_body[key]
                if isinstance(method, (ast.FunctionDef, ast.AsyncFunctionDef))
            ]
            if len(methods) < count:
                violating_lanes.append(key.lineno)
    if len(violating_lanes) != 0 and restriction_type == 1:
        return f"Недостаточное количество методов классов у классов на строках {violating_lanes}"
    if len(violating_lanes) != 0 and restriction_type == 0:
        return f"Избыточное количество методов классов у классов на строках {violating_lanes}"


def check_lists_max_length(objects: dict, length: int, restriction_type=0):
    lists = objects["lists"]
    violating_lanes = []
    for list in lists:
        if len(list.elts) > length:
            violating_lanes.append(list.lineno)
    if violating_lanes and restriction_type == 0:
        return f"Длина массивов на строках {violating_lanes} превышает максимальную"
    if violating_lanes and restriction_type == 1:
        return (
            f"Длина массивов на строках {violating_lanes} должна быть минимум {length}"
        )


def check_list_comprehension_usage(objects: dict, restriction_type=0):
    list_comprehensions = [
        value
        for value in objects["variables_assignment"]
        if isinstance(value.value, ast.ListComp)
    ]
    if len(list_comprehensions) == 0 and restriction_type == 1:
        return "List comprehensions не используется"
    if len(list_comprehensions) == 0 and restriction_type == 0:
        return "Использование List comprehensions запрещено"


def check_keys_same_type(objects: dict, restriction_type=0):
    dicts = objects["dicts"]
    violating_lanes = []
    keys = [{dict_object: dict_object.keys} for dict_object in dicts]
    for item in keys:
        for key in item.keys():
            print(item[key])
            key_types = {type(v.value) for v in item[key]}
            if len(key_types) != 1:
                violating_lanes.append(key.lineno)
    if len(violating_lanes) != 0 and restriction_type == 1:
        return f"Ключи словарей на строках {violating_lanes} разных типов"
    if len(violating_lanes) != 0 and restriction_type == 0:
        return (
            f"Ключи словарей на строках {violating_lanes} должны быть одинаковых типов"
        )


def check_values_same_type(objects: dict, restriction_type=0):
    dicts = objects["dicts"]
    violating_lanes = []
    keys = [{dict_object: dict_object.values} for dict_object in dicts]
    for item in keys:
        for key in item.keys():
            print(item[key])
            values_types = {type(v.value) for v in item[key]}
            if len(values_types) != 1:
                violating_lanes.append(key.lineno)
    if len(violating_lanes) != 0 and restriction_type == 1:
        return f"Значения в словарях на строках {violating_lanes} разных типов"
    if len(violating_lanes) != 0 and restriction_type == 0:
        return f"Значения в словарях на строках {violating_lanes} должны быть одинаковых типов"


def check_keys_specific_type(objects: dict, key_type: type, restriction_type=0):
    dicts = objects["dicts"]
    violating_lanes = []
    keys = [{dict_object: dict_object.keys} for dict_object in dicts]
    for item in keys:
        for key in item.keys():
            print(item[key])
            key_types = {type(v.value) for v in item[key]}
            if (
                len(key_types) == 1
                and list(key_types)[0] != key_type
                or len(key_types) != 1
            ):
                violating_lanes.append(key.lineno)

    if len(violating_lanes) != 0 and restriction_type == 1:
        return f"Ключи в словарях на строках {violating_lanes} не типа {key_type}"
    if len(violating_lanes) != 0 and restriction_type == 0:
        return f"Ключи в словарях на строках {violating_lanes} не могут быть типа {key_type}"


def check_values_specific_type(objects: dict, key_type: type, restriction_type=0):
    dicts = objects["dicts"]
    violating_lanes = []
    keys = [{dict_object: dict_object.values} for dict_object in dicts]
    for item in keys:
        for key in item.keys():
            values_types = {type(v.value) for v in item[key]}
            if (
                len(values_types) == 1
                and list(values_types)[0] != key_type
                or len(values_types) != 1
            ):
                violating_lanes.append(key.lineno)

    if len(violating_lanes) != 0 and restriction_type == 1:
        return f"Значения в словарях на строках {violating_lanes} не типа {key_type}"
    if len(violating_lanes) != 0 and restriction_type == 0:
        return f"Значения в словарях на строках {violating_lanes} не могут быть типа {key_type}"


def check_specific_method_usage(objects: dict, method, restriction_type=0):
    assignments = objects["variables_assignment"]
    calls = objects["calls"]
    dictionary_assignments_ids = [
        object.targets[0].id for object in assignments if type(object.value) is ast.Dict
    ]
    dictionary_function_calls = [
        object.func.attr
        for object in calls
        if type(object.func) == ast.Attribute
        and type(object.func.value) == ast.Name
        and object.func.value.id in dictionary_assignments_ids
    ]
    if restriction_type == 1 and method not in dictionary_function_calls:
        return f"Метод {method} для словарей не используется"
    if restriction_type == 0 and method in dictionary_function_calls:
        return f"Метод {method} для словарей запрещен к использованию"


def check_dict_comprehension_usage(objects: dict, restriction_type=0):
    comprehensions = objects["comprehensions"]
    dict_comprehensions = [
        object for object in comprehensions if type(object) == ast.DictComp
    ]
    if len(dict_comprehensions) == 0 and restriction_type == 1:
        return "Не используются dict comprehensions"
    if len(dict_comprehensions) == 0 and restriction_type == 0:
        return "Использование dict comprehensions запрещено"


def check_import_usage(
    objects: dict,
    restriction_type=0,
    import_value: str = None,
    import_from_value: str = None,
):
    imports = objects["imports"]
    violating_lanes = []
    if import_value:
        for import_object in imports:
            if type(import_object) == ast.Import:
                names = {object.name for object in import_object.names}
                if import_value in names:
                    violating_lanes.append(import_object.lineno)
            if type(import_object) == ast.ImportFrom:
                name = import_object.module
                if name == import_value:
                    violating_lanes.append(import_object.lineno)
    if import_from_value:
        imports_from = [object for object in imports if type(object) == ast.ImportFrom]
        for import_from in imports_from:
            imported_modules = {object.name for object in import_from.names}
            if import_from_value in imported_modules:
                violating_lanes.append(import_from.lineno)
    if len(violating_lanes) != 0 and restriction_type == 1 and import_value:
        return f"Библиотека {import_value} не используется"
    if len(violating_lanes) != 0 and restriction_type == 0 and import_value:
        return f"Библиотека {import_value} запрещена"
    if len(violating_lanes) != 0 and restriction_type == 1 and import_value:
        return f"Библиотека {import_from_value} не используется"
    if len(violating_lanes) != 0 and restriction_type == 0 and import_value:
        return f"Библиотека {import_from_value} запрещена"


def check_named_attributes(objects: dict, in_each: bool, restriction_type=0):
    functions = objects["function_definitions"]
    violating_lanes = []
    for func in functions:
        args = func.args
        kwonlyargs = args.kwonlyargs + args.kw_defaults
        if in_each:
            if len(kwonlyargs) == 0:
                violating_lanes.append(func.lineno)
        else:
            if len(kwonlyargs) == 0:
                if restriction_type == 1:
                    return "Не используются именованные параметры"
                if restriction_type == 0:
                    return "Использование именованных парметров запрещено"
        if in_each and len(violating_lanes) != 0:
            if restriction_type == 1:
                return f"Функции на строках {violating_lanes} не используют именованные параметры"
            if restriction_type == 0:
                return f"Функции на строках {violating_lanes} используют именованные параметры. Это запрещено"


def check_default_attributes_used(objects: dict, in_each: bool, restriction_type=0):
    functions = objects["function_definitions"]
    violating_lanes = []
    for func in functions:
        print(ast.dump(func))
        args = func.args
        defaults = args.kw_defaults + args.defaults
        if in_each:
            if len(defaults) == 0:
                violating_lanes.append(func.lineno)
        else:
            if len(defaults) == 0:
                if restriction_type == 1:
                    return "Функции не используют параметры по умолчанию"
            if len(defaults) != 0:
                if restriction_type == 0:
                    return "Функции используют параметры по умолчанию. Это запрещено"
    if in_each and len(violating_lanes) != 0:
        if restriction_type == 1:
            return f"Функции на строках {violating_lanes} не используют параметры по умолчанию"


def check_kwargs_used(objects: dict, in_each: bool, restriction_type=0):
    functions = objects["function_definitions"]
    violating_lanes = []
    if in_each:
        for func in functions:
            args = func.args
            kwargs = args.kwarg
            if not kwargs:
                violating_lanes.append(func.lineno)

    else:
        kwargs = [function.args.kwarg for function in functions if function.args.kwarg]
        print(kwargs)
        if len(kwargs) == 0:
            return "kwargs не используются"
    if in_each and len(violating_lanes) != 0:
        return f"Функции на строках {violating_lanes} не используют kwargs"


def check_varargs_used(objects: dict, in_each: bool, restriction_type=0):
    functions = objects["function_definitions"]
    violating_lanes = []
    if in_each:
        for func in functions:
            args = func.args
            varargs = args.vararg
            if not varargs:
                violating_lanes.append(func.lineno)

    else:
        varargs = [
            function.args.vararg for function in functions if function.args.vararg
        ]
        print(varargs)
        if len(varargs) == 0:
            print("varargs не используются")
    if in_each and len(violating_lanes) != 0:
        return f"Функции на строках {violating_lanes} не используют kwargs"


def check_return_used(objects, restriction_type=0, in_each=False):
    functions = objects["function_definitions"]
    counter = 0
    for function in functions:
        if any(isinstance(node, ast.Return) for node in ast.walk(function)):
            counter += 1
    if len(functions) > 0:
        if in_each and counter != len(functions):
            return "Не все функции используют return"
        if not in_each and counter == 0:
            return "return должен использоваться хотя бы в одной функции"


def check_decorator_used(objects, restriction_type=0, times_used=None):
    functions = objects["function_definitions"]
    counter = 0
    for function in functions:
        if "decorator_list" in function._fields:
            if len(function.decorator_list) > 0:
                counter += 1
    if times_used and counter < times_used or not times_used and counter == 0:
        return "Нет необходимого числа декораторов функций"


def check_specific_loop_used(objects, loop_type, restriction_type=0):
    control_flow = objects["control_flow"]
    if loop_type == "for":
        loop = ast.For
        anti_loop = ast.While
    if loop_type == "while":
        loop = ast.While
        anti_loop = ast.For
    anti_loops = list(filter(lambda node: type(anti_loop) == loop, control_flow))
    if len(anti_loops) > 0:
        return "Используется неподходящий цикл"


def check_nested_loops(objects, pattern, restriction_type=0):
    elements_dict = {
        ast.While: "while",
        ast.For: "for",
    }
    counter = 0
    control_flow = objects["control_flow"]
    flow_pattern = pattern.split("->")
    loops = list(filter(lambda node: type(node) in [ast.For, ast.While], control_flow))
    for loop in loops:
        inside_loops = list(
            filter(lambda node: type(node) in [ast.For, ast.While], ast.walk(loop))
        )
        flow = list(map(lambda node: elements_dict[type(node)], inside_loops))
        if flow == flow_pattern:
            counter += 1
    if counter == 0 and restriction_type == 0:
        return f"Не используется цикл с паттерном {pattern}"


def check_break_used(objects, restriction_type=0):
    control_flow = objects["control_flow"]
    breaks = list(filter(lambda node: type(node) == ast.Break, control_flow))
    if len(breaks) == 0 and restriction_type == 1:
        return "Не используется оператор break"
    if len(breaks) != 0 and restriction_type == 0:
        return "Использование оператора break запрещено"


def check_continue_used(objects, restriction_type=0):
    control_flow = objects["control_flow"]
    continues = list(filter(lambda node: type(node) == ast.Continue, control_flow))
    if len(continues) == 0 and restriction_type == 1:
        return "Не используется оператор continue"
    if len(continues) != 0 and restriction_type == 0:
        return "Использование оператора continue запрещено"


def check_try_used(objects, restriction_type=0):
    control_flow = objects["control_flow"]
    tries = list(filter(lambda node: type(node) == ast.Try, control_flow))
    if len(tries) == 0 and restriction_type == 1:
        return "Не используется оператор try"
    if len(tries) != 0 and restriction_type == 0:
        return "Использование оператора try запрещено"


def check_or_used(objects, restriction_type=0):
    control_flow = objects["control_flow"]
    ors = list(filter(lambda node: type(node) == ast.Or, control_flow))
    if len(ors) == 0 and restriction_type == 1:
        return "Не используется оператор or"
    if len(ors) != 0 and restriction_type == 0:
        return "Использование оператора or запрещено"


def check_context_manager_used(objects, restriction_type=0):
    control_flow = objects["control_flow"]
    withs = list(filter(lambda node: type(node) == ast.With, control_flow))
    if len(withs) == 0 and restriction_type == 1:
        return "Не используется оператор with"
    if len(withs) != 0 and restriction_type == 0:
        return "Использование оператора with запрещено"
