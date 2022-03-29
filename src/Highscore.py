import csv
import pygame

class Highscore():

    def __init__(self):
        self.set_highscore('john', 2341, '1')
        print(self.get('1'))
        pass

    def get(self, level):
        final = []
        with open('highscore.csv', encoding='UTF-8') as f:
            data = csv.reader(f, delimiter=",")
            for row in data:
                # Evité les valeurs vides
                if len(row) != 0 and level == row[2]:
                    final.append([row[0], int(row[1]), row[2]])
        return final 



    def set_highscore(self, username, score, level):
        # lire le contenue
        data = self.get(level)

        # ajouter la valeur (si il existe déjà, changer la valeur)
        found = False
        for i, row in enumerate(data):
            if username == row[0]:
                found = True
                if row[1] < score:
                    data[i][1] = score
        if not found:
            data.append([username,score,level])

        # sauvegarder
        with open('highscore.csv', 'w', newline='', encoding='UTF-8') as f:
            writer = csv.writer(f, )
            writer.writerows(data)
    
    def is_highscore(self, username, score, level):
        for row in self.get(level):
            if row[0] == username and row[2] == level:
                if score > row[1]:
                    return True
        return False

        
      