from typing import Literal

from pydantic import BaseModel, Field


SupportedLanguage = Literal[
    "cpp",
    "python",
    "java",
    "javascript",
    "c",
    "verilog",
]


class CodeRunRequest(BaseModel):
    language: SupportedLanguage

    code: str = Field(
        ...,
        min_length=1,
        description="Source code submitted by the candidate.",
    )

    stdin: str = Field(
        default="",
        description="Custom standard input provided by the candidate.",
    )


class CodeRunResponse(BaseModel):
    status: str

    stdout: str

    stderr: str

    execution_time_ms: float | None = None

    memory_kb: float | None = None