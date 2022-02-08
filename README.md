# Test dev Backend Junior

This is the test project for BetOnYou. You will have to complete new features in it and fix existing bugs.

## Setup

The project is build to develop under VSCode with Devcontainers.

- Fork the project
- Open it in VSCode
- Select run in devcontainer

## Scenario

BetOnYou is a play to earn application arround over games. As such we need to match player together through simple rules, collect their results and give or remove points. We also have to provide players with a list of awards when they collect enougth point.

Another part is to provide social interraction through friends and chat system.

Due to its complexity, the matching process will not be integrated to this project.

## Goals

### Features

- We currently have One to One conversation. We would like to create grouped conversation with the following requirements:
  * A group conversation can be named (default to None).
  * A group conversation must be created with at least 3 peoples.
  * People can leave conversation
  * A group conversation should be archived/closed automatically when there are only 1 person remaining.
  * People can invite others to conversation

- We added an auto resolver recently for Supercell games. We would like to modify the end of match process so people do not have any more actions to do for Supercell games but can contest there result if it is incorrect. 

### Bugs

- There seems to be a bug on the post match statistics. Player to not have correct draws results. 
- There is a bug in 1to1 messages where sometimes, a message is not correctly set as read.
- There is a bug in AFK check. When players act at the same time, the process only take one action at time.

