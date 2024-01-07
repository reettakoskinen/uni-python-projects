# Battleship Game

## Introduction
Battleship is a classic strategy game where the player aims to sink the enemy fleet by guessing the locations of ships on a grid. This Python implementation allows you to play the game by entering coordinates to shoot at the enemy fleet.

## Game Rules
1. **Game Board:** The game board is a 10x10 grid represented by letters (A-J) for columns and numbers (0-9) for rows.

2. **Ships:** The game features different types of ships with varying lengths: Carrier (5 cells), Battleship (4 cells), Cruiser (3 cells), Submarine (3 cells), and Destroyer (2 cells).

3. **Gameplay:** 
   - Enter coordinates (e.g., A3) to shoot at the enemy fleet.
   - The game board will be updated to show hits (X) and misses (*).
   - Sink all enemy ships to win the game.

## Starting Board
The starting board is an empty 10x10 grid with labeled columns (A-J) and rows (0-9). Ships are placed on the grid based on the coordinates provided in the input file.

## Input File
- You can specify ship types and coordinates by creating a text file.
- Each line in the file should contain ship type and coordinates separated by semicolons (e.g., "Carrier;A1;A2;A3;A4;A5").
- Ensure valid ship coordinates (e.g., A0 is invalid).
