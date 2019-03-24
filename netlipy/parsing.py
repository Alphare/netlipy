from typing import List

from dataclasses import dataclass


@dataclass
class RedirectEntry:
    source: str
    parameters: List[str]
    target: str
    status_code: int
    parameters_dict: dict = None

    def __post_init__(self):
        params_as_dict = {}

        for param in self.parameters:
            name, variable = param.split("=")
            params_as_dict[name] = variable

        self.parameters_dict = params_as_dict


class NetlipyRequestsFileParser:
    def __init__(self, file_path):
        self.file_path = file_path

        with file_path.open('r') as redirects_file:
            self.file_contents = list(redirects_file.readlines())

    def parse(self):
        entries = []
        for line in self.file_contents:
            entries.append(self.parse_single_pattern(line))
        return entries

    def parse_single_pattern(self, pattern):
        parts = pattern.split()

        if parts[-1] not in {'301', '302', '303', '404', '200'}:  # Simple permanent redirect
            parts.append(301)

        source, *parameters, target, status_code = parts
        status_code = int(status_code)

        return RedirectEntry(source=source,
                             parameters=parameters,
                             target=target,
                             status_code=status_code)
