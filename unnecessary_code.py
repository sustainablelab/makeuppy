def get_arg(swp='()'):
    """
    This is not necessary. Just use :eval.

    Return string found between '(' and ')' in input string
    'swp'.

    Returns empty string for common cases that cause Python
    built-in 'eval()' to throw an error message.

    Where possible, return a message to help the user correct
    their input expression.

    Parameters
    ----------
    'swp'
        String with parentheses
        Example: "eval('1+1')"

    Behavior
    --------
    Returns Missing ')' if input string is missing )
    Returns Missing '(' if input string is missing (
    Returns empty string if input string is ()
    Returns empty string if input string is ("")
    Returns empty string if input string is ("   ")
    Returns empty string if input string is ('')
    Returns empty string if input string is ('   ')
    Returns help message if eval expression is not a string
    Returns help message if quotes are mismatched
    Returns help message if string inside () is only one character
    Returns subset of input string that is inside parentheses

    Reference
    ---------
    https://docs.python.org/3/library/stdtypes.html#mutable-sequence-types
    https://docs.python.org/3/library/stdtypes.html#string-methods
    """
    # Turn input into a string if not already a string
    if type(swp) != str: swp = str(swp)
    # Check for missing parentheses
    if swp.find('(') == -1: return ["Missing '('"]
    if swp.find(')') == -1: return ["Missing ')'"]
    # Check for mismatched parentheses
    if swp.count('(') != swp.count(')'): return [f"Missing parentheses somewhere"]
    # Get string between (), eliminate surrounding whitespace
    after_open = swp.split('(',maxsplit=1)[1]
    inside = after_open.rsplit(')',maxsplit=1)[0].strip()
    # Check for truly empty input ()
    if len(inside) == 0: return ''
    # If not empty, it must start with a quote mark
    qm = inside[0]
    # Check expression part of arg is a string
    if qm != "'" and qm != '"': return ["Expression must be a string"]
    # Check for missing closing quote
    if len(inside) == 1: return [f"Missing closing {qm}"]
    # Check for mistmatched quotes
    if inside.count(qm)%2 != 0: return [f"Missing {qm} somewhere"]
    # Check for creative ways to send empty input
    using_single_quotes = inside[0] == "'"
    using_double_quotes = inside[0] == '"'
    if using_single_quotes:
        if (
            inside.split("'")[1] == ''
            or
            inside.split("'")[1].isspace()
            ):
            return ''
    if using_double_quotes:
        if (
            inside.split('"')[1] == ''
            or
            inside.split('"')[1].isspace()
            ):
            return ''
    # Success: string inside parentheses is OK to eval... maybe...
    return inside
def evaluate(cmd):
    """
    Activate 'cmdline' with : to start a COLON command.
    Return values are displayed on the 'cmdoutput' line.

    COLON command types
    -------------------
    :eval(expression)
        Evaluate with Python builtin 'eval'
        Example:
            :eval('1+1')
            2

    TODO: instead of requiring user to type 'eval', make this the
    ':echo' command, and do not require input arguments to be a
    string.

    TODO: use real ':eval' by sending parsed arg back to
    application to run 'eval(arg)' -- this makes 'eval()' useful
    because it lets user access the variables in the application.
    Calling eval from pygameapi.py only gives access to variables
    in pygameapi.py, which is not too useful.
    """
    # Catch 0-length commands (happens if user erases ':' and hits ENTER)
    empty = ''
    if len(cmd) == 0: return empty
    # COLON commands
    if cmd.startswith(':'):
        # strip leading `:`
        cmd = cmd[1:]
        if cmd[0:4] == 'eval':
            # EVAL EXPRESSIONS
            """
                Return an empty 'str' when:
                    The expression cannot be evaluated and there is no
                    obvious mistake to notify the user, like a missing
                    quote or parentheses.
                Examples when empty is appropriate:
                    :eval('')
                    :eval()
                    :eval("    ")
            """
            # arg = get_arg(cmd)
            # # arg is empty: ()
            # if arg == empty: return empty
            # # arg mistake is obvious
            # """
            #     Return a 'list' when:
            #         The expression cannot be evaluated and the
            #         mistake is obvious.
            #         List element 0 is a helpful message to display
            #         in the 'cmdoutput'.
            #     Examples when a helpful message is appropriate:
            #         :eval('print()) # user forgot "'"
            #         :eval('print()' # user forgot ")"
            # """
            # if type(arg) == list: return 'ERROR: ' + arg[0]
            # arg = eval(arg)
            # if type(arg) == str: return eval(arg)
            # # If user includes optional global dict or local dict,
            # # eval(get_arg(cmd)) returns a tuple.
            # if type(arg) == tuple:
            #     if len(arg) == 2: return eval(arg[0],arg[1])
            #     if len(arg) == 3: return eval(arg[0],arg[1],arg[2])

# Tests
class get_arg(unittest.TestCase):
    def test_Returns_help_message_if_input_string_is_missing_OPENPAREN(self):
        arg = "'1+x',{'x':3}"
        missing_open = f"eval{arg})"
        self.assertEqual(["Missing '('"], pgui.get_arg(missing_open))
    def test_Returns_help_message_if_input_string_is_missing_CLOSEPAREN(self):
        arg = "'1+x',{'x':3}"
        missing_close = f"eval({arg}"
        self.assertEqual(["Missing ')'"], pgui.get_arg(missing_close))
    def test_Returns_empty_string_if_input_string_is_OPENPARENCLOSEPAREN(self):
        empty_inside = "eval()"
        self.assertEqual('', pgui.get_arg(empty_inside))
    def test_Returns_help_message_if_eval_expression_is_not_a_string(self):
        self.assertEqual(["Expression must be a string"], pgui.get_arg("eval(2)"))
    def test_Returns_help_message_if_string_inside_OPENPARENCLOSEPAREN_is_only_one_character(self):
        qm = "'"
        self.assertEqual([f"Missing closing {qm}"], pgui.get_arg(f"eval({qm})"))
        qm = '"'
        self.assertEqual([f"Missing closing {qm}"], pgui.get_arg(f"eval({qm})"))
    def test_Returns_help_message_if_quotes_are_mismatched(self):
        qm = "'"
        self.assertEqual([f"Missing {qm} somewhere"], pgui.get_arg(f"eval({qm}2)"))
        qm = '"'
        self.assertEqual([f"Missing {qm} somewhere"], pgui.get_arg(f"eval({qm}2)"))
    def test_Returns_empty_string_if_input_string_is_OPENPARENSQUOTESQUOTECLOSEPAREN(self):
        empty_inside = "eval('')"
        self.assertEqual('', pgui.get_arg(empty_inside))
    def test_Returns_empty_string_if_input_string_is_OPENPARENSQUOTE___SQUOTECLOSEPAREN(self):
        empty_inside = "eval('   ')"
        self.assertEqual('', pgui.get_arg(empty_inside))
    def test_Returns_empty_string_if_input_string_is_OPENPARENDQUOTEDQUOTECLOSEPAREN(self):
        empty_inside = 'eval("")'
        self.assertEqual('', pgui.get_arg(empty_inside))
    def test_Returns_empty_string_if_input_string_is_OPENPARENDQUOTE___DQUOTECLOSEPAREN(self):
        empty_inside = 'eval("   ")'
        self.assertEqual('', pgui.get_arg(empty_inside))
    def test_Returns_subset_of_input_string_that_is_inside_parentheses(self):
        arg = "'1+1'"
        self.assertEqual(arg, pgui.get_arg(f"eval({arg})"))
        arg = "'1+x',{'x':3}"
        self.assertEqual(arg, pgui.get_arg(f"eval({arg})"))

class evaluate(unittest.TestCase):
    def test_Evaluates_DQUOTECOLONevalOPENPARENexpressionCLOSEPARENDQUOTE_by_returning_Python_builtin_SQUOTEevalOPENPARENexpressionCLOSEPARENSQUOTE(self):
        cmd = ":eval('1')"
        self.assertEqual(1, pgui.evaluate(cmd))
    def test_Evaluates_simple_expressions_like_DQUOTECOLONevalOPENPARENSQUOTE1PLUS1SQUOTECLOSEPARENDQUOTE(self):
        cmd = ":eval('1+1')"
        self.assertEqual(2, pgui.evaluate(cmd))
    def test_Evaluates_expressions_that_use_a_global_dict(self):
        cmd = ":eval('1+x',{'x':5})"
        self.assertEqual(6, pgui.evaluate(cmd))
    def test_Evaluates_expressions_that_use_global_and_local_dicts(self):
        cmd = ":eval('1+x+a_local',{'x':5},{'a_local':2})"
        self.assertEqual(8, pgui.evaluate(cmd))
    def test_Returns_empty_string_if_cmd_input_is_DQUOTECOLONevalOPENPARENCLOSEPARENDQUOTE(self):
        cmd = ":eval()"
        empty = ''
        self.assertEqual('', pgui.evaluate(cmd))
    def test_Returns_empty_string_if_cmd_input_is_DQUOTECOLONevalOPENPARENSQUOTESQUOTECLOSEPARENDQUOTE(self):
        cmd = ":eval('')"
        empty = ''
        self.assertEqual('', pgui.evaluate(cmd))
    def test_Returns_empty_string_if_cmd_input_is_SQUOTECOLONevalOPENPARENDQUOTEDQUOTECLOSEPARENSQUOTE(self):
        cmd = ':eval("")'
        empty = ''
        self.assertEqual('', pgui.evaluate(cmd))
    def test_Ignores_whitespace_inside_the_parentheses(self):
        empty = ''
        cmd = ':eval( "" )'
        self.assertEqual('', pgui.evaluate(cmd))
        cmd = ':eval( " " )'
        self.assertEqual('', pgui.evaluate(cmd))

