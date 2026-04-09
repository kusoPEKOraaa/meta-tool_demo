from __future__ import annotations

import ast
from collections.abc import Iterable

from .models import Finding


def analyze_source(source: str) -> list[Finding]:
    findings = list(_line_style_findings(source))
    tree = _parse_source(source, findings)
    if tree is None:
        return findings

    analyzer = _AstAnalyzer()
    analyzer.visit(tree)
    findings.extend(analyzer.findings)
    return sorted(findings, key=_finding_sort_key)


def _finding_sort_key(finding: Finding) -> tuple[int, int]:
    severity_rank = {"high": 0, "medium": 1, "low": 2}
    return (severity_rank.get(finding.severity, 3), finding.line or 10**9)


def _parse_source(source: str, findings: list[Finding]) -> ast.AST | None:
    try:
        return ast.parse(source)
    except SyntaxError as error:
        findings.append(
            Finding(
                title="Syntax error",
                detail=error.msg,
                severity="high",
                line=error.lineno,
                category="syntax",
                recommendation="Fix the syntax error before running automated refactoring.",
            )
        )
        return None


def _line_style_findings(source: str) -> Iterable[Finding]:
    lines = source.splitlines()
    for index, line in enumerate(lines, start=1):
        if len(line) > 79:
            yield Finding(
                title="Line exceeds 79 characters",
                detail=f"Current length is {len(line)} characters.",
                severity="low",
                line=index,
                category="pep8",
                recommendation="Split the statement across multiple lines.",
            )
        if line.rstrip(" \t") != line:
            yield Finding(
                title="Trailing whitespace",
                detail="The line ends with extra spaces or tabs.",
                severity="low",
                line=index,
                category="pep8",
                recommendation="Remove the trailing whitespace.",
            )
        if "\t" in line:
            yield Finding(
                title="Tab indentation detected",
                detail="Tabs can cause inconsistent indentation across editors.",
                severity="medium",
                line=index,
                category="pep8",
                recommendation="Replace tabs with four spaces.",
            )


class _AstAnalyzer(ast.NodeVisitor):
    def __init__(self) -> None:
        self.findings: list[Finding] = []
        self._parents: dict[ast.AST, ast.AST] = {}

    def visit(self, node: ast.AST) -> None:
        for child in ast.iter_child_nodes(node):
            self._parents[child] = node
        super().visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self._check_mutable_defaults(node)
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        self._check_mutable_defaults(node)
        self.generic_visit(node)

    def visit_ExceptHandler(self, node: ast.ExceptHandler) -> None:
        if node.type is None:
            self.findings.append(
                Finding(
                    title="Bare except",
                    detail="A bare except can hide unexpected runtime errors.",
                    severity="high",
                    line=node.lineno,
                    category="bug-risk",
                    recommendation="Catch a specific exception type instead of every exception.",
                )
            )
        self.generic_visit(node)

    def visit_Compare(self, node: ast.Compare) -> None:
        for operator, comparator in zip(node.ops, node.comparators):
            if isinstance(operator, (ast.Eq, ast.NotEq)) and _is_none_literal(comparator):
                self.findings.append(
                    Finding(
                        title="Comparison to None uses == or !=",
                        detail="PEP 8 recommends identity checks for None.",
                        severity="medium",
                        line=node.lineno,
                        category="pep8",
                        recommendation="Use `is None` or `is not None`.",
                    )
                )
        self.generic_visit(node)

    def visit_While(self, node: ast.While) -> None:
        if _is_true_literal(node.test) and not any(
            isinstance(child, ast.Break) for child in ast.walk(node)
        ):
            self.findings.append(
                Finding(
                    title="Potential infinite loop",
                    detail="`while True` is used without a visible break statement.",
                    severity="high",
                    line=node.lineno,
                    category="bug-risk",
                    recommendation="Add an explicit termination condition or break path.",
                )
            )
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call) -> None:
        if isinstance(node.func, ast.Name) and node.func.id == "open" and not _inside_with(
            node, self._parents
        ):
            self.findings.append(
                Finding(
                    title="File opened outside context manager",
                    detail="The file handle may stay open if an exception occurs.",
                    severity="medium",
                    line=node.lineno,
                    category="bug-risk",
                    recommendation="Prefer `with open(...) as handle:`.",
                )
            )
        self.generic_visit(node)

    def _check_mutable_defaults(
        self, node: ast.FunctionDef | ast.AsyncFunctionDef
    ) -> None:
        defaults = node.args.defaults
        args = node.args.args[-len(defaults) :] if defaults else []
        for argument, default in zip(args, defaults):
            if isinstance(default, (ast.List, ast.Dict, ast.Set)):
                self.findings.append(
                    Finding(
                        title="Mutable default argument",
                        detail=f"Parameter `{argument.arg}` uses a mutable default value.",
                        severity="high",
                        line=default.lineno,
                        category="bug-risk",
                        recommendation="Use `None` as the default and create a new object inside the function.",
                    )
                )


def _inside_with(node: ast.AST, parents: dict[ast.AST, ast.AST]) -> bool:
    current = node
    while current in parents:
        current = parents[current]
        if isinstance(current, ast.With):
            return True
        if isinstance(
            current, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Module, ast.ClassDef)
        ):
            return False
    return False


def _is_none_literal(node: ast.AST) -> bool:
    return isinstance(node, ast.Constant) and node.value is None


def _is_true_literal(node: ast.AST) -> bool:
    return isinstance(node, ast.Constant) and node.value is True
