import pm4py

class importer:
    def read_xes(self, xes_file_path):
        log = pm4py.read_xes(xes_file_path)
        event_log = []
        for trace in log:
            t = []
            for event in trace:
                if event.get('lifecycle:transition') == 'complete' or event.get('lifecycle:transition') is None:
                    t.append(event.get('concept:name'))
            event_log.append(t)
        return event_log
