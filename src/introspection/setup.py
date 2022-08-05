import importlib
import importlib.util

full_module_names = ['django.views.generic.base',
                     'django.views.generic.list',
                     'django.views.generic.detail',
                     'django.views.generic.edit',
                     'django.views.generic.dates',
                     'django.contrib.auth.views',
                     'django.forms.forms',
                     'django.forms.models',
                     'rest_framework.views',
                     'rest_framework.generics',
                     'rest_framework.serializers',
                     'rest_framework.mixins',
                     'rest_framework.parsers',
                     'rest_framework.authentication',
                     ]


def get_module_path(module):
    """Return origin module path"""
    module_info = importlib.util.find_spec(module)
    if module_info is None:
        return ''
    return module_info.origin


def get_module_classes(module):
    """Return all module classes using search string 'class ' """
    path_to_file = get_module_path(module)
    if not path_to_file:
        return []
    found_classes = []
    with open(path_to_file, 'r', encoding='utf8') as file:
        lines = file.readlines()
        for line in lines:
            if line[:6] == 'class ':
                found_class = line.split()[1]
                if ':' in found_class:
                    found_class = found_class.partition(':')[0]
                if '(' in found_class:
                    found_class = found_class.partition('(')[0]
                found_classes.append(found_class)
    return found_classes


def main():
    """Create settings.py file with:
     - a dictionary('classes_dict') with found classes from modules from 'full_module_names' module list;
     - imports of all these classes;
     - a dictionary('menu_dict') of structures frameworks, modules, classes.
     """
    result_import_lst = []
    result_dict_string = 'classes_dict = {\n\t'
    menu_dict = dict()
    for full_module_name in full_module_names:
        classes = get_module_classes(full_module_name)
        classes.sort()
        result = 'from ' + full_module_name + ' import ' + ', '.join(classes)
        result_dict_string += ',\n\t'.join("'" + class_name + "': " + class_name for class_name in classes)
        result_dict_string += ',\n\t'
        result_import_lst.append(result)
        packet_name = full_module_name.partition('.')[0].replace('_', ' ').capitalize()
        module_name = full_module_name.partition('.')[2].replace('.', ' ').capitalize()
        if packet_name not in menu_dict:
            menu_dict[packet_name] = dict()
        menu_dict[packet_name][module_name] = classes
    result_dict_string += '}'
    with open('settings.py', 'w', encoding='utf8') as file:
        for import_string in result_import_lst:
            file.write(import_string + '\n')
        file.write('\n\n')
        file.write(result_dict_string)
        file.write('\n\n')
        file.write('menu_dict = ')
        file.write(repr(menu_dict))
        file.write('\n')


if __name__ == '__main__':
    main()
