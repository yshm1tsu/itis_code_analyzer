from utils.analyzer.analyzer_utils import check_lists_max_length
from utils.analyzer.analyzer_utils import check_specific_loop_used
from utils.analyzer.analyzer_utils import check_class_methods_count

from utils.ast_utils.tree_utils import get_objects

results = {}


def process_file(results, content, filename):
    results[filename] = ""
    objects = get_objects(content)
    result = check_lists_max_length(objects, length=3)
    if result:
        results[filename] += f"{result}\n"
    result = check_specific_loop_used(objects, loop_type="for")
    if result:
        results[filename] += f"{result}\n"
    result = check_class_methods_count(objects, count=3)
    if result:
        results[filename] += f"{result}\n"
