# Study Results on Inconsistent State Update Vulnerabilities
## Overall
To gain a deeper understanding of inconsistent state update vulnerabilities, we study 116 such vulnerabilities found across 352 real-world projects between 2021 and 2024. These vulnerability samples are collected from [Code4rena](https://code4rena.com/) competitions. For each vulnerability, we deeply analyze the source code (which is available through GitHub), code comments, bug reports, and fix suggestions of the relevant contracts to fully understand the root causes, exploitation methods and effective fix strategies.

We classify the 116 collected inconsistent state update vulnerabilities based on their root causes, exploitation methods and fix strategies, respectively.
Manual analysis shows that, based on root causes, the vulnerabilities can be classified into four categories: `Dynamic Dependent Update Omission`, `Incorrect Logic Update`, `Variable Omission`, and `Initialization/Re-initialization Omission`.
Based on exploitation methods, they can be classified into four categories: `Exploiting Numerical Calculation Errors`, `Repeated transactions`, `Interim State Exploits`, and `Paralyzing Contract Functionality`.
Based on fix strategies, they can also be classified into four categories: `Direct Variable Change`, `Redesign Algorithm/Data Structure`, `Reorder Sequence`, and `Change Conditions`.
For each category, we provide a specific definition, along with the original links, root causes, exploitation methods, and fix strategies for each vulnerability falling under that category.

Since the official Code4rena links for several specific vulnerabilities are no longer valid, we replace them with their corresponding GitHub links.
