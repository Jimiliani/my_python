class Item:
    def __init__(self, name, health, damage, speed):
        self.name = name
        self.bonus_health = health
        self.bonus_damage = damage
        self.bonus_speed = speed


class Human:
    id = 0

    def __init__(self):
        self.name = "Human" + str(self.id)
        self.id += 1
        self.health = 100
        self.armor = 0
        self.damage = 12
        self.speed = 3
        self.items = []
        self.coordinates = (0, 0)

    def run(self, x, y):
        self.coordinates = (self.coordinates[0] + min(x, self.speed), self.coordinates[1] + min(y, self.speed))
        if self.health <= 0:
            print("He is dead, can't do this")
        else:
            print(self.name + " moved to " + str(self.coordinates))

    def take_item(self, other):
        if self.health <= 0:
            print("He is dead, can't do this")
        else:
            self.items.append(other)
            self.health += other.bonus_health
            self.damage += other.bonus_damage
            self.speed += other.bonus_speed
            print(self.name + " taked " + other.name)

    def shoot(self, other):
        other.health -= self.damage
        print(self.name + " dealed " + str(self.damage) + " damage, " + other.name + " has " + str(
            other.health) + " health")
        if other.health <= 0:
            print(other.name + " is dead")


class Vampire(Human):
    def __init__(self):
        super().__init__()
        self.name = "Vampire" + str(self.id)
        self.health = 80
        self.next_attack_bonus = 0

    def fly(self):
        self.next_attack_bonus = max(5, self.next_attack_bonus)
        print(self.name + " in air!")

    def shoot(self, other):
        other.health -= (self.damage + self.next_attack_bonus)
        self.next_attack_bonus = 0
        print(self.name + " dealed " + str(self.damage) + " damage, " + other.name + " has " + str(
            other.health) + " health")
        if other.health <= 0:
            print(other.name + " is dead")


def main():
    human = Human()
    vampire = Vampire()
    human.shoot(vampire)
    vampire.fly()
    vampire.shoot(human)
    vampire.shoot(human)
    vampire.shoot(human)
    human.run(2, 4)
    item = Item("Suped Sword", 0, 75, 0)
    human.take_item(item)
    human.shoot(vampire)


if __name__ == '__main__':
    main()
