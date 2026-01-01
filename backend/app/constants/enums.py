"""
Role and marking enums for RBAC and evaluation logic.
"""

from enum import Enum


class UserRole(str, Enum):
    student = "student"
    ta = "ta"
    admin = "admin"


class Marking(str, Enum):
    done = "done"
    partial = "partial"
    not_done = "not_done"
