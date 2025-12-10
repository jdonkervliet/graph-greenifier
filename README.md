
# Graph Greenifier

The Graph-Greenifier tool, developed by the [Massivizing Computer Systems research group](https://atlarge-research.com/) at [VU Amsterdam](https://vu.nl), uses simulation to evaluate the performance and sustainability of large-scale workloads executed on data-centre computing infrastructures.
Graph-Greenifier is available as FOSS software.
This README describes its overall design, integration with other Graph Massivizer tools, and instructions on how to deploy and use the tool.

## System Design

![architecture](docs/images/greenifier_architecture.png)

The design of Graph-Greenifier (in blue) consists of six components:

1. **Operational techniques**, encompassing all factors that influence the execution of a workload, such as scheduling algorithms or allocation policies. These allow the user to explore “what-if” scenarios to evaluate the impact of these techniques on workload performance and sustainability.
2. **Hardware information** describing the environment (i.e., data centre) on which the workload is scheduled. This information describes, for example, the number of machines in the data centre and a description of the hardware in each machine. Depending on how Graph-Greenifier is used, this information either provided  manually and directly by a user, or is provided automatically by the Graph-Choreographer tool;
3. **Workload traces**, provided by the Graph-Optimizer tool, define the workload tasks, their submission  times, their order, and performance and energy estimating models.
4. **Event-driven simulator**, based on the [OpenDC framework](https://github.com/atlarge-research/opendc), that explores multiple execution plans of a given workload on the available hardware using different (combinations of) operational techniques and scheduling policies, and predicts various metrics such as the hardware utilisation, total runtime, and energy use.
5. **Sustainability predictor**, combines the energy usage of the simulated data centers with information on the Power Grid, to create a sustainability report. This report is used by the Graph-Choreographer to make scheduling and provisioning decisions for graph-processing workloads.
6. **Sustainability report**, generated using the data centre energy use during a workload, combined with power grid information.

## Integration

Graph-Greenifier integrates with two other Graph Massivizer tools: Graph-Optimizer and Graph-Choreographer.

[Graph-Optimizer](https://github.com/graph-massivizer/graph-optimizer) provides input to Graph-Greenifier in the form of BGO workload traces along with performance and energy models.

[Graph-Choreographer](https://github.com/graph-massivizer/graph-choreographer) uses the output of Graph-Greenifier as its input. Graph-Greenifier provides simulated workload execution plans on available hardware infrastructure with performance and sustainability awareness. The Graph-Choreographer uses these execution plans to effectively schedule the workload on the real-world infrastructure.

## Deployment and Example Use

Graph-Greenifier leverages and extends the state-of-the-art OpenDC data-centre simulator. Detailed documentation on how to use this simulator is available on its [official website](https://atlarge-research.github.io/opendc/). The remainder of this section focuses on how to get started with Graph-Greenifier and OpenDC.
To deploy Graph-Greenifier, complete the following three steps:

1. Manually install Java (version 21), Python (version ≥ 3.8), and Pip.
2. Clone or download the Graph-Greenifier tool from this repository.
3. Install the remaining Python dependencies listed in requirements.txt using your preferred Python package manager.

To run Graph-Greenifier as a stand-alone tool, open the [demo](demo/demo.ipynb). You can run the demo as-is, or modify it to run custom scenarios. To run a custom scenario, you modify the system configuration, known as an _experiment_ in Graph-Greenifier terminology. The default experiment used in the demo is available in the [`demo`](demo) directory. The experiment configures the following four elements:

1. Topology which provides a hardware description of the data centre to simulate. The topology used in the demo is available under [`demo/topologies/topology.json`](demo/topologies/topology.json).
2. Carbon trace, which describes the carbon intensity of the energy provided to the data centre over time. The carbon trace is included in the topology description.
3. Workload: the (graph processing) workload to simulate. The workload used in the demo is available under [`demo/workloadTraces/greenifier/workload.json`](demo/workloadTraces/greenifier/workload.json).
4. Export models: the types of simulation models to use and output reports to produce. These are directly specified in the experiment file under [`demo/experiments/experiment.json`](demo/experiments/experiment.json).


## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE-Greenifier.txt) file for details.
