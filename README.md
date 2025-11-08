# Understanding Inconsistent State Update Vulnerabilities in Smart Contracts
## What is this repository?
The execution logic of a smart contract is closely related to the contract state, and thus the correct and safe execution of the contract depends heavily on the precise control and update of the contract state. However, the contract state update process can have issues. In particular, inconsistent state update issues can arise for reasons such as unsynchronized modifications. Inconsistent state update vulnerabilities have been exploited by attackers many times, but existing detection tools still have difficulty in effectively identifying them. This paper conducts the first large-scale empirical study about inconsistent state update vulnerabilities in smart contracts, aiming to shed light for developers, researchers, tool builders, and language or library designers in order to avoid inconsistent state update vulnerabilities. We systematically investigate 116 inconsistent state update vulnerabilities in 352 real-world smart contract projects, summarizing their root causes, fix strategies, and exploitation methods. Our study provides 11 original and important findings, and we also give the implications of our findings. To illustrate the potential benefits of our research, we also develop a proof-of-concept checker based on one of our findings. The checker effectively detects issues in 64 popular GitHub projects, and 19 project owners have confirmed the detected issues.

## Structure of this repository
The repository contains three folders: Inconsistent-State-Update-Vulnerabilities, State-Checker and Scripts.

- [Inconsistent-State-Update-Vulnerabilities](./Inconsistent-State-Update-Vulnerabilities) contains 116 real-world inconsistent state update vulnerabilities, along with our manual analysis of their root causes, fix strategies, and exploitation methods.
- [State-Checker](./State-Checker) contains the source code for the tool and the instructions on how to use the tool.
- [Scripts](./Scripts) contains the scripts used for generating certain data in the paper.

Inside each folder, we give more detailed descriptions of the content it contains.
