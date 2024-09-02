import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def getMeanUtilization(df_host):
    return df_host.cpu_utilization.mean()

def getTotalEnergyUsage(df_host, unit="joule"):
    if unit == "joule":
        return df_host.energy_usage.sum()
    if unit == "kWh":
        return df_host.energy_usage.sum() / 3_600_000
    
    raise ValueError(f"incorrect unit: {unit}. Allowed units are joule and kWh")

def getTotalCarbonEmissions(df_host, unit="kg"):
    if unit == "kg":
        return df_host.energy_usage.sum() * 1000
    if unit == "g":
        return df_host["carbon_emission"].sum()
    
    raise ValueError(f"incorrect unit: {unit}. Allowed units are joule and kWh")

def getTotalRuntime(df_service):
    return pd.to_timedelta(df_service.timestamp.max() - df_service.timestamp.min(), unit="ms")

def getMeanWaitTime(df_server):
    waitTimes = []

    for server_name, series in df_server.groupby("server_name"):
        waitTimes.append(series.host_id.isnull().sum()*300_000)

    return pd.to_timedelta(np.mean(waitTimes), unit="ms")


def plotService(df_service, column, label=""):
    plt.plot(df_service["timestamp"]/1000/60/60, df_service[column], label=label)
    plt.xlabel("Timestamp (h)")
    plt.ylabel(f"{column}")
    plt.legend()

def plotHosts(df_host, column, aggregation_method, label, window_size=1000):
    if aggregation_method not in ["mean", "sum"]:
        raise ValueError(f"incorrect aggregation method provided: {aggregation_method}, please pick on of [mean, sum]")

    df_agg = df_host.groupby("timestamp")[[column]].agg(aggregation_method)

    plt.plot(df_agg.index/1000/60/60, df_agg.rolling(window_size, min_periods=1).mean(), label=label)
    plt.xlabel("timestamp (h)")
    plt.ylabel(column)

    plt.legend()

def plotWaitTimesHist(df_server, label):
    waitTimes = []

    for server_name, series in df_server.groupby("server_name"):
        waitTimes.append(series.host_id.isnull().sum()*300_000/1000/60/60)

    plt.hist(waitTimes, alpha=0.8, label=label)
    plt.legend()
    plt.xlabel("wait time (h)")
    plt.ylabel("frequency")


def get_task_info(df_host, df_service, df_server, task_name):
    print(f"{task_name = }")

    # Get their starting time
    df_server_task = df_server[df_server.server_name == task_name]

    print(f"{df_server_task = }")

    # filter to when the task has a host
    df_server_task_with_host = df_server_task[df_server_task.host_id.notnull()]

    # Get the row with the first timestamp
    first_row = df_server_task_with_host[df_server_task_with_host.timestamp == df_server_task_with_host.timestamp.min()]

    print(f"{first_row = }")
    # Get host the task is run on
    host_id = first_row["host_id"].item()
    host_name = df_host[df_host.host_id == host_id]["host_name"].iloc[0]

    # Get their run time of task
    start_time = (first_row["timestamp"] - first_row["uptime"]).item()
    end_time = df_server_task_with_host["timestamp"].max()
    run_time = end_time - start_time


    return {"host": host_name, "start_time": start_time, "finish_time": end_time, "run_time": run_time}

def get_output(df_host, df_service, df_server, save=False, exportName=""):

    output = {"BGOs": {}}

    # Get task names
    task_names = list(df_server.server_name.unique())


    for task_name in task_names:
        output["BGOs"][task_name] = get_task_info(df_host, df_service, df_server, task_name)


    output["total_runtime"] = df_service["timestamp"].max()

    output["total_energy"] = (df_host["energy_usage"].sum() / 3_600_000).round(2)

    output["total_carbon"] = (df_host["carbon_emission"].sum() / 1000).round(2)

    if save:
        import json 
        with open(exportName, "w") as wf:
            json.dump(output, wf, indent = 4, default=str) 

    return output