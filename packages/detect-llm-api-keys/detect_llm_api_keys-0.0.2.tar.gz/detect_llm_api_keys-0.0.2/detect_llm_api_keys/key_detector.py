import ast
from detect_llm_api_keys.api_key_regexes import pats


override_comment_tags = {"nosec", "noqa"}


class APIKeyDetector(ast.NodeVisitor):
    """A class for detecting API keys in Python code."""

    def __init__(self, lines: list[str]):
        self._lines = lines
        self._results: dict[str, list[int]] = {}

    def _check_string(self, string_value: str, node: ast.AST) -> None:
        def _has_override_comment(node: ast.AST) -> bool:
            line = self._lines[node.lineno - 1]
            try:
                code, comment = line.rsplit("#", 1)
            except ValueError:
                return False
            split_comment = comment.strip().split()
            return bool(override_comment_tags.intersection(split_comment))

        for provider, pat in pats.items():
            if pat.search(string_value) and not _has_override_comment(node):
                try:
                    self._results[provider].append(node.lineno)
                except KeyError:
                    self._results[provider] = [node.lineno]

    def visit_Constant(self, node: ast.Constant):
        if isinstance(node.value, str):
            self._check_string(node.value, node)

    @classmethod
    def check_code(cls, python_code: str) -> dict[str, list[int]]:
        """Check Python code for API keys.

        Parameters
        ----------
        python_code : str
            The Python code to check for API keys.

        Returns
        -------
        results : dict[str, list[int]]
            A dictionary mapping API key providers to line numbers where API keys were found.
        """
        finder = cls(python_code.splitlines())
        finder.visit(ast.parse(python_code))
        return finder._results

    @classmethod
    def check_file(cls, py_file: str) -> dict[str, list[int]]:
        """Check a Python file for API keys.

        Parameters
        ----------
        py_file : str
            The Python file to check for API keys.

        Returns
        -------
        results : dict[str, list[int]]
            A dictionary mapping API key providers to line numbers where API keys were found.
        """
        with open(py_file) as file:
            return cls.check_code(file.read())
