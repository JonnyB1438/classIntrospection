import importlib
import importlib.util
import inspect
from .settings import classes_dict, menu_dict


def get_parent_classes(class_name, class_list=None):
    """Return recursive list of class parents"""
    if inspect.stack()[1][3] != inspect.stack()[0][3]:
        class_list = [{'class': class_name, 'name': class_name.__name__}]
    for parent_class in class_name.__bases__:
        if parent_class is not object:
            if class_list[0]['class'] == class_name:
                class_list.append({'class': parent_class, 'name': parent_class.__name__, 'main_parent': True})
            else:
                class_list.append({'class': parent_class, 'name': parent_class.__name__, 'main_parent': False})
            get_parent_classes(parent_class, class_list)
    if inspect.stack()[1][3] != inspect.stack()[0][3]:
        return class_list


def get_fields(class_names):
    """Return class fields with values and owners as a list of dicts"""
    fields = [{'name': f,
               'value': getattr(class_name['class'], f),
               'owner': class_name,
               'redefined': False}
              for class_name in class_names
              for f in class_name['class'].__dict__
              if (not callable(getattr(class_name['class'], f)) or inspect.isclass(getattr(class_name['class'], f)))
              and not f.startswith('__')]
    for index in range(len(fields)):
        if type(fields[index]['value']) == str:
            fields[index]['value'] = "'" + fields[index]['value'] + "'"
        elif type(fields[index]['value']) == type:
            fields[index]['value'] = str(fields[index]['value'])
    for index in range(len(fields) - 1):
        for sub_index in range(index+1, len(fields)):
            if fields[index]['name'] == fields[sub_index]['name']:
                fields[index]['redefined'] = True
                break
    return fields


def get_best_import_path_for_class(class_name: type) -> str:
    """Return the best module path for a class importing"""
    module_path = best_path = class_name.__module__
    while module_path := module_path.rpartition(".")[0]:
        try:
            module = importlib.import_module(module_path)
            if getattr(module, class_name.__name__, None) == class_name:
                best_path = module_path
        except Exception:
            print(Exception)
            return class_name.__module__
    return best_path


def get_methods(class_names):
    """Return all class methods with code of all parents"""
    result = {}
    for class_name in class_names:
        for f in class_name['class'].__dict__:
            if (inspect.isfunction(getattr(class_name['class'], f)) or inspect.ismethod(getattr(class_name['class'], f))) \
                    and not f.startswith('__'):
                if f not in result:
                    result[f] = {}
                result[f]['name'] = f
                result[f]['function'] = getattr(class_name['class'], f),
                result[f]['signature'] = str(inspect.signature(getattr(class_name['class'], f)))
                result[f]['owner'] = class_name
                if 'code' not in result[f]:
                    result[f]['code'] = []
                lines, lnum = inspect.getsourcelines(getattr(class_name['class'], f))
                first_alfa = len(lines[0]) - len(lines[0].lstrip())
                if first_alfa:
                    lines = [line[first_alfa:] for line in lines if not line[:first_alfa].strip()]
                result[f]['code'].insert(0, {'owner': class_name['class'].__name__, 'code': ''.join(lines), 'lnum': lnum})
                result[f]['docstring'] = inspect.getdoc(getattr(class_name['class'], f))
    return [method for method in result.values()]


def get_class_data(name: str) -> dict:
    """
    A function returning a class structure by the name
    :param name: a name of the class
    :return: the class structure
    """
    if name not in classes_dict:
        return {}
    class_name = classes_dict[name]
    class_data = dict()
    class_data['docstring'] = inspect.getdoc(class_name)
    class_data['parents'] = get_parent_classes(class_name)
    class_data['import'] = get_best_import_path_for_class(class_name)
    class_data['fields'] = get_fields(class_data['parents'][::-1])
    class_data['methods'] = get_methods(class_data['parents'][::-1])
    class_data['framework_name'] = class_data['import'].partition('.')[0].replace('_', ' ').capitalize()
    return class_data


def get_structure_data(name=None) -> dict:
    """
    A function returning a structure of modules and frameworks
    :param name: a framework name
    :return: dict with a structure of modules and frameworks
    """
    if name is None or name not in menu_dict:
        return {'frameworks': menu_dict}
    return {'framework_name': name, 'modules': menu_dict[name]}
