from flask import request, redirect, current_app


class NetlipyGenericView:
    def __init__(self, source, redirect_entries):
        self.source = source
        self.entries = redirect_entries
        self.__name__ = source

    def apply_query_parameters(self, entry, query_args, target):
        for arg, value in query_args.items():
            variable = entry.parameters_dict.get(arg)
            if variable:
                target = target.replace(variable, value)
        return target

    def get_target_file(self, entry):
        target = entry.target

        query_args = request.args

        if len(query_args):
            target = self.apply_query_parameters(entry, query_args, target)

        return target

    def __call__(self):
        entry = self.get_entry()
        target = self.get_target_file(entry)

        if entry.status_code == 200:
            if target.startswith('/'):
                target = target[1:]
            return current_app.send_static_file(target)

        return redirect(location=target, code=entry.status_code)

    def get_entry(self):
        return self.entries.get(tuple(sorted(request.args)), self.entries[()])
