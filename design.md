# System Blueprint (_a.k.a._ "Design Doc")

## TNPG: BATMood
## project: BATMood Games
## Target ship date: 2026-06-08

#### roster:


| Name | Email | Primary Role | Secondary Role |
|---|---|---|---|
| Thamidur Rahman | thamidurr@nycstudents.net | PM | Frontend Devo |
| Alvin Sze | alvins44@nycstudents.net | Database Devo | Backend Devo |
| Bogdan Sotnikov | bogdans2789@nycstudents.net | Backend Devo | Frontend Devo |
| Matthew Ciu | matthewc691@nycstudents.net | Frontend Devo | Database Devo |

---


# Summary
Inspired by Jackbox Games Party Packs, our site allows users to play party games together. 

## Problem Being Solved
Lack of entertainment and bad vibes.

## Target Users

Who will use this system?

- Friends that want to have a quick, free way to play short party games.
- People who want to store game stats.


## Why This Project Matters

It will be fun!


# Minimum Viable Product (MVP) Scope

## Core Features (Required for Final Submission)
Features that **must** be completed

1. User accounts to track wins and losses.
2. Lobbies that authorize player to join if they are part of the game.
3. One game.

## Stretch Features (Only if MVP is Complete)
1. Up to four games. 
2. Player profile customization.
3. Game joining without an account

## Explicit Non-Goals
Features intentionally excluded:
- Bugs.


---

# Technology Stack

| Layer | Selected Tool |
|---|---|
| Backend Framework | Flask |
| Frontend Framework | Bootstrap |
| Database | SQLite |
| Authentication | Flask sessions |

## Why This Stack Was Chosen
Our team prefers the ease of use and aesthetic possibilities of Bootstrap and we have experience with it on multiple projects. SQLite seems relatively cleaner to use with Flask and we have all used it extensively.

# Team Ownership Plan

Each member must own meaningful deliverables. 

| Team Member | Primary Ownership | Secondary Ownership | Specific Deliverables |
|---|---|---|---|
| Thamidur Rahman | Flask App | Game Script | Plan for unique game and how it will be implemented. |
| Alvin Sze | Database | Game Script | Database to store player info and authenticate. |
| Bogdan Sotnikov | Flask App | JS | System to house multiple links for different lobbies. |
| Matthew Ciu | CSS | HTML | |

---

# Component map

<img width="975" height="460" alt="image" src="https://github.com/user-attachments/assets/0b7da6ab-8032-41ff-9c92-0693bb751d0c" />


# Site map

<img width="349" height="711" alt="image" src="https://github.com/user-attachments/assets/6820bffe-f7d8-467e-ac43-05884ad7444d" />


## Key User Stories

At a party I want a site that allows me to quickly host a game that anyone with internet connection can join easily.

As a player I want to compete with others, see how others perform, and see how they've performed in the past. 



# Database Design

| player | String |PK |
|---|---|---|
| password | String | |
| wins | int | |
| losses | int | |

| serverID | String |PK |
|---|---|---|
| password | String | |
| gameID | int | |
| player1 | String | |
| player2 | String | |
| player3 | String | |
| player4 | String | |
| player5 | String | |
| player6 | String | |


# Testing Plan
We will be sure to test that only authorized users can enter in specific links.

# Timeline
## Week 1 Goals: Smooth database updates within a game.
## Week 2 Goals: Player authorization and splitting of games to different domains.
## Week 3 Goals: Creating rules and displaying games.
## Internal Deadlines: Front end for each part.


# Completion Criteria (_a.k.a._ "Definition of 'Done'")
Project is considered complete when all of the following are true:
1. Players can authorize joining into a lobby.
2. Games can continue and end with player input without issues.
3. Wins and losses are tracked onto player profiles which can be displayed.

# Open Questions
We are unsure if all games will be of our own design.

# Appendix
Current inspirations: Jackbox, Imposter, Tapple, 

# Other
We love this assignment!

