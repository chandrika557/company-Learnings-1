import requests
import psutil
import time
from agent import chat_with_llama_direct  # Import the function from agent.py

# Configuration



def get_system_metrics():
    """Fetch basic system metrics like CPU, memory, and disk usage."""
    cpu_usage = psutil.cpu_percent(interval=1)
    mem_info = psutil.virtual_memory()
    disk_usage = psutil.disk_usage('/')
    return {
        "cpu_usage": cpu_usage,
        "mem_usage": mem_info.used / 1024 ** 2,  # Convert to MB
        "disk_usage": disk_usage.percent
    }


def chat_with_llama_with_electricity_metrics(prompt):
    """Wrapper for chat_with_llama to track electricity consumption."""
    start_time = time.time()  # Record the start time
    response = chat_with_llama_direct(prompt)  # Call the original function
    end_time = time.time()  # Record the end time

    # Calculate electricity consumption
    duration = end_time - start_time  # Duration in seconds

    # Estimate power consumption (in watts)
    # This is a rough estimate; adjust based on your system's specifications
    cpu_power_draw = 50  # Average CPU power draw in watts
    electricity_consumed = (cpu_power_draw * duration)  # Convert to kWh

    print(f"Electricity consumed during processing: {electricity_consumed:.6f} kWh")

    return response


def main():
    prompt = "tell me who is the president of india in 2020, in one word"
    print("Prompt:", prompt)

    # Call the wrapped function
    response = chat_with_llama_with_electricity_metrics(prompt)
    print("Response:", response)

    # Fetch and display system metrics
    system_metrics = get_system_metrics()
    print("System Metrics:")
    for metric, value in system_metrics.items():
        print(f"{metric}: {value}")


if __name__ == "__main__":
    main()