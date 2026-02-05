import json
import os
import random
import csv
from utils import calculate_distance, find_nearest_agent
from report_generator import initialize_report, update_report, calculate_efficiency


# ---- Configuration ----
REPORT_FOLDER = "reports"
TEST_CASE_FOLDER = "test_cases"

os.makedirs(REPORT_FOLDER, exist_ok=True)

# Optional: reproducible randomness
random.seed(42)


# ---- Export Top Performer to CSV ----
def export_top_performer_to_csv(report, output_file):

    best_agent_id = report.get("best_agent")
    if not best_agent_id:
        return

    agent = report[best_agent_id]
    csv_file = output_file.replace(".json", "_top_agent.csv")

    with open(csv_file, mode="w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow([
            "agent_id",
            "packages_delivered",
            "total_distance",
            "total_delay_time",
            "avg_delay_time",
            "efficiency"
        ])

        writer.writerow([
            best_agent_id,
            agent["packages_delivered"],
            round(agent["total_distance"], 2),
            agent["total_delay_time"],
            agent["avg_delay_time"],
            agent["efficiency"]
        ])


# ---- Run Delivery Simulation ----
def run_simulation(input_file, output_file):

    # ---- Load Input JSON ----
    with open(input_file) as file:
        data = json.load(file)

    warehouses = data.get("warehouses", [])
    agents = data.get("agents", [])
    packages = data.get("packages", [])

    # ---- Normalize Warehouses ----
    if isinstance(warehouses, list):
        warehouse_dict = {w["id"]: w["location"] for w in warehouses}
    else:
        warehouse_dict = warehouses

    # ---- Normalize Agents ----
    if isinstance(agents, list):
        agent_list = agents
    else:
        agent_list = [{"id": aid, "location": loc} for aid, loc in agents.items()]

    if not agent_list:
        return

    # ---- Initialize Report ----
    report = initialize_report(agent_list)

    # ---- Package Delivery Loop ----
    for package in packages:

        warehouse_id = package.get("warehouse_id") or package.get("warehouse")
        destination = package.get("destination") or package.get("location")

        # ---- Validate Package ----
        if not warehouse_id or not destination:
            continue

        if warehouse_id not in warehouse_dict:
            continue

        warehouse_location = warehouse_dict[warehouse_id]

        # ---- Agent Assignment ----
        agent, dist_to_warehouse = find_nearest_agent(agent_list, warehouse_location)

        # ---- Distance Calculation ----
        dist_to_destination = calculate_distance(warehouse_location, destination)
        total_distance = dist_to_warehouse + dist_to_destination

        # ---- Simulated Time Delay ----
        delay_time = random.randint(0, 10)  # minutes

        # ---- Update Report ----
        update_report(
            report,
            agent["id"],
            total_distance,
            delay_time
        )

    # ---- Calculate Efficiency Metrics ----
    report = calculate_efficiency(report)

    # ---- Save JSON Report ----
    with open(output_file, "w") as file:
        json.dump(report, file, indent=4)

    # ---- Export Best Agent to CSV ----
    export_top_performer_to_csv(report, output_file)


# ---- Run Base Case ----
print("Running Base Case...")
run_simulation("base_case.json", os.path.join(REPORT_FOLDER, "base_case_report.json"))


# ---- Run All Test Cases ----
for filename in os.listdir(TEST_CASE_FOLDER):

    if filename.endswith(".json"):

        input_path = os.path.join(TEST_CASE_FOLDER, filename)
        output_name = filename.replace(".json", "_report.json")
        output_path = os.path.join(REPORT_FOLDER, output_name)

        print(f"Running {filename}...")
        run_simulation(input_path, output_path)

print("✅ All simulations completed!")
