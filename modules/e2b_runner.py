def execute_code(code, df):

    local_env = {"df": df}

    output = {
        "figures": [],
        "text": []
    }

    try:
        exec(code, {}, local_env)

        # Collect figure
        if "fig" in local_env:
            output["figures"].append(local_env["fig"])

        # Collect printed text
        if "insight" in local_env:
            output["text"].append(str(local_env["insight"]))

        return output

    except Exception as e:
        return {"error": str(e)}


