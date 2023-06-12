import ast


def get_objects(file) -> dict:
    objects = {
        "function_definitions": [],
        "classes": [],
        "constants": [],
        "formatted_values": [],
        "joined_strings": [],
        "lists": [],
        "tuples": [],
        "sets": [],
        "dicts": [],
        "variables_assignment": [],
        "expressions": [],
        "subscriptions": [],
        "slices": [],
        "imports": [],
        "control_flow": [],
        "calls": [],
        "comprehensions": [],
    }
    parsed_ast = ast.parse(file)
    for node in ast.walk(parsed_ast):
        if isinstance(
            node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda, ast.Return)
        ):
            objects["function_definitions"].append(node)
        elif isinstance(node, ast.ClassDef):
            objects["classes"].append(node)
        elif isinstance(node, ast.Constant):
            objects["constants"].append(node)
        elif isinstance(node, ast.FormattedValue):
            objects["formatted_values"].append(node)
        elif isinstance(node, ast.JoinedStr):
            objects["joined_strings"].append(node)
        elif isinstance(node, ast.List):
            objects["lists"].append(node)
        elif isinstance(node, ast.Tuple):
            objects["tuples"].append(node)
        elif isinstance(node, ast.Set):
            objects["sets"].append(node)
        elif isinstance(node, ast.Dict):
            objects["dicts"].append(node)
        elif isinstance(node, (ast.Assign, ast.AnnAssign, ast.AugAssign)):
            objects["variables_assignment"].append(node)
        elif isinstance(node, (ast.Expr, ast.NamedExpr, ast.Expression)):
            objects["expressions"].append(node)
        elif isinstance(node, ast.Subscript):
            objects["subscriptions"].append(node)
        elif isinstance(node, ast.Slice):
            objects["slices"].append(node)
        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            objects["imports"].append(node)
        elif isinstance(
            node,
            (
                ast.If,
                ast.For,
                ast.While,
                ast.Or,
                ast.Break,
                ast.Continue,
                ast.Try,
                ast.ExceptHandler,
                ast.With,
            ),
        ):
            objects["control_flow"].append(node)
        elif isinstance(node, ast.Call):
            objects["calls"].append(node)
        elif isinstance(node, (ast.DictComp, ast.ListComp, ast.SetComp)):
            objects["comprehensions"].append(node)
    return objects
