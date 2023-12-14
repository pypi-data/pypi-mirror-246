import jupytext

def reads(file, format=".md", **kwargs):

    namespace = {}
    exec(file, namespace)
    # Print or return the output
    result = namespace.get('output', None)
    return jupytext.reads(result, {"extension": format}, **kwargs)