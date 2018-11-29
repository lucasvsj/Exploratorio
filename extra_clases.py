

class Point:

    def __init__(self, x=0, y=0, mirando=None):
        self.x = x
        self. y = y
        self.usado = False
        self.mirando = mirando


    def ciclo(self, other):
        if self.x == other.x and self.y == other.y:
            self.usado = True
            return None


    def __eq__(self, other):
        if self.x == other.x and self.y == other.y:
            return True
        else:
            return False


    def __hash__(self):
        return hash(str(self.x)+str(self.y))


class HitBox:

    def __init__(self, x, y):
        self.s_i = 0
        self.s_d = 0
        self.i_i = 0
        self.i_d = 0
        self.x = x
        self.y = y
        self.perimetro = set()


    def definir_area(self, other):
        self.centro = Point(int(other.x+other.pixmap.width()/2), \
                            int(other.y+other.pixmap.height()/2))
        self.s_i = Point(self.centro.x - (int((other.pixmap.width()/2))+2), \
                            self.centro.y + (int((other.pixmap.height()/2))+1))
        self.s_d = Point(self.centro.x + (int((other.pixmap.width()/2))+1), \
                            self.centro.y  + (int((other.pixmap.height()/2))+1))
        self.i_i = Point(self.centro.x - (int((other.pixmap.width()/2))+1), \
                            self.centro.y - (int((other.pixmap.height()/2))+1))
        self.i_d = Point(self.centro.x + (int((other.pixmap.width()/2))+1), \
                            self.centro.y  - (int((other.pixmap.height()/2))+1))
        self.perimetro = set([self.s_i, self.s_d, self.i_i, self.i_d])


    def seguir(self, other):
        if self.centro.x < other.centro.x:
            self.centro.x += 1
            for punto in self.perimetro:
                punto.x += 1
        if self.centro.y < other.centro.y:
            self.centro.y += 1
            for punto in self.perimetro:
                punto.y += 1
        if other.centro.x < self.centro.x:
            self.centro.x -= 1
            for punto in self.perimetro:
                punto.x -= 1
        if other.centro.y < self.centro.y:
            self.centro.y -= 1
            for punto in self.perimetro:
                punto.y -= 1


if __name__ == '__main__':
    a = HitBox(0,0)
