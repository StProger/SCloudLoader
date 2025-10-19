import logging


class MarkdownFormatter(logging.Formatter):
    """
    Markdown formatter for telegram
    """

    FMT = """*%(levelname)s*\n_%(name)s:%(funcName)s_
    ``` %(message)s ``` %(exc)s
    """

    BLOCK_OPEN = BLOCK_CLOSE = "```"
    MODE = "markdown"


FORMATTER = MarkdownFormatter(
    """
    ```
    HIRE_AI
    ```

    **🔹 Log Details:**

    **🚨 Level:** _%(levelname)s_
    **🔧 Function:** `%(funcName)s`
    **📂 File:** `%(filename)s` Line `%(lineno)d`
    **🕒 Timestamp:** `%(asctime)s`

    **🎯 Result:**

    ```
    %(message)s
    ```
    """
)
