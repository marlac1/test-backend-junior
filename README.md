# Test dev Backend Junior

This is the test project for BetOnYou. You will have to complete new features in it and fix existing bugs.

## Setup

The project is build to develop under VSCode with Devcontainers.

- Fork the project
- Copy `.env.sample` to `.env` and complete it
- Open the project in VSCode
- Select run in devcontainer

You can find the API documentation on: http://0.0.0.0:8000/docs

### Outside of Dev container

- Fork the project
- Copy `.env.sample` to `.env` and complete it
- You can use Makefile task `setup_dev` to install required dev packages.
- You have to activate linter `black` for python or run format manually.
- You should use docker-compose stack to test your code.

## Scenario

BetOnYou is a play to earn application around games. As such we need to match player together through simple rules, collect their results and give or remove points. We also have to provide players with a list of awards when they collect enough points.

Another part is to provide social interaction through friends and chat system.

Due to its complexity, the matching process will not be integrated into this project.

## Goals

### Features

- We currently have a One to One conversation. We would like to create grouped conversation with the following requirements:

- - A group conversation can be named (default to None).
- - A group conversation must be created with at least 3 people.
- - People can leave conversation
- - A group conversation should be archived/closed automatically when there is only 1 person remaining.
- - People can invite others to conversation

<!-- - We added an auto resolver recently for Supercell games. We would like to modify the end of match process so people do not have any more actions to do for Supercell games but can contest their result if it is incorrect. -->

### Bugs

- There is a performance issue on production. Some request are anormaly long.
  We suspect a concurrent run issues where request are queued instead of being executed in parallel.

<!-- - There seems to be a bug in the post match statistics. Players do not have correct draws results.
- There is a bug in 1to1 messages where sometimes, a message is not correctly set as read.
- There is a bug in AFK check.
- - When both player set ready at the same time, they are locked in waiting
- - When player make leave and ready at the same time, only one action is correctly computed -->

## Tests

Test case are provided for players. You should try to implement them on socials at least for your new features.

## Some rules

* You have to fork the project on your side.
* You must not break current responses and inputs without great justification (retro compatibility issues)
* You should commit using conventional commit format: https://www.conventionalcommits.org/en/v1.0.0/