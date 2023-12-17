from pathlib import Path

from commitizen.cz.base import BaseCommitizen
from commitizen.defaults import Questions

__all__ = ["PydataCz"]


class PydataCz(BaseCommitizen):
    """Commitizen for PyData-style commits.

    Use with `cz --name cz_pydata <command>`.
    """

    bump_pattern = r"^(API|BUG|DEP|ENH|NEW|REM)"
    bump_map = {
        "API": "MAJOR",
        "BUG": "PATCH",
        "DEP": "MINOR",
        "ENH": "MINOR",
        "NEW": "MINOR",
        "REM": "MINOR",
    }
    bump_map_major_version_zero = {
        "API": "MINOR",
        "BUG": "PATCH",
        "DEP": "MINOR",
        "ENH": "MINOR",
        "NEW": "MINOR",
        "REM": "MINOR",
    }

    commit_parser = r"^(?P<change_type>\w+)[:\s]*(?P<message>.*)"
    changelog_pattern = r"^(API|BUG|DEP|ENH|NEW|REM)"
    change_type_map = {
        "API": "BREAKING CHANGES",
        "BUG": "Fixed",
        "DEP": "Deprecated",
        "ENH": "Changed",
        "NEW": "Added",
        "REM": "Removed",
    }
    change_type_order = [
        "BREAKING CHANGES",
        "Added",
        "Changed",
        "Deprecated",
        "Removed",
        "Fixed",
    ]

    def questions(self) -> Questions:
        """Questions regarding the commit message.

        Used by `cz commit`.
        """
        questions: Questions = [
            {
                "name": "acronym",
                "type": "list",
                "message": "Select the type of change",
                "choices": [
                    {"value": "API", "name": "breaking change"},
                    {"value": "BUG", "name": "bug fix"},
                    {"value": "DEP", "name": "deprecate a feature"},
                    {"value": "ENH", "name": "improve a feature"},
                    {"value": "NEW", "name": "add a new feature"},
                    {"value": "REM", "name": "remove a feature"},
                ],
            },
            {
                "name": "summary",
                "type": "input",
                "message": "Provide a summary of the change",
            },
            {
                "name": "description",
                "type": "input",
                "message": "Provide a description of the change (press [enter] to skip)",
            },
        ]

        return questions

    def message(self, answers: dict) -> str:
        """Generate the commit message based on the answers.

        Used by `cz commit`.
        """
        message = "{acronym}: {summary}".format(**answers)

        if description := answers.get("description", None):
            message = f"{message}\n\n{description}"

        return message

    def example(self) -> str:
        """Show an example of the commit message.

        Used by `cz example`.
        """
        return "\n\n".join(["BUG: Fix regression in some feature", "Closes: #3456"])

    def schema(self) -> str:
        """Show the schema for the commit message.

        Used by `cz schema`.
        """
        return "\n".join(["<acronym>: <summary>", "<BLANK LINE>", "<description>"])

    def info(self) -> str:
        """Show a detailed explanation of the commit rules.

        Used by `cz info`.
        """
        info_path = next(Path(__file__).parent.glob("*info.txt"))

        return info_path.read_text()
