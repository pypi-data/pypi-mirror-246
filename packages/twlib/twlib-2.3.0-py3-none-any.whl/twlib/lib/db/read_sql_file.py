def read_sql_from_file(filepath: str) -> dict:
    """
    Reads SQL statements from a file and organizes them into a dictionary.

    The function expects the file to contain SQL statements separated by ';\n'.
    Each statement must be preceded by a comment line starting with '-- result-title:',
    which will be used as the key in the returned dictionary.
    The SQL statement itself will be the value associated with this key.

    Returns:
    dict: A dictionary where each key is a title extracted from the comment line,
    and each value is the corresponding SQL statement.
    """
    with open(filepath, "r") as f:
        content = f.read()

    sql_dict = {}
    for section in content.split(";\n"):
        lines = section.split("\n")
        title_line = None
        sql_lines = []

        for line in lines:
            if line.strip().startswith("-- result-title:"):
                title_line = line
            elif line.strip() and not line.strip().startswith("--"):
                sql_lines.append(line)

        if title_line and sql_lines:
            title = title_line.split(":")[1].strip()
            sql_statement = "\n".join(sql_lines).strip()
            sql_dict[title] = sql_statement

    return sql_dict


def test_read_sql_from_file(tmpdir):
    # Prepare a temp SQL file
    p = tmpdir.mkdir("sub").join("testfile.sql")
    p.write(
        "-- result-title: show-entry\nselect *\nfrom public.\"user\"\nwhere first_name = 'test'\n;\n\n-- result-title: test-write\nINSERT INTO public.\"user\" (first_name, last_name, email)\nVALUES ('test', 'test', 'test@test.test')\nreturning *;\n;\n\n-- result-title: test-read\nDELETE\nFROM public.\"user\"\nWHERE first_name = 'test'\nreturning *;\n;"
    )

    result = read_sql_from_file(p.strpath)

    assert isinstance(result, dict)
    assert "show-entry" in result
    assert "test-write" in result
    assert "test-read" in result

    assert (
        result["show-entry"]
        == "select *\nfrom public.\"user\"\nwhere first_name = 'test'"
    )
    assert (
        result["test-write"]
        == "INSERT INTO public.\"user\" (first_name, last_name, email)\nVALUES ('test', 'test', 'test@test.test')\nreturning *"
    )
    assert (
        result["test-read"]
        == "DELETE\nFROM public.\"user\"\nWHERE first_name = 'test'\nreturning *"
    )


def test_read_sql_from_file_with_incorrect_format(tmpdir):
    # Prepare a temp SQL file
    p = tmpdir.mkdir("sub").join("testfile.sql")
    p.write("This is not a valid SQL file")

    result = read_sql_from_file(p.strpath)

    assert isinstance(result, dict)
    assert not result  # Should be an empty dictionary
