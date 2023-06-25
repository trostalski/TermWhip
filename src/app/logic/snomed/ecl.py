def transform_ecl_to_sql(ecl_expression):
    # Define a dictionary to map the ECL operators to their equivalent SQL operators
    operator_map = {
        "=": "=",
        "<": "<",
        ">": ">",
        "<=": "<=",
        ">=": ">=",
        "<>": "!=",
        "!=": "!=",
        "AND": "AND",
        "OR": "OR",
        "MINUS": "EXCEPT",
        "CHILDREN": "@>",
        "DESCENDANT": "<@",
        "SELF": "=",
        "ANCESTOR": "<@",
        "PARENT": "@>",
        "SIBLING": "<>",
    }

    # Split the ECL expression into tokens using whitespace as a delimiter
    tokens = ecl_expression.split()

    # Create an empty list to store the SQL query parts
    sql_parts = []

    # Iterate over each token and generate the appropriate SQL syntax
    for i, token in enumerate(tokens):
        # Check if the token is an operator
        if token.upper() in operator_map:
            # Map the ECL operator to its equivalent SQL operator
            sql_operator = operator_map[token.upper()]

            # If the operator is a comparison operator, add the left and right operands to the SQL query
            if sql_operator in ["=", "<", ">", "<=", ">=", "!=", "<>"]:
                left_operand = tokens[i - 1]
                right_operand = tokens[i + 1]

                # If the left operand is a concept ID, wrap it in quotes to make it a string literal
                if left_operand.isdigit():
                    left_operand = f"'{left_operand}'"

                # If the right operand is a concept ID, wrap it in quotes to make it a string literal
                if right_operand.isdigit():
                    right_operand = f"'{right_operand}'"

                sql_parts.append(f"{left_operand} {sql_operator} {right_operand}")

        # Check if the token is a modifier
        elif token.upper() in [
            "MINUS",
            "CHILDREN",
            "DESCENDANT",
            "SELF",
            "ANCESTOR",
            "PARENT",
            "SIBLING",
        ]:
            # Map the ECL modifier to its equivalent SQL syntax
            sql_modifier = operator_map[token.upper()]

            # Add the modifier to the SQL query
            sql_parts.append(sql_modifier)

    # Combine the SQL query parts into a complete SQL query
    sql_query = "SELECT DISTINCT concept_id FROM concept WHERE " + " ".join(sql_parts)

    return sql_query
