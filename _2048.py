import tkinter as tk
import random
import copy

class Game2048(tk.Frame):
    COLORS = {
        0: ("#cdc1b4", "#776e65"),
        2: ("#eee4da", "#776e65"),
        4: ("#ede0c8", "#776e65"),
        8: ("#f2b179", "#f9f6f2"),
        16: ("#f59563", "#f9f6f2"),
        32: ("#f67c5f", "#f9f6f2"),
        64: ("#f65e3b", "#f9f6f2"),
        128: ("#edcf72", "#f9f6f2"),
        256: ("#edcc61", "#f9f6f2"),
        512: ("#edc850", "#f9f6f2"),
        1024: ("#edc53f", "#f9f6f2"),
        2048: ("#edc22e", "#f9f6f2"),
        4096: ("#3c3a32", "#f9f6f2"),
        8192: ("#3c3a32", "#f9f6f2"),
    }
    FONT = ("Helvetica", 40, "bold")
    
    
     
    def __init__(self):
        tk.Frame.__init__(self)
        self.grid()
        self.master.title('2048')

        self.main_grid = tk.Frame(self, bg='azure3', bd=3, width=400, height=400)
        self.main_grid.grid(pady=(100, 0))
        self.make_GUI()
        self.start_game()

        self.master.bind("<Left>", self.move_left)
        self.master.bind("<Right>", self.move_right)
        self.master.bind("<Up>", self.move_up)
        self.master.bind("<Down>", self.move_down)

        self.hint_button = tk.Button(self, text="Tipp", command=self.show_hint)
        self.hint_button.grid()

        self.mainloop()

    def make_GUI(self):
        self.cells = []
        for i in range(4):
            row = []
            for j in range(4):
                cell_frame = tk.Frame(
                    self.main_grid,
                    bg='azure4',
                    width=100,
                    height=100
                )
                cell_frame.grid(row=i, column=j, padx=5, pady=5)

                cell_number = tk.Label(
                    self.main_grid,
                    bg='azure4',
                    justify=tk.CENTER,
                    font=self.FONT,
                    width=4,
                    height=2
                )
                cell_number.grid(row=i, column=j)
                cell_number.bind("<Button-1>", lambda event, row=i, col=j: self.cell_clicked(row, col))
                row.append(cell_number)
            self.cells.append(row)

        score_frame = tk.Frame(self)
        score_frame.place(relx=0.5, y=45, anchor="center")
        tk.Label(score_frame, text="Score", font=("Arial", 24)).grid(row=0)
        self.score_label = tk.Label(score_frame, text="0", font=("Arial", 24))
        self.score_label.grid(row=1)

    def start_game(self):
        self.matrix = [[0] * 4 for _ in range(4)]
        self.score = 0

        self.add_new_tile()
        self.add_new_tile()
        self.update_GUI()

    def add_new_tile(self):
        empty_cells = [(i, j) for i in range(4) for j in range(4) if self.matrix[i][j] == 0]
        if empty_cells:
            row, col = random.choice(empty_cells)
            self.matrix[row][col] = random.choice([2, 4])

    def update_GUI(self):
        for i in range(4):
            for j in range(4):
                tile_value = self.matrix[i][j]
                if tile_value == 0:
                    self.cells[i][j].configure(text="", bg=self.COLORS[0][0])
                else:
                    self.cells[i][j].configure(text=str(tile_value),
                                               bg=self.COLORS[tile_value][0],
                                               fg=self.COLORS[tile_value][1])
        
        self.score_label.configure(text=self.score)
        self.update_idletasks()

    def stack(self):
        new_matrix = [[0] * 4 for _ in range(4)]
        for i in range(4):
            fill_position = 0
            for j in range(4):
                if self.matrix[i][j] != 0:
                    new_matrix[i][fill_position] = self.matrix[i][j]
                    fill_position += 1
        self.matrix = new_matrix

    def combine(self):
        for i in range(4):
            for j in range(3):
                if self.matrix[i][j] != 0 and self.matrix[i][j] == self.matrix[i][j+1]:
                    self.matrix[i][j] *= 2
                    self.matrix[i][j+1] = 0
                    self.score += self.matrix[i][j]

    def reverse(self):
        new_matrix = []
        for i in range(4):
            new_matrix.append([])
            for j in range(4):
                new_matrix[i].append(self.matrix[i][3-j])
        self.matrix = new_matrix

    def transpose(self):
        new_matrix = []
        for i in range(4):
            new_matrix.append([])
            for j in range(4):
                new_matrix[i].append(self.matrix[j][i])
        self.matrix = new_matrix

    def move_left(self, event):
        self.move_and_add_tile(self.move_left_logic)

    def move_right(self, event):
        self.move_and_add_tile(self.move_right_logic)

    def move_up(self, event):
        self.move_and_add_tile(self.move_up_logic)

    def move_down(self, event):
        self.move_and_add_tile(self.move_down_logic)

    def move_left_logic(self):
        self.stack()
        self.combine()
        self.stack()

    def move_right_logic(self):
        self.reverse()
        self.stack()
        self.combine()
        self.stack()
        self.reverse()

    def move_up_logic(self):
        self.transpose()
        self.stack()
        self.combine()
        self.stack()
        self.transpose()

    def move_down_logic(self):
        self.transpose()
        self.reverse()
        self.stack()
        self.combine()
        self.stack()
        self.reverse()
        self.transpose()

    def move_and_add_tile(self, move_logic):
        matrix_copy = copy.deepcopy(self.matrix)
        move_logic()
        if matrix_copy != self.matrix:
            self.add_new_tile()
        self.update_GUI()
        self.check_game_over()

    def check_game_over(self):
        for row in self.matrix:
            if 0 in row:
                return
        for i in range(4):
            for j in range(3):
                if self.matrix[i][j] == self.matrix[i][j+1]:
                    return
                if self.matrix[j][i] == self.matrix[j+1][i]:
                    return
        game_over_frame = tk.Frame(self.main_grid, borderwidth=2)
        game_over_frame.place(relx=0.5, rely=0.5, anchor="center")
        tk.Label(
            game_over_frame,
            text="Game Over!", 
            bg="red",
            fg="white",
            font=("Arial", 48)
        ).pack()

    def show_hint(self):
        moves = ["Left", "Right", "Up", "Down"]
        best_move = None
        best_score = -1

        def evaluate_grid(matrix, score):
            empty_cells = sum(row.count(0) for row in matrix)
            smoothness = self.calculate_smoothness(matrix)
            return score + empty_cells + smoothness

        # The more symmetrical numbers are near one to another the higher smoothness
        def calculate_smoothness(matrix):
            smoothness = 0
            for i in range(4):
                for j in range(4):
                    if matrix[i][j] != 0:
                        if i < 3 and matrix[i+1][j] != 0:
                            smoothness -= abs(matrix[i][j] - matrix[i+1][j])
                        if j < 3 and matrix[i][j+1] != 0:
                            smoothness -= abs(matrix[i][j] - matrix[i][j+1])
            return smoothness

        def deep_search(move_logic):
            matrix_copy = copy.deepcopy(self.matrix)
            score_copy = self.score

            move_logic()
            first_move_score = evaluate_grid(self.matrix, self.score)

            if matrix_copy == self.matrix:
                return -float("inf")

            second_move_scores = []
            for second_move in [self.move_left_logic, self.move_right_logic, self.move_up_logic, self.move_down_logic]:
                second_matrix_copy = copy.deepcopy(self.matrix)
                second_score_copy = self.score
                second_move()
                second_move_score = evaluate_grid(self.matrix, self.score)
                second_move_scores.append(second_move_score)
                self.matrix = second_matrix_copy
                self.score = second_score_copy

            total_score = first_move_score + max(second_move_scores)

            self.matrix = matrix_copy
            self.score = score_copy

            return total_score

        for move in moves:
            if move == "Left":
                move_logic = self.move_left_logic
            elif move == "Right":
                move_logic = self.move_right_logic
            elif move == "Up":
                move_logic = self.move_up_logic
            elif move == "Down":
                move_logic = self.move_down_logic

            move_score = deep_search(move_logic)

            if move_score > best_score:
                best_score = move_score
                best_move = move

        if best_move is None:
            best_move = "No possible turns"

        hint_frame = tk.Frame(self.main_grid, borderwidth=2)
        hint_frame.place(relx=0.5, rely=0.5, anchor="center")
        tk.Label(
            hint_frame,
            text=f"Best turn: {best_move}",
            bg="green",
            fg="white",
            font=("Arial", 24)
        ).pack()
        self.after(1000, hint_frame.destroy)


    def calculate_smoothness(self, matrix):
        smoothness = 0
        for i in range(4):
            for j in range(4):
                if matrix[i][j] != 0:
                    if i < 3 and matrix[i+1][j] != 0:
                        smoothness -= abs(matrix[i][j] - matrix[i+1][j])
                    if j < 3 and matrix[i][j+1] != 0:
                        smoothness -= abs(matrix[i][j] - matrix[i][j+1])
        return smoothness


        hint_frame = tk.Frame(self.main_grid, borderwidth=2)
        hint_frame.place(relx=0.5, rely=0.5, anchor="center")
        tk.Label(
            hint_frame,
            text=f"Best turn: {best_move}",
            bg="green",
            fg="white",
            font=("Arial", 24)
        ).pack()
        self.after(1000, hint_frame.destroy)


    def cell_clicked(self, row, col):
        self.popup = tk.Toplevel(self)
        self.popup.title("Configure cell")

        label = tk.Label(self.popup, text="Enter the number (0 to delete):")
        label.pack(pady=10)

        self.entry = tk.Entry(self.popup)
        self.entry.pack(pady=10)
        self.entry.focus()

        button = tk.Button(self.popup, text="OK", command=lambda: self.set_cell_value(row, col))
        button.pack(pady=10)

    def set_cell_value(self, row, col):
        try:
            value = int(self.entry.get())
            if value >= 0:
                self.matrix[row][col] = value
                self.update_GUI()
            self.popup.destroy()
        except ValueError:
            pass

if __name__ == "__main__":
    Game2048()
