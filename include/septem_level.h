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

    constexpr int max_map_size = 32;
    constexpr int max_enemies = 24;

    // A foe standing on a cell (map text 'M': the Somnolent Monk).
    struct enemy
    {
        int x;
        int y;
        bool alive;
    };

    // A map as stored in the ROM (generated from maps/*.txt by
    // tools/build_map.py; patched in place by the web map editor).
    struct map_block
    {
        char magic[8];      // "SEPTMAP1"
        uint8_t width;
        uint8_t height;
        uint8_t start_x;
        uint8_t start_y;
        uint8_t start_facing;
        uint8_t pad[3];
        char cells[max_map_size * max_map_size];   // '#' wall, 'W' window wall, '.' floor, 'M' monk
    };

    class level
    {

    public:
        int width = 0;
        int height = 0;
        int start_x = 0;
        int start_y = 0;
        int start_facing = 0;

        // Copies a map from the ROM. The volatile read keeps the compiler from
        // folding the layout into the code, so a patched ROM always takes effect.
        void load(const map_block& block)
        {
            const volatile map_block& source = block;
            width = clamp_size(source.width);
            height = clamp_size(source.height);
            start_x = source.start_x;
            start_y = source.start_y;
            start_facing = source.start_facing & 3;

            _enemies_count = 0;

            for(int i = 0, limit = width * height; i < limit; ++i)
            {
                char c = source.cells[i];

                if(c == 'M')
                {
                    if(_enemies_count < max_enemies)
                    {
                        _enemies[_enemies_count] = { i % width, i / width, true };
                        ++_enemies_count;
                    }

                    c = '.';
                }

                _cells[i] = c;
            }
        }

        // Every foe stands again (the stage resets when the player dies).
        void revive_enemies()
        {
            for(int i = 0; i < _enemies_count; ++i)
            {
                _enemies[i].alive = true;
            }
        }

        // Index of the living foe on (x, y), or -1.
        [[nodiscard]] int enemy_at(int x, int y) const
        {
            for(int i = 0; i < _enemies_count; ++i)
            {
                const enemy& e = _enemies[i];

                if(e.alive && e.x == x && e.y == y)
                {
                    return i;
                }
            }

            return -1;
        }

        void kill_enemy(int index)
        {
            _enemies[index].alive = false;
        }

        [[nodiscard]] int enemies_count() const
        {
            return _enemies_count;
        }

        [[nodiscard]] cell at(int x, int y) const
        {
            if(x < 0 || y < 0 || x >= width || y >= height)
            {
                return WALL;
            }

            switch(_cells[y * width + x])
            {
            case '.':
                return OPEN;
            case 'W':
                return WINDOW;
            default:
                return WALL;
            }
        }

    private:
        char _cells[max_map_size * max_map_size] = {};
        enemy _enemies[max_enemies] = {};
        int _enemies_count = 0;

        static int clamp_size(int size)
        {
            return size < 1 ? 1 : size > max_map_size ? max_map_size : size;
        }
    };
}

#endif
