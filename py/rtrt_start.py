import yaml
from rtrt_client import rtrt_client
import json
import re

conf = {}


def start():
    global conf
    if not conf:
        conf = get_conf()

    rtrt = rtrt_client.RtrtClient(conf)

    events = rtrt.get_events()
    events = filter_events(events)
    print(events)

    for event in events:
        process_event(rtrt, event)
    # print(json.dumps(events, indent=2, default=str))
    # print(events)


def process_event(rtrt, event):
    categories = rtrt.get_categories(event)

    event_conf = get_event_conf(event)
    pattern = event_conf['categories']

    cat_names = []
    for category in categories:
        if re.match(pattern, category['name']):
            cat_names.append(category['name'])

    for cat in cat_names:
        participants = rtrt.get_participants(event, cat)
        cat_results = []
        for participant in participants:
            results = rtrt.get_results(event, participant['pid'])
            results = format_results(participant, results)

            cat_results.append(results)

        store(event, cat, cat_results)

    pass


def store(event, cat, cat_results):
    with open("output/"+event+"_"+cat+".csv", 'a') as writer:
        writer.write("bib,team,lname,fname,country,city,gender,race,overall pos,overall total,team pos,team total,swim,swim pace,t1,bike,bike pace,t2,run,run pace,total time,status,reason\n")
        for r in cat_results:
            writer.write(",".join(r) + "\n")


def format_results(participant, results):
    splits = {}
    if not results:
        results = []
    for split in results:
        splits[split['label']] = split

    csv = [
        participant.get('bib') or "",
        participant.get('team') or "",
        participant.get('lname') or "",
        participant.get('fname') or "",
        participant.get('country') or "",
        participant.get('city') or "",
        participant.get('sex') or "",
        participant.get('race') or "",
        splits.get("Run/Finish").get("results").get("course").get("p")
                    if
                        splits and splits.get("Run/Finish") and
                        splits.get("Run/Finish").get("results") and
                        splits.get("Run/Finish").get("results").get("course") and
                        splits.get("Run/Finish").get("results").get("course").get("p")
                    else "",
        splits.get("Run/Finish").get("results").get("course").get("t")
                    if
                        splits and splits.get("Run/Finish") and
                        splits.get("Run/Finish").get("results") and
                        splits.get("Run/Finish").get("results").get("course") and
                        splits.get("Run/Finish").get("results").get("course").get("t")
                    else "",
        splits.get("Run/Finish").get("results").get("sex-team").get("p")
                    if
                        splits and splits.get("Run/Finish") and
                        splits.get("Run/Finish").get("results") and
                        splits.get("Run/Finish").get("results").get("sex-team") and
                        splits.get("Run/Finish").get("results").get("sex-team").get("p")
                    else "",
        splits.get("Run/Finish").get("results").get("sex-team").get("t")
                    if
                        splits and splits.get("Run/Finish") and
                        splits.get("Run/Finish").get("results") and
                        splits.get("Run/Finish").get("results").get("sex-team") and
                        splits.get("Run/Finish").get("results").get("sex-team").get("t")
                    else "",
        splits.get("Swim").get("splitTime") if splits.get("Swim") else "",
        splits.get("Swim").get("pace").split(' ')[0] if splits.get("Swim") and splits.get("Swim").get("pace") else "",

        splits.get("T1").get("splitTime") if splits.get("T1") else "",

        splits.get("Bike").get("splitTime") if splits.get("Bike") else "",
        splits.get("Bike").get("mph") if splits.get("Bike") else "",

        splits.get("T2").get("splitTime") if splits.get("T2") else "",

        splits.get("Run/Finish").get("splitTime") if splits.get("Run/Finish") else "",
        splits.get("Run/Finish").get("milePace") if splits.get("Run/Finish") else "",

        splits.get("Run/Finish").get("time") if splits.get("Run/Finish") else "",

    ]

    if not splits.get("Run/Finish"):
        csv.append(participant.get("pstatus") or "NS")
        csv.append(participant.get("pstatus_note") or "")

    return csv


def get_event_conf(event_name: str):
    events = conf['events']
    for event in events:
        if events[event]["name"] == event_name:
            return events[event]
    return None


def filter_events(events):
    res = []
    for conf_event in conf.get("events"):
        event = conf.get("events").get(conf_event)
        if event.get("name") in events:
            res.append(event.get("name"))

    return res


def get_conf():
    with open(get_conf_file(), 'r') as file:
        c = yaml.full_load(file)

    print(json.dumps(c, indent=2))
    return c


def get_conf_file():
    return "conf/conf.yaml"


if __name__ == "__main__":
    conf = get_conf()
    start();