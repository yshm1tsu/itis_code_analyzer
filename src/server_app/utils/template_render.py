from typing import List

import jinja2
from jinja2 import FileSystemLoader


def render_template(configuration: List, student_directory_name: str):
    import_names = [object["CheckName"] for object in configuration]
    functions = {}
    for object in configuration:
        function_name = object["CheckName"]
        parameters = (
            "".join(f"{param}," for param in object["CheckAttributes"]).rstrip(",")
            if object["CheckAttributes"] != ["*=*"]
            else ""
        )
        functions[function_name] = parameters
    environment = jinja2.Environment(loader=FileSystemLoader("templates/"))
    template = environment.get_template("executable.j2")
    functions = functions
    content = template.render(
        files=["a.py", "b.py"],
        import_names=import_names,
        functions=functions,
        student_directory_name=student_directory_name,
    )
    with open("executable.py", mode="w") as message:
        message.write(content)
