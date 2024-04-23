import sys
from io import StringIO

def evaluate_python_file(python_file, evaluation_script):
    with open(evaluation_script, 'r') as script_file:
        lines = script_file.readlines()

    input_outputs = []
    i = 0

    while i < len(lines):
        line = lines[i].strip()

        if line.startswith("Case"):
            case_number = line.split(" ")[1].strip(":")
            input_line = lines[i + 1].strip()
            output_line = lines[i + 2].strip()
            points_line = lines[i + 3].strip()

            inputs = eval(input_line.split(":")[1].strip())
            expected_output = eval(output_line.split(":")[1].strip())
            points = int(points_line.split(":")[1].strip())

            input_outputs.append((case_number, inputs, expected_output, points))
            i += 4

    results = []

    for case_number, input_value, expected_output, points in input_outputs:
        sys.argv[1:] = [str(value) for value in input_value]

        captured_output = StringIO()
        original_stdout = sys.stdout
        sys.stdout = captured_output

        try:
            exec(compile(open(python_file).read(), python_file, 'exec'))
        except Exception as e:
            print(f"Error while executing Python file for case {case_number}: {e}")
            sys.stdout = original_stdout
            continue

        sys.stdout = original_stdout
        output = captured_output.getvalue().strip()

        if output == str(expected_output):
            result = f"Case {case_number}: PASSED (+{points} points)"
        else:
            result = f"Case {case_number}: FAILED (Expected: {expected_output}, Actual: {output})"

        results.append(result)

    return {"status":200, "result":results}