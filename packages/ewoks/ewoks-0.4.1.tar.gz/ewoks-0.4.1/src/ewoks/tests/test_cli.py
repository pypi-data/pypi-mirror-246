import os
import sys
import pytest

from ewoks.__main__ import main
from ewokscore import load_graph
from ewokscore.tests.examples.graphs import graph_names
from ewokscore.tests.examples.graphs import get_graph
from ewokscore.tests.utils.results import assert_execute_graph_default_result


@pytest.mark.parametrize("graph_name", graph_names())
@pytest.mark.parametrize("scheme", (None, "json"))
@pytest.mark.parametrize("engine", (None, "dask", "ppf"))
def test_execute(graph_name, scheme, engine, tmpdir):
    graph, expected = get_graph(graph_name)
    argv = [sys.executable, "execute", graph_name, "--test", "--merge-outputs"]
    if engine:
        argv += ["--engine", engine]
    if engine == "ppf":
        argv += ["--outputs", "end"]
    else:
        argv += ["--outputs", "all"]
    if scheme:
        argv += ["--data-root-uri", str(tmpdir), "--data-scheme", scheme]
        varinfo = {"root_uri": str(tmpdir), "scheme": scheme}
    else:
        varinfo = None

    keep = graph
    ewoksgraph = load_graph(graph)
    non_dag = ewoksgraph.is_cyclic or ewoksgraph.has_conditional_links

    if non_dag and engine != "ppf":
        with pytest.raises(RuntimeError):
            main(argv=argv, shell=False)
        return

    result = main(argv=argv, shell=False)

    assert_execute_graph_default_result(ewoksgraph, result, expected, varinfo)
    assert keep == graph


@pytest.mark.parametrize("graph_name", graph_names())
def test_convert(graph_name, tmpdir):
    destination = str(tmpdir / f"{graph_name}.json")
    argv = [
        sys.executable,
        "convert",
        graph_name,
        destination,
        "--test",
        "-s",
        "indent=2",
    ]
    main(argv=argv, shell=False)
    assert os.path.exists(destination)
