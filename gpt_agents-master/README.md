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

This repository hosts the code used in the paper, which explores how generative AI agents can model and influence market dynamics, particularly focusing on price expectations in economic systems. The research utilizes agent-based modeling and machine learning techniques to simulate interactions between AI-driven economic agents. This is built on the work of R. Maria del Rio-Chanona, Marco Pangallo, Pamela Mishkin, and Cars Hommes, as they have originally set up this codebase for their experiments. With their permissionm, I have extended their code by adding different personality and persona prompts to LLM agents, and have included functions that help with concluding the findings of the experiments such as linear regression, consolidating data across multiple experiment csv files, and other data analysis tools for graphs. 

## Directory structure

- `/src`: Contains the source code for the simulations and analysis.
- `/data`: Datasets used in the experiments.
- `/notebooks`: Jupyter notebooks with current work
- `/results`: Output from simulations and experiments.
- `/Linear Regression`: Consolidated experiment files (averages of 10 runs per experiment) are stored here for analysis for linear regression. Later on, we just create the consolidated files in each batch folder inside `/results` and just read from there. This is for the earlier attempts without creating custom tools to help with data consolidation.  

## License

This project is licensed under an Academic License. You may use the software for academic, non-commercial research, and educational purposes only. Redistribution, publication, modification, and commercial use of the software are not permitted without prior written permission from the authors.

For more information, see the LICENSE file.
