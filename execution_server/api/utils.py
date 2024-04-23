import subprocess


def execute_python(volume_path: str, file_name_list: list, output_path: str):
    result_of_execution = subprocess.run(
        ["python3"] + [volume_path + "/" + name for name in file_name_list],
        capture_output=True,
        text=True,
    )
    result = (
        result_of_execution.stderr
        if result_of_execution.returncode
        else result_of_execution.stdout
    )

    f = open(output_path, "w")
    f.write(result)
    f.close()

    return {"status": 200, "detail": {"message": "Successfully executed!"}}


def execute_java(volume_path: str, file_name_list: list, output_path: str):
    result_of_compilation = subprocess.run(
        ["javac"] + [volume_path + "/" + name for name in file_name_list],
        capture_output=True,
        text=True,
    )
    if result_of_compilation.returncode != 0:
        return {
            "status": 400,
            "detail": {
                "message": f"Compilation failed with return code {result_of_compilation.stderr}"
            },
        }

    result_of_execution = subprocess.run(
        ["java", "main"], capture_output=True, text=True
    )
    result = (
        result_of_execution.stderr
        if result_of_execution.returncode
        else result_of_execution.stdout
    )

    f = open(output_path, "w")
    f.write(result)
    f.close()

    return {"status": 200, "detail": {"message": "Successfully executed!"}}


def execute_cpp(volume_path: str, file_name_list: list, output_path: str):
    result_of_compilation = subprocess.run(
        ["g++"]
        + [volume_path + "/" + name for name in file_name_list]
        + ["-o", "compiled_binary"],
        capture_output=True,
        text=True,
    )
    if result_of_compilation.returncode != 0:
        return {
            "status": 400,
            "detail": {
                "message": f"Compilation failed with return code {result_of_compilation.returncode}"
            },
        }

    result_of_execution = subprocess.run(
        ["./compiled_binary"], capture_output=True, text=True
    )
    result = (
        result_of_execution.stderr
        if result_of_execution.returncode
        else result_of_execution.stdout
    )

    f = open(output_path, "w")
    f.write(result)
    f.close()

    return {"status": 200, "detail": {"message": "Successfully executed!"}}


def execute_c(volume_path: str, file_name_list: list, output_path: str):
    result_of_compilation = subprocess.run(
        ["gcc"]
        + [volume_path + "/" + name for name in file_name_list]
        + ["-o", "compiled_binary"],
        capture_output=True,
        text=True,
    )
    if result_of_compilation.returncode != 0:
        return {
            "status": 400,
            "detail": {
                "message": f"Compilation failed with return code {result_of_compilation.returncode}"
            },
        }

    result_of_execution = subprocess.run(
        ["./compiled_binary"], capture_output=True, text=True
    )
    result = (
        result_of_execution.stderr
        if result_of_execution.returncode
        else result_of_execution.stdout
    )

    f = open(output_path, "w")
    f.write(result)
    f.close()

    return {"status": 200, "detail": {"message": "Successfully executed!"}}


def execute_haskell(volume_path: str, file_name_list: list, output_path: str):
    result_of_compilation = subprocess.run(
        ["ghc"]
        + [volume_path + "/" + name for name in file_name_list]
        + ["-o", "compiled_binary"],
        capture_output=True,
        text=True,
    )
    if result_of_compilation.returncode != 0:
        return {
            "status": 400,
            "detail": {
                "message": f"Compilation failed with return code {result_of_compilation.returncode}"
            },
        }

    result_of_execution = subprocess.run(
        ["./compiled_binary"], capture_output=True, text=True
    )
    result = (
        result_of_execution.stderr
        if result_of_execution.returncode
        else result_of_execution.stdout
    )

    f = open(output_path, "w")
    f.write(result)
    f.close()

    return {"status": 200, "detail": {"message": "Successfully executed!"}}


def execute_prolog(volume_path: str, file_name_list: list, output_path: str):
    result_of_compilation = subprocess.run(
        ["gplc"]
        + [volume_path + "/" + name for name in file_name_list]
        + ["-o", "compiled_binary"],
        capture_output=True,
        text=True,
    )
    if result_of_compilation.returncode != 0:
        return {
            "status": 400,
            "detail": {
                "message": f"Compilation failed with return code {result_of_compilation.returncode}"
            },
        }

    result_of_execution = subprocess.run(
        ["./compiled_binary"], capture_output=True, text=True
    )
    result = (
        result_of_execution.stderr
        if result_of_execution.returncode
        else result_of_execution.stdout
    )

    f = open(output_path, "w")
    f.write(result)
    f.close()

    return {"status": 200, "detail": {"message": "Successfully executed!"}}

language_map = {
    "python": execute_python,
    "java": execute_java,
    "cpp": execute_cpp,
    "c": execute_c,
    "haskell": execute_haskell,
    "prolog": execute_prolog,
}


def execute_files(
    pl_language: str, volume_path: str, file_name_list: list, output_path: str
):
    execution_function = language_map[pl_language]
    return execution_function(volume_path, file_name_list, output_path)


def execute_make(volume_path: str, args: list, output_path: str):
    result_of_execution = subprocess.run(
        ["make"] + [volume_path + "/" + name for name in args],
        capture_output=True,
        text=True,
    )
    if result_of_execution.returncode != 0:
        return {
            "status": 400,
            "detail": {
                "message": f"Execution failed with return code {result_of_execution.returncode}"
            },
        }

    parse_result = parse(result_of_execution.stdout)
    result_of_saving = subprocess.run(
        ["echo", f"{parse_result}", ">>", f"{output_path}"],
        capture_output=True,
        text=True,
    )
    if result_of_saving.returncode != 0:
        return {
            "status": 400,
            "detail": {
                "message": f"Saving failed with return code {result_of_saving.returncode}"
            },
        }

    return {"status": 200, "detail": {"message": "Successfully executed!"}}
