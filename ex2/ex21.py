from datetime import datetime as dt

def log_as_dictionary(csv_file):
    result = dict()

    for line in filter(lambda s: s != "", csv_file.split('\n')):
        split_data = line.split(";")
        case_id = split_data[1]
        sub_dict = dict()
        sub_dict["task_id"] = split_data[0]
        sub_dict["user_id"] = split_data[2]
        sub_dict["timestamp"] = dt.strptime(split_data[3], "%Y-%m-%d %H:%M:%S").timestamp()
        try:
            result[case_id].append(sub_dict)
        except KeyError:
            result[case_id] = [sub_dict]
    return result


def dependency_graph(log):
    result = dict()
    for case_id in log.keys():
        sorted_tasks = list(map(lambda t: t["task_id"], sorted(log[case_id], key=(lambda t: t["timestamp"]))))
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