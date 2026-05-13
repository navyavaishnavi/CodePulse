import re


class ComplexityAnalyzer:

    def __init__(self, code):
        self.code = code

    def detect_loops(self):
        """
        Detects number of loops in the code
        """
        loops = re.findall(r'\b(for|while)\b', self.code)
        return len(loops)

    def detect_nested_loops(self):
        """
        Basic nested loop detection
        """
        lines = self.code.split('\n')

        indent_levels = []

        for line in lines:
            stripped = line.lstrip()

            if stripped.startswith("for") or stripped.startswith("while"):
                indent = len(line) - len(stripped)
                indent_levels.append(indent)

        nested = False

        for i in range(len(indent_levels) - 1):
            if indent_levels[i + 1] > indent_levels[i]:
                nested = True

        return nested

    def estimate_complexity(self):
        """
        Estimates Big-O complexity
        """

        loop_count = self.detect_loops()
        nested = self.detect_nested_loops()

        if loop_count == 0:
            return "O(1)"

        elif loop_count == 1:
            return "O(n)"

        elif nested:
            return "O(n²)"

        else:
            return "O(n)"

    def analyze(self):

        result = {
            "loops": self.detect_loops(),
            "nested_loops": self.detect_nested_loops(),
            "estimated_complexity": self.estimate_complexity()
        }

        return result
