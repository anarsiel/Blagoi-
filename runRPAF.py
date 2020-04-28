import sys
import logging

from body.Interpreter import Interpreter

interpreter = Interpreter()
try:
    interpreter.parse_file(sys.argv[1])
except (Interpreter.CompilationError, Interpreter.RunTimeError) as exception:
    logging.error(str(exception))
except Interpreter.RunTimeWarning as exception:
    logging.warning(str(exception))