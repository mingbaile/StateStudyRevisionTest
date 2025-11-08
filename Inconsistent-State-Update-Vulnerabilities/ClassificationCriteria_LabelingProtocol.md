# Classification criteria / Labeling protocol
## Root Causes
### Dynamic Dependent Update Omission (Omission of Update for Dynamic Operation Dependent State Variables).

In transactions involving multiple operational steps, each operation of a smart contract affects multiple state variables. Developers fail to develop a comprehensive strategy for updating state variables, resulting in the smart contract's inability to promptly update dependent state variables that reflect dynamic states after executing operations. When certain state variables remain unupdated, the contract state becomes inconsistent with the actual operations.

### Incorrect Logic Update (Conducted State Variable Update with Incorrect Logic).

When performing state variable updates, the underlying logic of the update is incorrect, causing state variables to be erroneously updated. This leads to a deviation of the contract state from the expected state.

### Variable Omission (Omission of Critical State Variables).

The contract lacks certain critical state variables, such as flags, mappings, and counters.

### Initialization/Re-initialization Omission (Omission of Initializations/Re-initializations of Critical State Variables).

Certain critical state variables in the contract lack explicit initialization or re-initialization, resulting in incomplete or erroneous state logic. Meanwhile, other related state variables have been correctly updated.

## Fix Strategies
### Direct Variable Change (Directly Modify Computations on the Unsafe State Variables). 

Directly add, remove, or modify operations on unsafe state variables, aiming to ensure the contract remains unaffected by illegal inputs or erroneous computations during execution. This typically involves promptly updating critical data variables, adding overflow protection, removing unsafe operations, or performing secure type conversions to enhance computational reliability.

### Redesign Algorithm/Data Structure. 

Developers need to re-examine the contract's core logic, adjusting data structures or algorithms to ensure proper handling of data storage, retrieval, and updates. This involves selecting appropriate data structures such as mappings, arrays, linked lists, structs, hash tables, and others to refine the logic of the original algorithm, ensuring state synchronization across different operations.

### Reorder Sequence (Reorder Function Call Sequence or State Variable Update Sequence). 

Adjust the sequence of function calls or state variable updates to ensure the contract uses the correct state information during execution.

### Change Conditions. 

Modify execution conditions to prevent or mitigate the impact of inconsistent state update vulnerabilities. This typically involves introducing or refining conditional checks in the code to ensure the consistency of state transitions and enhance logical rigor.


## Exploitation Methods
### Exploiting Numerical Calculation Errors. 
During the normal operation of a contract, critical computational processes may experience minor deviations in their results due to inconsistently updated states. Attackers first comprehend the contract logic through the contract code to locate the exact positions where calculation errors occur, and determine whether profits can be made. Then, based on data flow relationships, they identify transactions related to these calculation errors. Finally, they call functions that can enable them to illegally profit, thereby obtaining illicit gains.

### Repeated Transactions. 

Attackers repeatedly execute identical operations to exploit inconsistently updated states for undue benefits. Attackers might input identical conditions (such as the same token address or order) or repeatedly call functions like reward claims and asset transfers, leading to significant financial losses. These attacks typically involve legitimate function calls.

### Interim State Exploits.

During the transitional phase of a transaction, critical state updates have not yet been fully completed. Attackers exploit this brief window of delayed state synchronization to insert malicious operations and obtain improper profits. Typical manifestations of this exploitation method include price manipulation, front-running, and reentrancy attacks.

### Paralyzing Contract Functionality. 

Disrupt the normal logic of the contract, preventing its critical functions from operating correctly. Attackers exploit flaws where key state variables are not correctly updated after specific operations (e.g., updating administrative addresses, cross-chain message processing, etc.), and use abnormal operation sequences (such as overwriting critical state variables) or input extreme parameters to undermine the management of critical states. This causes subsequent modules relying on these state variables to fail (e.g., permission verification, message forwarding decisions, etc.) or results in permanent asset locking.
