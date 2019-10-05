from math import cos, pi, floor, log2, radians
import mercantile
from mercantile import Tile


class QuadkeyUtils:
    E = 6378137  # 地球 [m]

    def l_e(self, tile):
        return (
            cos(mercantile.ul(tile.x, tile.y, tile.z).lat)
            * 2
            * pi
            * QuadkeyUtils.E
        ) / pow(2, tile.z)

    def search_LoD(m, tile):
        return floor(
            (
                cos(mercantile.ul(tile.x, tile.y, tile.z).lat)
                * 2
                * pi
                * QuadkeyUtils.E
            )
            / (2 * m)
        )

    def search_LoD_lat(m, lat):
        return floor(log2((cos(radians(lat)) * 2 * pi * QuadkeyUtils.E) / m))

    def neighbors(tile):
        _top = QuadkeyUtils.nextTile(tile, "top")
        _bottom = QuadkeyUtils.nextTile(tile, "bottom")
        return [
            QuadkeyUtils.nextTile(_top, "left"),
            _top,
            QuadkeyUtils.nextTile(_top, "right"),
            QuadkeyUtils.nextTile(tile, "left"),
            tile,
            QuadkeyUtils.nextTile(tile, "right"),
            QuadkeyUtils.nextTile(_bottom, "left"),
            _bottom,
            QuadkeyUtils.nextTile(_bottom, "right"),
        ]

    def neighbors_quadkey(tile):
        return [mercantile.quadkey(*t) for t in QuadkeyUtils.neighbors(tile)]

    def cut_key(quadkey, LoD):
        return quadkey[:LoD]

    def nextTile(tile, dir):
        # TODO:極域条件
        if dir == "top":
            return Tile(tile.x - 1, tile.y, tile.z)
        elif dir == "bottom":
            return Tile(tile.x + 1, tile.y, tile.z)
        elif dir == "left":
            return Tile(tile.x, tile.y - 1, tile.z)
        elif dir == "right":
            return Tile(tile.x, tile.y + 1, tile.z)
