# State Variable Update Omission And State Variable Optimization Checker
To demonstrate the potential value of our findings, we design a checker to detect a specific type of problematic code, which may involve missing state variable updates or gas consumption that can be optimized. The checker is motivated by the large percentage of inconsistent state update vulnerabilities that arise due to the omission of update for dynamic operation dependent state variables.

Our observation is that when a developer declares a state variable in a smart contract, if the declaration does not use the "constant" or "immutable" modifier and the variable is never reassigned throughout the project, then it can be concluded that the update for that variable has been missed—assuming that the developer did not forget to use these two modifiers during declaration. Therefore, when the checker detects a state variable that meets the above conditions, it will issue a warning, indicating that the variable might be missing an update or may require the use of an appropriate modifier to enhance the contract's security and optimize gas consumption.

The checker is supported by [python-solidity-parser](https://www.npmjs.com/package/@solidity-parser/parser).

## How To Use the Checker
The checker supports detecting multiple projects simultaneously. Please place the smart contract projects to be detected in the `projects/` directory and run `checker.py` to perform the detection. 

The detection process requires generating AST files for all smart contract files in the `projects/` directory, and an `ASTJsonFiles/` folder will be created in the current directory to store them. The `node_modules/` directory contains some commonly used dependencies for generating AST, which we have prepared. If your contract requires additional dependencies, you will need to add them as needed. If there are too many smart contract files in the `projects/` directory, this process may take a while. 

the output will be:
```
Processing project: project1

problematic state variable: 
 ...
Declared in files:
 ...
====================================================================================================
Processing project: project2
 ...
```

## Evaluation of the Checker
We applied the checker to 208 Solidity projects on GitHub that have been updated within the past month given our evaluation time and have at least 30 stars. And it detected that 64 projects suffered from this issue for their latest versions of code. Within two weeks of submitting the issues, the owners of 23 projects responded. Our work has received positive feedback from many Solidity developers, with some describing our research as "meaningful" and others calling it a "good shout!" These results indicate that, beyond our specific findings, this proof-of-concept checker can effectively enhance the security of state variable updates in Solidity smart contracts.

Among the 23 responses, 19 confirmed the effectiveness of our tool.
| Serial number  | Link  |
|------|------|
| 1 | [Dapp-Learning-DAO/Dapp-Learning](https://github.com/Dapp-Learning-DAO/Dapp-Learning/issues/1274) |
| 2 | [Cyfrin/foundry-devops](https://github.com/Cyfrin/foundry-devops/issues/38) |
| 3 | [Cyfrin/foundry-defi-stablecoin-cu](https://github.com/Cyfrin/foundry-defi-stablecoin-cu/issues/119) |
| 4 | [devdacian/solidity-fuzzing-comparison](https://github.com/devdacian/solidity-fuzzing-comparison/issues/2) |
| 5  | [PaulRBerg/prb-contracts](https://github.com/PaulRBerg/prb-contracts/discussions/49)|
| 6  | [balancer/balancer-v3-monorepo](https://github.com/balancer/balancer-v3-monorepo/issues/1325)  |
| 7  | [Idle-Labs/idle-tranches](https://github.com/Idle-Labs/idle-tranches/issues/101#issuecomment-2651085014)  |
| 8 | [oo-00/Votium](https://github.com/oo-00/Votium/issues/3) |
| 9 | [AaronZaki/CoreVaultV2](https://github.com/AaronZaki/CoreVaultV2/issues/4) |
| 10 | [mittrorylinna/IUniswapFactory](https://github.com/mittrorylinna/IUniswapFactory/issues/2) |
| 11 | [oioi-code/GoverDue](https://github.com/oioi-code/GoverDue/issues/29) |
| 12 | [BTC415/ERC20-Token-Presale-Smart-Contract](https://github.com/BTC415/ERC20-Token-Presale-Smart-Contract/issues/5) |
| 13 | [crytic/building-secure-contracts](https://github.com/crytic/building-secure-contracts/issues/396) |
| 14 | [ethereum-optimism/superchain-ops](https://github.com/ethereum-optimism/superchain-ops/issues/684) |
| 15 | [morpho-org/bundler3](https://github.com/morpho-org/bundler3/issues/252#event-16788880275) |
| 16 | [l2beat/l2beat](https://github.com/l2beat/l2beat/issues/6978#issuecomment-2724961120) |
| 17 | [inceptionlrt/smart-contracts](https://github.com/inceptionlrt/smart-contracts/issues/130#issuecomment-2720872854) |
| 18 | [PufferFinance/puffer-contracts](https://github.com/PufferFinance/puffer-contracts/issues/104) |
| 19 | [semgrep/semgrep-rules](https://github.com/semgrep/semgrep-rules/issues/3571) |

Besides the 19 confirmed issues, there are also 4 false positives in our detection results.
| Serial number  | Link  |
|------|------|
| 1 | [ava-labs/icm-contracts](https://github.com/ava-labs/icm-contracts/issues/727) |
| 2 | [sablier-labs/lockup](https://github.com/sablier-labs/lockup/issues/1191) |
| 3 | [Ratimon/redprint-forge](https://github.com/Ratimon/redprint-forge/issues/3) |
| 4 | [ToucanProtocol/contracts](https://github.com/ToucanProtocol/contracts/issues/11) |

