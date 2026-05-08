# System Blueprint (_a.k.a._ "Design Doc")

## TNPG: BATMood
## project: BATMood Games
## Target ship date: {2026-06-xx}

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
Entertainment

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
My team prefers the ease of use and aesthetic of Bootstrap and we have experience with it on multiple projects. SQLite seems relatively cleaner to use with Flask and we have all used it extensively.

# Team Ownership Plan

Each member must own meaningful deliverables. 

| Team Member | Primary Ownership | Secondary Ownership | Specific Deliverables |
|---|---|---|---|
| Thamidur Rahman | Flask App | | |
| Alvin Sze | Database | Flask App | |
| Bogdan Sotnikov | | | |
| Matthew Ciu | | | |

---

# Component map

{Insert your mermaid(or equivalent)-generated diagram here}

# Site map

{Insert your mermaid(or equivalent)-generated diagram here}
eg...

## Key User Stories
### eg0
As a __________, I want to __________ so that...

### eg1
As a __________, I want to __________ so that...

### eg2
As a __________, I want to __________ so that...



# Database Design

{Insert your table/document organizational structure here}


# Testing Plan
{Delineate here your plan for testing each component}

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
{Delineate anything undecided here}

# Appendix
{Any relevant info that is useful but would have interrupted narrative flow above, or cluttered the information portrayed}

# Other
{Put here anything that did not sensibly fit under above headings. This section will inform evolution of SoftDev.}

