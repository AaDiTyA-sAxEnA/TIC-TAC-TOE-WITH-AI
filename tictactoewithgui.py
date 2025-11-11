#!/usr/bin/env python3
"""
Tic Tac Toe with Pygame GUI + Unbeatable AI + Win Probability display.
"""

import pygame
import sys
from typing import List, Optional, Tuple

# ---------- Game Logic ----------

EMPTY = " "
HUMAN = "X"
AI = "O"

WIN_LINES = [
    (0,1,2),(3,4,5),(6,7,8),
    (0,3,6),(1,4,7),(2,5,8),
    (0,4,8),(2,4,6)
]

def available_moves(board: List[str]) -> List[int]:
    return [i for i,v in enumerate(board) if v == EMPTY]

def winner(board: List[str]) -> Optional[str]:
    for a,b,c in WIN_LINES:
        if board[a] == board[b] == board[c] != EMPTY:
            return board[a]
    if EMPTY not in board:
        return "Draw"
    return None

def score_for(player: str, result: Optional[str]) -> int:
    if result == "Draw" or result is None:
        return 0
    return 1 if result == player else -1

def minimax(board: List[str], player: str, maximizing: bool,
            alpha: int, beta: int) -> Tuple[int, Optional[int]]:
    w = winner(board)
    if w is not None:
        return score_for(AI, w), None

    best_move = None
    if maximizing:
        max_eval = -999
        for m in available_moves(board):
            board[m] = player
            eval_score, _ = minimax(board, HUMAN if player == AI else AI, False, alpha, beta)
            board[m] = EMPTY
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = m
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = 999
        for m in available_moves(board):
            board[m] = player
            eval_score, _ = minimax(board, HUMAN if player == AI else AI, True, alpha, beta)
            board[m] = EMPTY
            if eval_score < min_eval:
                min_eval = eval_score
                best_move = m
            beta = min(beta, eval_score)
            if beta <= alpha:
                break
        return min_eval, best_move

def ai_move(board: List[str]) -> Tuple[int, float]:
    """Returns AI move and win probability."""
    moves = available_moves(board)
    outcomes = []
    for m in moves:
        board[m] = AI
        score, _ = minimax(board, HUMAN, False, -999, 999)
        board[m] = EMPTY
        outcomes.append(score)
    total = len(outcomes)
    wins = outcomes.count(1)
    draws = outcomes.count(0)
    prob = (wins + 0.5*draws) / total if total else 0
    best_score = max(outcomes)
    best_index = outcomes.index(best_score)
    return moves[best_index], prob

# ---------- Pygame GUI ----------

pygame.init()
WIDTH, HEIGHT = 400, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe AI")

FONT = pygame.font.SysFont("arial", 48)
SMALL = pygame.font.SysFont("arial", 28)
LINE_COLOR = (50,50,50)
BG_COLOR = (230,230,230)

def draw_board(board: List[str], prob: Optional[float], message: str):
    WIN.fill(BG_COLOR)
    # grid
    for i in range(1,3):
        pygame.draw.line(WIN, LINE_COLOR, (0, i*WIDTH/3), (WIDTH, i*WIDTH/3), 4)
        pygame.draw.line(WIN, LINE_COLOR, (i*WIDTH/3, 0), (i*WIDTH/3, WIDTH), 4)

    # symbols
    for i,v in enumerate(board):
        if v != EMPTY:
            x = (i % 3) * WIDTH/3 + WIDTH/6
            y = (i // 3) * WIDTH/3 + WIDTH/6
            text = FONT.render(v, True, (0,0,0))
            rect = text.get_rect(center=(x,y))
            WIN.blit(text, rect)

    # probability bar
    if prob is not None:
        pygame.draw.rect(WIN, (200,200,200), (50,420,300,25))
        pygame.draw.rect(WIN, (100,200,100), (50,420,int(300*prob),25))
        prob_text = SMALL.render(f"AI Win Probability: {prob*100:.1f}%", True, (0,0,0))
        WIN.blit(prob_text, (50,390))
    else:
        WIN.blit(SMALL.render(message, True, (0,0,0)), (50,390))

    pygame.display.update()

def main():
    board = [EMPTY]*9
    current = HUMAN
    running = True
    result = None
    ai_prob = None
    message = "Your Turn"

    while running:
        draw_board(board, ai_prob, message)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if result:
                continue

            if current == HUMAN and event.type == pygame.MOUSEBUTTONDOWN:
                x,y = pygame.mouse.get_pos()
                col = int(x // (WIDTH/3))
                row = int(y // (WIDTH/3))
                idx = row*3 + col
                if idx in available_moves(board):
                    board[idx] = HUMAN
                    current = AI
                    ai_prob = None

        if not result and current == AI:
            pygame.time.wait(500)
            move, prob = ai_move(board)
            board[move] = AI
            ai_prob = prob
            current = HUMAN

        result = winner(board)
        if result:
            draw_board(board, ai_prob, f"{result} wins!" if result!="Draw" else "Draw")
            pygame.time.wait(2000)
            board = [EMPTY]*9
            result = None
            ai_prob = None
            current = HUMAN
            message = "Your Turn"

if __name__ == "__main__":
    main()
