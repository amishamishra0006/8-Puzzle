import tkinter as tk
import random
import heapq
import time

# Goal State
GOAL = [[1,2,3],
        [4,5,6],
        [7,8,0]]

class Puzzle:
    def __init__(self, root):
        self.root = root
        self.root.title("8 Puzzle Game - AI Project")
        self.board = [[1,2,3],[4,5,6],[7,8,0]]
        self.buttons = []
        self.moves = 0

        self.create_board()
        self.create_controls()
        self.update_board()

    def create_board(self):
        for i in range(3):
            row = []
            for j in range(3):
                btn = tk.Button(self.root, text="", font=("Arial", 20),
                                width=4, height=2,
                                command=lambda r=i, c=j: self.move(r,c))
                btn.grid(row=i, column=j)
                row.append(btn)
            self.buttons.append(row)

    def create_controls(self):
        tk.Button(self.root, text="Shuffle", command=self.shuffle).grid(row=3, column=0)
        tk.Button(self.root, text="Solve (AI)", command=self.solve).grid(row=3, column=1)
        self.label = tk.Label(self.root, text="Moves: 0")
        self.label.grid(row=3, column=2)

    def update_board(self):
        for i in range(3):
            for j in range(3):
                value = self.board[i][j]
                self.buttons[i][j]["text"] = "" if value == 0 else str(value)

    def find_blank(self):
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == 0:
                    return i,j

    def move(self, r, c):
        br, bc = self.find_blank()
        if abs(br-r)+abs(bc-c) == 1:
            self.board[br][bc], self.board[r][c] = self.board[r][c], self.board[br][bc]
            self.moves += 1
            self.label.config(text=f"Moves: {self.moves}")
            self.update_board()
            if self.board == GOAL:
                self.label.config(text="You Won! 🎉")

    def shuffle(self):
        nums = list(range(9))
        random.shuffle(nums)
        self.board = [nums[i:i+3] for i in range(0,9,3)]
        self.moves = 0
        self.label.config(text="Moves: 0")
        self.update_board()

    # -------- AI PART (A*) --------
    def heuristic(self, state):
        distance = 0
        for i in range(3):
            for j in range(3):
                if state[i][j] != 0:
                    x = (state[i][j]-1)//3
                    y = (state[i][j]-1)%3
                    distance += abs(x-i)+abs(y-j)
        return distance

    def get_neighbors(self, state):
        neighbors = []
        for i in range(3):
            for j in range(3):
                if state[i][j] == 0:
                    x,y = i,j

        moves = [(-1,0),(1,0),(0,-1),(0,1)]
        for dx,dy in moves:
            nx,ny = x+dx,y+dy
            if 0<=nx<3 and 0<=ny<3:
                new = [row[:] for row in state]
                new[x][y], new[nx][ny] = new[nx][ny], new[x][y]
                neighbors.append(new)
        return neighbors

    def solve(self):
        start = self.board
        pq = []
        heapq.heappush(pq,(self.heuristic(start),0,start,[]))
        visited = set()

        while pq:
            _,cost,state,path = heapq.heappop(pq)

            if state == GOAL:
                self.animate(path)
                return

            visited.add(str(state))

            for neighbor in self.get_neighbors(state):
                if str(neighbor) not in visited:
                    heapq.heappush(pq,(cost+1+self.heuristic(neighbor),
                                       cost+1,
                                       neighbor,
                                       path+[neighbor]))

    def animate(self, path):
        for state in path:
            self.board = state
            self.update_board()
            self.root.update()
            time.sleep(0.4)

root = tk.Tk()
game = Puzzle(root)
root.mainloop()
