def initialize_report(agents):

    report = {}

    for agent in agents:
        report[agent["id"]] = {
            "packages_delivered": 0,
            "total_distance": 0.0,
            "total_delay_time": 0
        }

    return report


def update_report(report, agent_id, distance, delay_time):

    report[agent_id]["packages_delivered"] += 1
    report[agent_id]["total_distance"] += distance
    report[agent_id]["total_delay_time"] += delay_time


def calculate_efficiency(report):

    best_agent = None
    best_efficiency = float("inf")

    for agent_id in report:

        delivered = report[agent_id]["packages_delivered"]
        total_distance = report[agent_id]["total_distance"]
        total_delay = report[agent_id]["total_delay_time"]

        efficiency = total_distance / delivered if delivered > 0 else 0
        avg_delay = total_delay / delivered if delivered > 0 else 0

        report[agent_id]["efficiency"] = round(efficiency, 2)
        report[agent_id]["avg_delay_time"] = round(avg_delay, 2)

        if delivered > 0 and efficiency < best_efficiency:
            best_efficiency = efficiency
            best_agent = agent_id

    report["best_agent"] = best_agent

    return report
