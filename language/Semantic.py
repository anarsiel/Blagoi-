class Semantic:
    __variable_name_pattern = '[%][a-zA-Z_][a-zA-Z0-9_]*'
    __symbols = {'var_separator'   : ':=',
                 'var'             : 'var',
                 'import'          : 'import',
                 'return_variable' : '_'}

    @staticmethod
    def get_variable_name_pattern():
        return Semantic.__variable_name_pattern

    @staticmethod
    def get_symbol(name):
        return Semantic.__symbols[name]