from enum import StrEnum


class EmailSubjectRegex(StrEnum):
    OCBC = r"OCBC Bank: Your Credit Card e-Statement"
    HSBC = r"Your.HSBC.*eStatement"
