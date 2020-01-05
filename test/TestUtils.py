from pathlib import Path


def resolve_path_test_sources() -> str:
    this_file = Path(__file__)
    return this_file.parent.parent.absolute().joinpath("test_sources").as_posix()
