from modules._interfaces.CommonLogic import CommonLogic


class IOLogic:
    @staticmethod
    def do_print_message(message):
        print(message)

    @staticmethod
    def print_to_file(filename, message):
        try:
            with open(filename, 'w') as f:
                f.write(message)
        except:
            raise CommonLogic.RunTimeError(
                f'Incorrect filename: `{filename}`'
            )


class IO:
    __info = [
        ['print', IOLogic.do_print_message, [str], None, None],
        ['print_to_file', IOLogic.print_to_file, [str, str], None, None],
    ]

    @staticmethod
    def get_info():
        return IO.__info