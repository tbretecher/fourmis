import tkinter as tk
from typing import List


class Food:
    def __init__(self, master: tk.Canvas, color='green', radius=10, base_pos=0, coords=(17, 14)):
        self.canvas = master
        self.color = color
        self.radius = radius
        self._base_pos = base_pos
        self.unit = base_pos*2
        self.coords = coords
        self.food = self.create_food()

    def map_coords(self, coords=(1,1)):
        return (
            self._base_pos + (coords[0] - 1) * self.unit,
            self._base_pos + 19 * self.unit - (coords[1] - 1) * self.unit,
        )

    def create_food(self):
        x, y = self.map_coords(coords=self.coords)

        return self.canvas.create_rectangle(
            x - self.radius,
            y - self.radius,
            x + self.radius,
            y + self.radius,
            fill=self.color,
            outline=''
        )


class Ant:
    def __init__(self, master: tk.Canvas, _id=None, color='black', radius=4, base_pos=0, coords=None, life=[], pv=20, delay=750):
        self.canvas = master
        self.id = _id 
        self.color = color
        self._base_pos = base_pos
        self.unit = base_pos*2
        self.life = life
        self.life_max = float(pv)
        self.radius = radius * life[0] / self.life_max

        self.anim = True
        self.time_cur = 0  # current time, time being defined by index of coords list
        self.time_max = len(coords)-1
        self.delay = delay
        self.smooth_delay = int(delay / float(self.unit+5))


        if isinstance(coords, list):
            self.coords_list = coords
            self.coords = coords[0]
        else:
            self.coords = coords

        self.ant = self.create_ant()
        self.canvas.tag_raise(self.ant)

        self.canvas.after(1500, self.animate)

    def map_coords(self, coords=(1,1)):
        return (
            self._base_pos + (coords[0] - 1) * self.unit,
            self._base_pos + 19 * self.unit - (coords[1] - 1) * self.unit,
        )

    def create_ant(self):
        x, y = self.map_coords(coords=self.coords)

        return self.canvas.create_oval(
            x - self.radius,
            y - self.radius,
            x + self.radius,
            y + self.radius,
            fill=self.color
        )

    def smooth_move_up(self):
        if self.delta < 0:
            # print('up: ', self.delta)
            self.canvas.move(self.ant, *(0, -1))
            self.delta += 1
            self.canvas.after(self.smooth_delay, self.smooth_move_up)

    def smooth_move_right(self):
        if self.delta > 0:
            # print('right: ', self.delta)
            self.canvas.move(self.ant, *(1, 0))
            self.delta -= 1
            self.canvas.after(self.smooth_delay, self.smooth_move_right)

    def smooth_move_down(self):
        if self.delta > 0:
            # print('down: ', self.delta)
            self.canvas.move(self.ant, *(0, 1))
            self.delta -= 1
            self.canvas.after(self.smooth_delay, self.smooth_move_down)

    def smooth_move_left(self):
        if self.delta < 0:
            # print('right: ', self.delta)
            self.canvas.move(self.ant, *(-1, 0))
            self.delta += 1
            self.canvas.after(self.smooth_delay, self.smooth_move_left)

    def update_ant(self):
        x_cur, y_cur = self.coords_list[self.time_cur]
        self.time_cur += 1
        x_next, y_next = self.coords_list[self.time_cur]

        print('Time {}/{}; ant {} will now move from x {} to x {} and from y {} to y {}; Life: {}'.format(self.time_cur, self.time_max, self.id, x_cur, x_next, y_cur, y_next, self.life[self.time_cur]))

        x_last, y_last = self.map_coords((x_cur, y_cur))
        x, y = self.map_coords((x_next, y_next))

        dx = x - x_last
        dy = y - y_last

        if dx > 0:
            self.delta = self.unit
            self.smooth_move_right()
        elif dx < 0:
            self.delta = -self.unit
            self.smooth_move_left()
        elif dy > 0:
            self.delta = self.unit
            self.smooth_move_down()
        elif dy < 0:
            self.delta = -self.unit
            self.smooth_move_up()

        self.canvas.move(self.ant, *(dx, dy))
        

        radius = self.radius * self.life[self.time_cur] / self.life_max
        if radius == 0:
            color = 'white'
            self.anim = False
        else:
            color = 'black'

        self.canvas.coords(
            self.ant,
            x_last - radius,
            y_last - radius,
            x_last+ radius,
            y_last + radius,
        )

        self.canvas.itemconfig(self.ant, fill=color, outline="")
        self.canvas.tag_raise(self.ant)

    def animate(self):
        if self.time_cur < self.time_max and self.anim:
            self.update_ant()
            self.canvas.after(self.delay, self.animate)
            


class Mainframe(tk.Frame):
    def __init__(self, master, width, height, food_coords, ants_dict, pv, delay=750):
        tk.Frame.__init__(self, master, width=width, height=height)
        self.master = master
        self.grid(sticky='nsew')
        self.grid_propagate(0)
        self.width = 400
        self.height = 400
        self.step_size = 20
        self.ants_dict = ants_dict

        self.food_coords = food_coords

        self.canvas = tk.Canvas(
            self,
            width=self.width,
            height=self.height,
            background='ivory',
            relief=tk.SOLID
        )

        self.canvas.pack(padx=8, pady=8, side=tk.TOP)
        self.create_grid()

        for key in self.ants_dict:
            Ant(self.canvas, _id=key, radius=10, color='black', base_pos=self.step_size/2., coords=self.ants_dict[key]['coords'], life=self.ants_dict[key]['life'], pv=pv, delay=delay)

        for food_coord in self.food_coords:
            Food(self.canvas, base_pos=self.step_size/2., coords=food_coord)

        # self.master.bind("<Key>", self.ant.move)

    def create_grid(self):
        self.canvas.create_line(0, 1, 400, 1, fill='black', width=1)
        self.canvas.create_line(1, 0, 1, 400, fill='black', width=1)
        for step in range(self.step_size, self.width+self.step_size, self.step_size):
            self.canvas.create_line(0, step, self.height, step, fill='black', width=1)
            self.canvas.create_line(step, 0, step, self.width, fill='black', width=1)


class Visual_App(tk.Tk):
    def __init__(self, ants_dict, foodx, foody, pv, delay=750):
        tk.Tk.__init__(self)
        self.title("My app")
        self.width = 500
        self.height = 500
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.mainframe = Mainframe(self, width=self.width, height=self.height, food_coords=self._parse_food(foodx, foody), ants_dict=self._parse_ants_dict(ants_dict), pv=pv, delay=delay)
        
    def _parse_food(self, foodx, foody):
        return list(zip(foodx, foody))

    def _parse_ants_dict(self, ants_dict):
        new_ants_dict = {}
        for key in ants_dict:
            new_ants_dict[key] = {'coords': list(zip(ants_dict[key]['x'], ants_dict[key]['y'])), 'life': ants_dict[key]['pv']}

        return new_ants_dict

    def run(self):      
        self.update()
        self.resizable(True, True)
        self.mainloop()


if __name__ == '__main__':

    foodx = [17, 20, 1, 20, 6, 15]
    foody = [14, 17, 3, 6, 4, 12]
    ants_dict =  {
        0: {
            'x': [16, 17, 17, 18, 18, 18, 17, 17, 17, 17],
            'y': [4, 4, 3, 3, 4, 5, 5, 5, 5, 6],
            'pv': [20, 18, 16, 14, 12, 10, 8, 7.0, 6.0, 4.0]},
        1: {
            'x': [10, 9, 9, 8, 9, 9, 9, 10, 10, 10],
            'y': [11, 11, 10, 10, 10, 9, 10, 10, 10, 10],
            'pv': [20, 18, 16, 14, 12, 10, 8, 7.0, 6.0, 5.0]},
        2: {
            'x': [13, 13, 14, 14, 14, 14, 14, 14, 15, 16],
            'y': [6, 5, 5, 6, 5, 6, 7, 7, 7, 7],
            'pv': [20, 18, 16, 14, 12, 10, 8, 7.0, 5.0, 3.0]},
        3: {
            'x': [5, 5, 5, 5, 6, 6, 6, 6, 7, 7],
            'y': [4, 3, 4, 5, 5, 4, 3, 4, 4, 5],
            'pv': [20, 18, 16, 14, 12, 20, 18, 20, 18, 16.0]
            }
        }
    delay = 2000

    app = Visual_App(ants_dict, foodx, foody, pv=20, delay=delay)
    app.run()

