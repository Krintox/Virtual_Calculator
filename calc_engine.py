# calc_engine.py
import ast

class CalcError(Exception):
    pass

ALLOWED_BINOPS = {
    ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Mod, ast.Pow, ast.FloorDiv
}
ALLOWED_UNARYOPS = {ast.UAdd, ast.USub}

def _eval_node(node):
    if isinstance(node, ast.Expression):
        return _eval_node(node.body)

    if isinstance(node, ast.Constant):  # Python 3.8+
        if isinstance(node.value, (int, float)):
            return node.value
        else:
            raise CalcError("Invalid constant")
    if isinstance(node, ast.Num):  # older ast
        return node.n

    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        op = type(node.op)
        if op is ast.Add:
            return left + right
        if op is ast.Sub:
            return left - right
        if op is ast.Mult:
            return left * right
        if op is ast.Div:
            return left / right
        if op is ast.Mod:
            return left % right
        if op is ast.Pow:
            return left ** right
        if op is ast.FloorDiv:
            return left // right
        raise CalcError("Operation not allowed")

    if isinstance(node, ast.UnaryOp):
        if type(node.op) not in ALLOWED_UNARYOPS:
            raise CalcError("Unary op not allowed")
        val = _eval_node(node.operand)
        if isinstance(node.op, ast.UAdd):
            return +val
        if isinstance(node.op, ast.USub):
            return -val

    if isinstance(node, ast.Call):
        raise CalcError("Function calls not allowed")

    raise CalcError("Expression not allowed")

def safe_eval(expr: str):
    """
    Evaluate arithmetic expression safely.
    Raises CalcError on any invalid input.
    """
    try:
        parsed = ast.parse(expr, mode='eval')
    except Exception as e:
        raise CalcError("Parse error") from e

    value = _eval_node(parsed)
    return value
