#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2021 - 2023 Mewbot Developers <mewbot@quicksilver.london>
#
# SPDX-License-Identifier: BSD-2-Clause


# pylint: disable=import-outside-toplevel


"""
Wrapper class for running linting tools.

The output of these tools will be emitted as GitHub annotations (in CI)
or default human output (otherwise).
By default, all paths declared to be part of mewbot source - either of the main
module or any installed plugins - are linted.
"""

from __future__ import annotations

from collections.abc import Iterable
from typing import Optional, Union

import argparse
import dataclasses
import os
import subprocess
import sys

from .path import gather_paths, gather_paths_standard_locs
from .security_analysis import BanditMixin
from .toolchain import Annotation

LEVELS = frozenset({"notice", "warning", "error"})


@dataclasses.dataclass
class LintOptions:
    """
    Used for programmatic invocations of lint when you might not want to deal with argparse.

    Mostly written for testing purposes - but there might be other uses.
    """

    path: list[str]
    in_ci: bool = False
    tests: bool = True

    def __init__(self) -> None:
        """
        Some startup tasks need to be done on init.
        """
        self.path = [
            os.getcwd(),
        ]


class LintToolchain(BanditMixin):
    """
    Wrapper class for running linting tools.

    The output of these tools will be emitted as GitHub annotations (in CI)
    or default human output (otherwise).
    By default, all paths declared to be part of mewbot source - either of the main
    module or any installed plugins - are linted.
    """

    def run(self) -> Iterable[Annotation]:
        """Runs the linting tools in sequence."""

        # Linters that can mutate code
        yield from self.lint_isort()
        yield from self.lint_black()
        yield from self.lint_ruff()
        # Linters that only read code
        yield from self.lint_flake8()
        yield from self.lint_mypy()
        yield from self.lint_pylint()
        yield from self.lint_pydocstyle()
        yield from self.lint_bandit()

    def lint_isort(self) -> Iterable[Annotation]:
        """
        Run 'isort', an automatic import ordering tool.

        Black handles most formatting updates automatically, maintaining
        readability and code style compliance.
        """

        args = [
            "isort",
        ]

        if self.in_ci:
            args.extend(["--diff", "--quiet"])

        isort_name: str = "isort (Imports Re-ordering)"
        result = self.run_tool(isort_name, *args)

        # isort returns code 0 if the program runs successfully.
        # It does not care if the ordering is correct
        # So need to give the method which processes the output the chance to complain

        yield from lint_isort_diffs(result, isort_name, self.run_success)

    def lint_black(self) -> Iterable[Annotation]:
        """
        Run 'black', an automatic formatting tool.

        Black handles most formatting updates automatically, maintaining
        readability and code style compliance.
        """

        args = ["black"]

        if self.in_ci:
            args.extend(["--diff", "--no-color", "--quiet"])

        result = self.run_tool("Black (Formatter)", *args)

        yield from lint_black_errors(result)
        yield from lint_black_diffs(result)

    def lint_flake8(self) -> Iterable[Annotation]:
        """
        Runs 'flake8', an efficient code-style enforcer.

        flake8 is a lightweight and fast tool for finding issues relating to
        code-style, import management (both missing and unused) and a range of
        other issue.
        """

        result = self.run_tool("Flake8", "flake8")

        for line in result.stdout.decode("utf-8").split("\n"):
            if ":" not in line:
                continue

            try:
                file, line_no, col, error = line.strip().split(":", 3)
                yield Annotation(
                    "error", file, int(line_no), int(col), "flake8", "", error.strip()
                )
            except ValueError:
                pass

    def lint_mypy(self) -> Iterable[Annotation]:
        """
        Runs 'mypy', a python type analyser/linter.

        mypy enforces the requirement for type annotations, and also performs type-checking
        based on those annotations and resolvable constants.
        """

        args = ["mypy", "--strict", "--explicit-package-bases"]
        env = {}

        if not self.in_ci:
            env["MYPY_FORCE_COLOR"] = "1"
            args.append("--pretty")

        # MyPy does not use the stock import engine for doing its analysis,
        # so we have to give it additional hints about how the namespace package
        # structure works.
        # See https://mypy.readthedocs.io/en/stable/running_mypy.html#mapping-file-paths-to-modules
        #
        # There are two steps to this:
        #  - We set MYPYPATH equivalent to PYTHONPATH
        env["MYPYPATH"] = os.pathsep.join(gather_paths("src", search_root=self.search_root))

        #  - We alter the folder list such that, in src-dir folders, we pass the
        #    folder of the actual pacakge (i.e. ./src/mewbot rather than ./src)
        folders = set(get_module_paths(*self.folders))

        # Run mypy
        result = self.run_tool("MyPy (type checker)", *args, env=env, folders=folders)

        for line in result.stdout.decode("utf-8").split("\n"):
            if ":" not in line:
                continue

            try:
                file, line_no, level, error = line.strip().split(":", 3)
                level = level.strip()

                if level == "note":
                    level = "notice"

                level = level if level in LEVELS else "error"

                yield Annotation(level, file, int(line_no), 1, "mypy", "", error.strip())
            except ValueError:
                pass

    def lint_pylint(self) -> Iterable[Annotation]:
        """
        Runs 'pylint', the canonical python linter.

        pylint performs a similar set of checks as flake8, but does so using the full
        codebase as context. As such it will also find similar blocks of code and other
        subtle issues.
        """

        result = self.run_tool("PyLint", "pylint")

        result_lines = result.stdout.decode("utf-8", errors="replace")

        for line in result_lines.split("\n"):
            if ":" not in line:
                continue

            try:
                file, line_no, col, error = line.strip().split(":", 3)
                yield Annotation("error", file, int(line_no), int(col), "pylint", "", error)
            except ValueError:
                pass

    def lint_ruff(self) -> Iterable[Annotation]:
        """
        Runs 'ruff', a high performance python linter written in rust.

        Theoretically ruff is a superset of a number of other linters used here. It may take over
        as the default linter - for normal runs.
        However, for CI runs before accepting code, it makes sense to run the other linters as
        well.
        There should be no difference, but they are the reference implementations.
        Time is also less of a factor in a rare CI acceptance run.
        """

        args = ["ruff"]

        if not self.in_ci:
            args.append("--fix")

        result = self.run_tool("Ruff", *args)

        result_lines = result.stdout.decode("utf-8", errors="replace")

        for line in result_lines.split("\n"):
            if ":" not in line:
                continue

            try:
                file, line_no, col, error = line.strip().split(":", 3)
                yield Annotation("error", file, int(line_no), int(col), "pylint", "", error)
            except ValueError:
                pass

    def lint_pydocstyle(self) -> Iterable[Annotation]:
        """
        Runs 'pydocstyle', which tests python doc blocks.

        pydocstyle checks for the existence and format of doc strings in all
        python modules, classes, and methods. These will have to be formatted
        with a single headline, arguments, return values and any extra info.
        """

        result = self.run_tool("PyDocStyle", "pydocstyle", "--match=.*\\.py$")

        lines = iter(result.stdout.decode("utf-8").split("\n"))

        for header in lines:
            if ":" not in header:
                continue

            try:
                file, line_no = header.split(" ", 1)[0].split(":")
                error = next(lines).strip()

                yield Annotation("error", file, int(line_no), 1, "pydocstyle", "", error)
            except ValueError:
                pass
            except StopIteration:
                pass


def lint_black_errors(
    result: subprocess.CompletedProcess[bytes],
) -> Iterable[Annotation]:
    """Processes 'blacks' output in to annotations."""

    errors = result.stderr.decode("utf-8").split("\n")

    for error in errors:
        error = error.strip()

        if not error or ":" not in error:
            continue

        # Note - Improve error handling here - this could yield an annotation
        if error.lower().startswith("error: cannot format"):
            raise NotImplementedError("black cannot parse this file")

        # We're (hopefully) reporting on a reformat event
        if error.lower().startswith("reformatted"):
            yield _process_reformat_line(error)
            continue

        # We should, at this point, have a conventional error
        level, _, message, line, char, info, file = _tokenize_error_line(error)

        # It's possible the splitting has, coincidentally, worked when it shouldn't
        # Hence the error handling here
        try:
            yield Annotation(
                level, file, int(line), int(char), "black", message.strip(), info.strip()
            )
        except ValueError as exp:
            raise ValueError(f"Could not yield - could not parse line {error}") from exp


def _tokenize_error_line(error: str) -> tuple[str, str, str, str, str, str, str]:
    """
    Attempt to tokenize an error line into a format which we can use to yield annotations.
    """
    try:
        level, header, message, line, char, info = error.split(":", 5)
    except ValueError as exp:
        raise NotImplementedError(f"Unexpected case '{error}'") from exp

    header, _, file = header.rpartition(" ")

    level = level.strip() if level.strip() in LEVELS else "error"

    return level, header, message, line, char, info, file


def _process_reformat_line(error: str) -> Annotation:
    """
    A reformat line has been detected - process it.
    """
    level = "error"
    header = "File reformatted"
    _, file = header.split(" ")
    line = "0"
    char = "0"
    info = "File reformatted"
    return Annotation(level, file, int(line), int(char), "black", error.strip(), info.strip())


def lint_isort_diffs(
    result: subprocess.CompletedProcess[bytes], tool_name: str, run_success: dict[str, bool]
) -> Iterable[Annotation]:
    """Processes 'blacks' output in to annotations."""

    result_lines = list(result.stdout.decode("utf-8").split("\n"))

    yield from isort_diffs_to_annotations(result_lines, tool_name, run_success)
    yield from isort_fix_lines_to_annotations(result_lines, tool_name, run_success)


def isort_diffs_to_annotations(
    result_lines: list[str], tool_name: str, run_success: dict[str, bool]
) -> Iterable[Annotation]:
    """
    Transform lines from isort output into annotations - for isort diffs.
    """
    file = ""
    line = 0
    buffer = ""

    # Process diff lines
    for diff_line in result_lines:
        if diff_line.startswith("+++ "):
            continue

        if diff_line.startswith("--- "):
            if file and buffer:
                run_success[tool_name] = False
                yield Annotation("error", file, line, 1, "isort", "isort alteration", buffer)

            buffer = ""
            file, _ = diff_line[4:].split("\t")
            continue

        if diff_line.startswith("@@"):
            if file and buffer:
                run_success[tool_name] = False
                yield Annotation("error", file, line, 1, "isort", "isort alteration", buffer)

            _, start, _, _ = diff_line.split(" ")
            _line, _ = start.split(",")
            line = abs(int(_line))
            buffer = ""
            continue

        buffer += diff_line + "\n"


def isort_fix_lines_to_annotations(
    result_lines: list[str], tool_name: str, run_success: dict[str, bool]
) -> Iterable[Annotation]:
    """
    Transform lines from isort output into annotations - for isort fixed lines.
    """

    # Process fixing lines
    for cand_result_line in result_lines:
        if cand_result_line.lower().startswith("fixing"):
            _, file_path = cand_result_line.split(" ")
            run_success[tool_name] = False
            yield Annotation(
                "error", file_path, 0, 1, "isort", "isort alteration", cand_result_line
            )


def lint_black_diffs(
    result: subprocess.CompletedProcess[bytes],
) -> Iterable[Annotation]:
    """Processes 'blacks' output in to annotations."""

    file = ""
    line = 0
    buffer = ""

    for diff_line in result.stdout.decode("utf-8").split("\n"):
        if diff_line.startswith("+++ "):
            continue

        if diff_line.startswith("--- "):
            if file and buffer:
                yield Annotation("error", file, line, 1, "black", "Black alteration", buffer)

            buffer = ""
            file, _ = diff_line[4:].split("\t")
            continue

        if diff_line.startswith("@@"):
            if file and buffer:
                yield Annotation("error", file, line, 1, "black", "Black alteration", buffer)

            _, start, _, _ = diff_line.split(" ")
            _line, _ = start.split(",")
            line = abs(int(_line))
            buffer = ""
            continue

        buffer += diff_line + "\n"


def get_module_paths(*folders: str) -> Iterable[str]:
    """
    Covert a list of folders into modules paths.

    "src-dir" style folders will be expanded out into the paths for the
    root of each module. src-dir style roots are detected on the basis
    of being members of `sys.path`.
    """

    for path in folders:
        if path in sys.path:
            # Each folder in PYTHONPATH is considered a src-dir style collection of modules
            # We xpand these into the actual list of modules
            potential_paths = [os.path.join(path, module) for module in os.listdir(path)]
            yield from [
                module_path for module_path in potential_paths if os.path.isdir(module_path)
            ]
        else:
            # All other paths are returned unchanged
            yield path


def parse_lint_options() -> argparse.Namespace:
    """Parse command line argument for the linting tools."""

    parser = argparse.ArgumentParser(description="Run code linters for mewbot")
    parser.add_argument(
        "--ci",
        dest="in_ci",
        action="store_true",
        default="GITHUB_ACTIONS" in os.environ,
        help="Run in GitHub actions mode",
    )
    parser.add_argument(
        "--no-tests",
        dest="tests",
        action="store_false",
        default=True,
        help="Exclude tests from linting",
    )
    parser.add_argument(
        "path", nargs="*", default=[], help="Path of a file or a folder of files."
    )

    return parser.parse_args()


def main(
    search_root: Optional[str] = None, programatic_options: Optional[LintOptions] = None
) -> None:
    """
    Needed for script packaging.

    :param search_root:
    :return:
    """
    options: Union[LintOptions, argparse.Namespace] = (
        parse_lint_options() if programatic_options is None else programatic_options
    )

    paths = options.path
    if not paths:
        paths = gather_paths_standard_locs(search_root=search_root, tests=options.tests)

    linter = LintToolchain(*paths, in_ci=options.in_ci, search_root=os.curdir)
    linter()


if __name__ == "__main__":
    main()
