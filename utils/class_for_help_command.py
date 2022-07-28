

class InitialClass:
    help_str = ''

    def set_help_str(self, cls):
        ignor_list = set()
        for base in cls.__bases__:
            for func_name in dir(base):
                ignor_list.add(func_name)
        i = 0
        for func_name in dir(cls):
            func = getattr(cls, func_name)
            if not callable(func) or func_name.startswith('_') or func_name in ignor_list:
                continue

            i += 1
            cls.help_str += f'{i}: {func_name} '
            for par_name, par_type in func.__dict__['params'].items():
                if par_name == 'self' or par_name == 'ctx':
                    continue
                if par_type.default is None:
                    cls.help_str += f'<{par_name}>'
                else:
                    cls.help_str += f'[{par_name}]'

            cls.help_str += '\n'
        cls.help_str[-1] = ''
