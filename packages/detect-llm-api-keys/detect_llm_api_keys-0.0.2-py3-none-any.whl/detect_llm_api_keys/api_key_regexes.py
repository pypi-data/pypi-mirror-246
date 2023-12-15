import re

pats: dict[str, re.Pattern] = {
    "anthropic": re.compile(r"^sk-ant-api\d{2}-[a-zA-Z0-9_\-]{95}$"),
    "anyscale": re.compile(r"^secret_[a-zA-Z0-9]{26}$"),
    "azure": re.compile(r"^[a-zA-Z0-9]{32}$"),
    "langchain": re.compile(r"^ls__[a-zA-Z0-9]{32}$"),
    "openai": re.compile(r"^sk-[a-zA-Z0-9]{48}$"),
    "mistral": re.compile(r"^[a-zA-Z0-9]{32}$"),
}
