#ifndef SEPTEM_LEVEL_H
#define SEPTEM_LEVEL_H

#include "bn_common.h"

namespace septem
{
    // Cell codes, as used by the view panels (tools/engrave_world.py).
    enum cell : uint8_t
    {
        OPEN = 0,
        WALL = 1,
        WINDOW = 2,
    };

    // Facing: 0 north (-y), 1 east (+x), 2 south (+y), 3 west (-x).
    constexpr int dir_x[4] = { 0, 1, 0, -1 };
    constexpr int dir_y[4] = { -1, 0, 1, 0 };

    struct level
    {
        int width;
        int height;
        const char* rows;   // '#' wall, 'W' wall with a lancet window, '.' floor
        int start_x;
        int start_y;
        int start_facing;

        [[nodiscard]] cell at(int x, int y) const
        {
            if(x < 0 || y < 0 || x >= width || y >= height)
            {
                return WALL;
            }

            switch(rows[y * width + x])
            {
            case '#':
                return WALL;
            case 'W':
                return WINDOW;
            default:
                return OPEN;
            }
        }
    };

    // Stage I - Sloth: the Drowned Abbey (first sketch of the layout).
    inline constexpr char drowned_abbey_rows[] =
        "################"
        "#W#....W....#W.#"
        "#.#.##...##.#..#"
        "#...#.....#...##"
        "###.#.#.#.#.#..#"
        "#.....#.#.....W#"
        "#.#####.#####..#"
        "#W....#.#......#"
        "###.#.#.#.####.#"
        "#...#.#.#.#....#"
        "#.###.#.#.#.####"
        "#.....#.#......#"
        "###.#W#.#W######"
        "#.......#......#"
        "#.#####...####.#"
        "#######W########";

    inline constexpr level drowned_abbey = { 16, 16, drowned_abbey_rows, 7, 14, 0 };
}

#endif
