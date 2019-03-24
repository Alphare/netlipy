from collections import defaultdict

from flask import Flask
from pathlib import Path

from dataclasses import dataclass

from netlipy.parsing import NetlipyRequestsFileParser, RedirectEntry
from netlipy.request import NetlipyGenericView


@dataclass
class Netlipy:
    root_dir: Path
    host: str = '0.0.0.0'
    port: int = 8000

    def __post_init__(self):
        self.root_dir = self.root_dir.absolute()
        self.app = Flask(__name__, static_url_path='', static_folder=self.root_dir)
        mapped_urls = self.group_entries_by_path()

        for source, entries_mapping in mapped_urls.items():
            view = NetlipyGenericView(source=source, redirect_entries=entries_mapping)
            self.app.add_url_rule(source, view_func=view)

        self.app.register_error_handler(404, lambda e: self.app.send_static_file('404.html'))

    def group_entries_by_path(self):
        urls = NetlipyRequestsFileParser(self.root_dir / '_redirects').parse()

        mapped_urls = defaultdict(dict)
        mapped_urls['/'] = {
            (): RedirectEntry(source='/', parameters=[], target='index.html', status_code=200)
        }

        for url in urls:
            parameters_tuple = tuple(sorted(url.parameters_dict))
            mapped_urls[url.source][parameters_tuple] = url

        return mapped_urls

    def serve(self):
        self.app.run(host=self.host, port=self.port, debug=True)