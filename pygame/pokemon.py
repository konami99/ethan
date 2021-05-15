class Pokemon(object):
    name = 'Pokemon'
    ability = 'ability'

    def __init__(self, name, ability):
        self.name = name
        self.ability = ability

    def attack(self):
        print(self.name + ' is attacking with ' + self.ability)

    def retreat(self):
        print(self.name + ' is retreating')


class Pikachu(Pokemon):
    pass

class Mewtwo(Pokemon):
    pass

class Litten(Pokemon):
    pass


new_pikachu = Pikachu('Pika', 'lighting bolt')
new_pikachu.attack()
new_pikachu.retreat()

new_mewtwo = Mewtwo('Mew', 'Dark pulse')
new_mewtwo.attack()
new_mewtwo.retreat()

new_litten = Litten('Litt', 'Fire Fang')
new_litten.attack()
new_litten.retreat()