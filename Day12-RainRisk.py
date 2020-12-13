from math import sin, cos, pi

class Ship:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.dx = 1
        self.dy = 0

    def move(self, instr : str):
        direction, value = instr[0], int(instr[1:])
        #old = (self.x, self.y, self.dx, self.dy)

        if direction == "E":
            self.x += value
        elif direction == "N":
            self.y += value
        elif direction == "W":
            self.x -= value
        elif direction == "S":
            self.y -= value

        elif direction in "LR":
            # Switch to always L
            if direction == "R":
                value = 360 - value
            # Repeatedly rotate 90 CCW
            for _ in range(value // 90):
                self.dx, self.dy = -self.dy, self.dx

        elif direction == "F":
            self.x += self.dx * value
            self.y += self.dy * value

        #print(f"{instr}: {old} -> ({self.x}, {self.y}, {self.dx}, {self.dy})")

    @property
    def norm(self) -> int:
        return abs(self.x) + abs(self.y)
    
class WaypointShip(Ship):
    def __init__(self):
        self.x = 0
        self.y = 0
        # dx, xy now represent the position of the waypoint relative to the ship
        self.dx = 10
        self.dy = 1

    def move(self, instr : str):
        direction, value = instr[0], int(instr[1:])
        #old = (self.x, self.y, self.dx, self.dy)

        if direction == "E":
            self.dx += value
        elif direction == "N":
            self.dy += value
        elif direction == "W":
            self.dx -= value
        elif direction == "S":
            self.dy -= value

        elif direction in "LR":
            # Switch to always L
            if direction == "R":
                value = 360 - value
            # Repeatedly rotate waypoint 90 CCW
            for _ in range(value // 90):
                self.dx, self.dy = -self.dy, self.dx

        elif direction == "F":
            self.x += self.dx * value
            self.y += self.dy * value

        #print(f"{instr}: {old} -> ({self.x}, {self.y}, {self.dx}, {self.dy})")
    

if __name__ == "__main__":
    ship = Ship()
    wp_ship = WaypointShip()
    with open("input12.txt") as f:
        for line in f.readlines():
            instr = line.strip()
            ship.move(instr)
            wp_ship.move(instr)
    
    print("Final position of ship:", ship.x, ship.y)
    print("Manhattan distance to origin:", ship.norm)
    
    print("Final position of waypoint ship:", wp_ship.x, wp_ship.y)
    print("Manhattan distance to origin:", wp_ship.norm)
