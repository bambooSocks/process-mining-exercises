from datetime import datetime as dt
import xml.etree.ElementTree as ETree

def read_from_file(file_path):
    tree = ETree.parse(file_path)
    root = tree.getroot()
    result = dict()

    for t in root.iter("{http://www.xes-standard.org/}trace"):
        case_id = t.find("{http://www.xes-standard.org/}string").attrib.get("value")
        result[case_id] = []
        for e in t.iter("{http://www.xes-standard.org/}event"):
            cost = 0
            concept_name = ""
            org_resource = ""
            time_timestamp = dt.now()
            for i in e.iter("{http://www.xes-standard.org/}int"):
                if i.attrib.get("key") == "cost":
                    cost = int(i.attrib.get("value"))
            for s in e.iter("{http://www.xes-standard.org/}string"):
                if s.attrib.get("key") == "org:resource":
                    org_resource = s.attrib.get("value")
                if s.attrib.get("key") == "concept:name":
                    concept_name = s.attrib.get("value")
            for d in e.iter("{http://www.xes-standard.org/}date"):
                if d.attrib.get("key") == "time:timestamp":
                    time_timestamp = dt.fromisoformat(d.attrib.get("value")).replace(tzinfo=None)
            result[case_id].append({"concept:name": concept_name, "org:resource": org_resource, "time:timestamp": time_timestamp, "cost": cost})

    return result

def dependency_graph(log):
    result = dict()
    for case_id in log.keys():
        sorted_tasks = list(map(lambda t: t["concept:name"], sorted(log[case_id], key=(lambda t: t["time:timestamp"]))))
        for i in range(len(sorted_tasks) - 1):
            try:
                result[sorted_tasks[i]][sorted_tasks[i+1]] += 1
            except KeyError:
                try:
                    result[sorted_tasks[i]]
                except KeyError:
                    result[sorted_tasks[i]] = dict()
                result[sorted_tasks[i]][sorted_tasks[i+1]] = 1
    return result