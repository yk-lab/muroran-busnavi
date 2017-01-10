from math import cos, pi
import mercantile

class QuadkeyUtils(mercantile):
    E = 6378137 # 地球 [m]

    def l_e(self, tile):
        return (cos(self.ul(tile.x, tile.y, tile.z).lat)*2*pi*self.E)/(2*tile.z)    # (cos(lat)*2*pi*E)/(2*LoD)

    def neighbors(self, tile):
        return [
            self.nextTile(self.nextTile(tile, "top"), "left"), self.nextTile(tile, "top"), self.nextTile(self.nextTile(tile, "top"), "right"),
            self.nextTile(tile, "left"), tile, self.nextTile(tile, "right"),
            self.nextTile(self.nextTile(tile, "bottom"), "left"), self.nextTile(tile, "bottom"), self.nextTile(self.nextTile(tile, "bottom"), "right")
        ]

    def neighbors_quadkey(self, tile):
        return [self.quadkey(*tile) for tile in self.neighbors(tile)]

    def cut_key(self, quadkey, LoD):
        return quadkey[:LoD]

    def nextTile(self, tile, dir):
        # TODO:極域条件
        if dir == "top":
            return Tile(tile.x - 1, tile.y, tile.z)
        elif dir == "bottom":
            return Tile(tile.x + 1, tile.y, tile.z)
        elif dir == "left":
            return Tile(tile.x, tile.y - 1, tile.z)
        elif dir == "right":
            return Tile(tile.x, tile.y + 1, tile.z)
