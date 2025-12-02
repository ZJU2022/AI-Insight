"""
多智能体模块：包含各种专业角色的Agent
"""

from .requirement_agent import RequirementAgent
from .architect_agent import ArchitectAgent
from .coder_agent import CoderAgent
from .reviewer_agent import ReviewerAgent
from .tester_agent import TesterAgent

__all__ = [
    "RequirementAgent",
    "ArchitectAgent",
    "CoderAgent",
    "ReviewerAgent",
    "TesterAgent",
]

