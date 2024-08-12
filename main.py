import streamlit as st
import re


OPERATORS = ["+", "-", "*", "/"]
NUMS = "0123456789"

# Initialize the calculator's state
if "current_expression" not in st.session_state:
    st.session_state.current_expression = "0"
if "last_operator" not in st.session_state:
    st.session_state.last_operator = None
if "new_input" not in st.session_state:
    st.session_state.new_input = True


def input_number(num):
    """Handle number input."""
    # a regex pattern that matches the delimiters (operators)
    delimiters = OPERATORS
    pattern = '|'.join(map(re.escape, delimiters))

    if st.session_state.new_input:
        st.session_state.current_expression = num
        st.session_state.new_input = False
    else:
        if num == '.' and '.' in re.split(pattern, st.session_state.current_expression)[-1]:
            return  # prevent adding another dot to a number
        st.session_state.current_expression += num
    print("Current expression: ", st.session_state.current_expression)


def input_operator(op):
    """Handle operator input."""
    if st.session_state.last_operator:
        compute_result(op)
        st.session_state.current_expression += op
    else:
        st.session_state.current_expression += op
    print("Current expression: ", st.session_state.current_expression)
    st.session_state.last_operator = op  


def split_expression(expression: str):
    negative = False
    if expression[0] == "-":
        negative = True
        expression = expression[1:]
    
    for pos, char in enumerate(expression):
        if char in OPERATORS:
            operand_0 = float(expression[:pos])
            operand_1 = float(expression[pos+1:])
            operator = char
            if negative:
                operand_0 = -operand_0
            return operator, operand_0, operand_1
    return None, None, None


def eval(expression):
    operator, operand_0, operand_1 = split_expression(expression)
    if operator is None:
        return 0
    elif operator == "+":
        result = operand_0 + operand_1
    elif operator == "-":
        result = operand_0 - operand_1
    elif operator == "*":
        result = operand_0 * operand_1
    else:
        result = operand_0 / operand_1

    return round(result, 8)


def compute_result(op):
    """Compute the result based on the last operator."""
    if st.session_state.last_operator is not None:
        try:
            result = eval(st.session_state.current_expression)
            # if result is both a float and integer, convert it to integer
            if result.is_integer():
                result = int(result)
            st.session_state.current_expression = str(result)
        except ZeroDivisionError:
            st.session_state.current_expression = "INF"

        if op == "=":
            st.session_state.last_operator = None
        print("Current expression: ", st.session_state.current_expression)


def clear():
    """Clear the calculator."""
    st.session_state.current_expression = "0"
    st.session_state.last_operator = None
    st.session_state.new_input = True
    st.rerun()


# Display the calculator
st.title("My simple Calculator")
value_cols = st.columns([3, 1])
with value_cols[0]:
    st.text_input("Display", value=st.session_state.current_expression, key="display", disabled=True, label_visibility="collapsed")
with value_cols[1]:
    if st.button("AC"):
        clear()


# Add custom CSS to match the button height with the input field
st.markdown(
    """
    <style>
    div.stButton > button:first-child {
        width: 100%;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Regular buttons
cols = st.columns(4)

for i, symbol in enumerate("789/456*123-0.=+"):
    with cols[i % 4]:
        if symbol == "=":
            if st.button(symbol, key=symbol):
                compute_result(symbol)
                st.rerun()
        elif symbol == ".":
            if st.button(symbol, key=symbol):
                input_number(symbol) 
                st.rerun()
        elif symbol in NUMS:
            if st.button(symbol, key=symbol):
                input_number(symbol) 
                st.rerun()
        elif symbol in OPERATORS:
            if st.button(symbol, key=symbol):
                input_operator(symbol) 
                st.rerun()
        else:
            if st.button(symbol, key=symbol):
                pass
