# System Blueprint (_a.k.a._ "Design Doc")

## TNPG: BATMood
## Project: BATMood Games
## Target ship date: 2026-06-14

#### Roster:


| Name | Email | Primary Role | Secondary Role |
|---|---|---|---|
| Thamidur Rahman | thamidurr@nycstudents.net | PM | Frontend Devo |
| Alvin Sze | alvins44@nycstudents.net | Database Devo | Backend Devo |
| Bogdan Sotnikov | bogdans2789@nycstudents.net | Backend Devo | Frontend Devo |
| Matthew Ciu | matthewc691@nycstudents.net | Frontend Devo | Database Devo |

---


# Summary
Inspired by Jackbox Games Party Packs, our site allows users to play party games together. They will be mostly word based where players submit words independently and react to other players' submissions. Lobbies will be entered using a code, like Kahoot.

## Problem Being Solved
Lack of entertainment and bad vibes.

## Target Users

Who will use this system?

- Friends that want to have a quick, free way to play short party games.
- People who want to store game stats.

<br>

## Why This Project Matters

It will be fun!


# Minimum Viable Product (MVP) Scope

## Core Features (Required for Final Submission)
Features that **must** be completed

1. User accounts to track wins and losses.
2. Lobbies that authorize player to join if they are part of the game.
3. One game, beginning with Imposter. 

## Stretch Features (Only if MVP is Complete)
1. Up to four games. 
2. Player profile customization.
3. Game joining without an account

## Explicit Non-Goals
Features intentionally excluded:
- Bugs.
- There will be a player limit that may be editted.


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


| Team Member | Primary Ownership | Secondary Ownership | Specific Deliverables |
|---|---|---|---|
| Thamidur Rahman | Flask App | CSS | CSS for login and register. |
| Alvin Sze | Database | Game Script | Database to store player info and authenticate.  Javascript for websockets.|
| Bogdan Sotnikov | Flask App | Database | System to house multiple links for different lobbies. |
| Matthew Ciu | CSS | HTML | CSS for homepage.|

---

# Component map
<img width="973" height="506" alt="Screenshot 2026-06-14 225857" src="https://github.com/user-attachments/assets/77adeca0-011c-4a94-81ab-fbe6e4dc41b7" />


# Site map
<img width="357" height="739" alt="Screenshot 2026-06-14 225156" src="https://github.com/user-attachments/assets/630581f6-20f6-4504-a930-ea1a7596d065" />


## Key User Stories

At a party I want a site that allows me to quickly host a game that anyone with internet connection can join easily.

As a player I want to compete with others, see how others perform, and see how they've performed in the past.  


# Database Design

| PLAYER DB | TYPE | |
|---|---|---|
| player | TEXT |PK |
| password | TEXT | |
| wins | INT | |
| losses | INT | |

| SERVER DB | TYPE | |
|---|---|---|
| serverID | TEXT |PK |
| gameID | TEXT | |
| gameID | INT | |
| player1 | TEXT | |
| player2 | TEXT | |
| player3 | TEXT | |
| player4 | TEXT | |
| category | TEXT | |
| word | TEXT | |
| firstPlayer | int | |
| specialPlayer | TEXT | |


# Testing Plan
We will be sure to test that only authorized users can enter in specific links.

# Timeline
## Week 1 Goals: Smooth database updates within a game.
## Week 2 Goals: Player authorization and splitting of lobbies to different routes.
## Week 3 Goals: Javascript for websockets and dynamic updates.
## Internal Deadlines: Front end for each part.


# Completion Criteria (_a.k.a._ "Definition of 'Done'")
Project is considered complete when all of the following are true:
1. Players can authorize joining into a lobby.
2. Games can continue and end with player input without issues.
3. Wins and losses are tracked onto player profiles which can be displayed.

# Open Questions

# Appendix
Current inspirations: Jackbox, Imposter, Tapple.

# Other
We love this assignment (considerably less)!
