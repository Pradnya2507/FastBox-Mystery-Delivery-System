import math

def calculate_distance(p1, p2):
    return math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)


def find_nearest_agent(agents, warehouse_location):

    min_distance = float("inf")
    nearest_agent = None

    for agent in agents:
        dist = calculate_distance(agent["location"], warehouse_location)

        if dist < min_distance:
            min_distance = dist
            nearest_agent = agent

    return nearest_agent, min_distance
