# Does LLM agents have the capacity to simulate heterogeneous human behaviour in market scenarios? 

This directory contains the code associated with the paper:

**Evalauting the Feasibility of Large Language Models in Agent-Based Models**

Authors:
- R. Maria del Rio-Chanona\* (University College London, Bennett Institute for Public Policy, University of Cambridge)
- Marco Pangallo\* (CENTAI)
- Pamela Mishkin (OpenAI)
- Cars Hommes (Bank of Canada, University of Amsterdam)

\*Equal contribution
Market dynamics of price expectations with Generative AI agents

## Description

This repository hosts the code used in the paper, which explores how generative AI agents can model and influence market dynamics, particularly focusing on price expectations in economic systems. The research utilizes agent-based modeling and machine learning techniques to simulate interactions between AI-driven economic agents. This project extends the foundational codebase developed by R. Maria del Rio-Chanona, Marco Pangallo, Pamela Mishkin, and Cars Hommes, whose pioneering work established the experimental framework for modeling expectations and price dynamics in economic systems. With their permission, I have significantly expanded upon this framework by incorporating a diverse set of personality and persona-driven prompts for LLM-based agents. In addition, I have developed new functionalities to support the analysis and synthesis of simulation results, including tools for linear regression, cross-experiment data consolidation from CSV files, and a suite of other utilities. These enhancements aim to deepen the investigation into how generative AI agents with heterogeneous characteristics can shape collective market behaviour through expectations.
## Directory structure

- `/src`: Contains the source code for the simulations and analysis.
- `/data`: Datasets used in the experiments.
- `/notebooks`: Jupyter notebooks with current work
- `/results`: Output from simulations and experiments.
- `/Linear Regression`: This folder contains consolidated experiment files, each representing the average results of 10 runs per experiment. These files were originally created to support linear regression analysis during early stages of the project, prior to the development of custom tools for automated data consolidation. In the current workflow, consolidated files are now generated directly within each batch folder under /results, making this directory primarily a legacy structure retained for reference.

## License

This project is licensed under an Academic License. You may use the software for academic, non-commercial research, and educational purposes only. Redistribution, publication, modification, and commercial use of the software are not permitted without prior written permission from the authors.

For more information, see the LICENSE file.
