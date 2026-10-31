#include "septem_view.h"

#include "bn_bg_palette_item.h"
#include "bn_bg_palette_ptr.h"
#include "bn_bg_tiles.h"
#include "bn_color.h"
#include "bn_memory.h"
#include "bn_regular_bg_map_cell_info.h"
#include "bn_regular_bg_map_item.h"
#include "bn_regular_bg_tiles_item.h"

#include "gen/septem_view.h"

namespace septem
{

namespace
{
    constexpr int screen_tiles = 30 * 20;

    BN_DATA_EWRAM_BSS alignas(4) bn::tile frame_tiles[screen_tiles];
    BN_DATA_EWRAM_BSS alignas(4) bn::regular_bg_map_cell map_cells[32 * 32];

    // Index 0 transparent (backdrop black), 1 black, 2 white, 3 blood red.
    // #D00024 in BGR555 is (26, 0, 4): shown as #D00020 on the console.
    constexpr bn::color palette_colors[16] = {
        bn::color(0, 0, 0), bn::color(0, 0, 0), bn::color(31, 31, 31), bn::color(26, 0, 4),
        bn::color(0, 0, 0), bn::color(0, 0, 0), bn::color(0, 0, 0), bn::color(0, 0, 0),
        bn::color(0, 0, 0), bn::color(0, 0, 0), bn::color(0, 0, 0), bn::color(0, 0, 0),
        bn::color(0, 0, 0), bn::color(0, 0, 0), bn::color(0, 0, 0), bn::color(0, 0, 0),
    };

    constexpr bn::bg_palette_item palette_item(palette_colors, bn::bpp_mode::BPP_4);

    bn::regular_bg_tiles_ptr create_tiles()
    {
        bn::memory::copy(gen::base_view[0], screen_tiles * 8, frame_tiles[0].data[0]);
        bool allow_offset = bn::bg_tiles::allow_offset();
        bn::bg_tiles::set_allow_offset(false);

        bn::regular_bg_tiles_ptr result = bn::regular_bg_tiles_ptr::create(
                bn::regular_bg_tiles_item(frame_tiles, bn::bpp_mode::BPP_4));
        bn::bg_tiles::set_allow_offset(allow_offset);
        return result;
    }

    bn::regular_bg_map_ptr create_map(const bn::regular_bg_tiles_ptr& tiles)
    {
        bn::memory::clear(map_cells);

        for(int row = 0; row < 20; ++row)
        {
            for(int column = 0; column < 30; ++column)
            {
                bn::regular_bg_map_cell_info info;
                info.set_tile_index(row * 30 + column);
                map_cells[row * 32 + column] = info.cell();
            }
        }

        bn::regular_bg_map_item map_item(map_cells[0], bn::size(32, 32));
        return bn::regular_bg_map_ptr::create(map_item, tiles, bn::bg_palette_ptr::create(palette_item));
    }

    void blit(const gen::panel& p)
    {
        const gen::panel_tile* t = p.tiles;

        for(int i = 0; i < p.count; ++i, ++t)
        {
            uint32_t* dst = frame_tiles[t->index].data;

            if(t->opaque)
            {
                for(int r = 0; r < 8; ++r)
                {
                    dst[r] = t->data[r];
                }
            }
            else
            {
                for(int r = 0; r < 8; ++r)
                {
                    dst[r] = (dst[r] & ~t->mask[r]) | t->data[r];
                }
            }
        }
    }
}

view::view() :
    _tiles(create_tiles()),
    _map(create_map(_tiles)),
    _bg(bn::regular_bg_ptr::create(_map))
{
    // Map pixel (0, 0) at the top-left of the screen.
    _bg.set_position(8, 48);
    _bg.set_priority(3);
}

void view::draw(const level& lv, int x, int y, int facing)
{
    int fx = dir_x[facing];
    int fy = dir_y[facing];
    int rx = -fy;
    int ry = fx;

    auto cell_at = [&](int l, int d)
    {
        return lv.at(x + fx * d + rx * l, y + fy * d + ry * l);
    };

    bn::memory::copy(gen::base_view[0], screen_tiles * 8, frame_tiles[0].data[0]);

    // Painter's order: far to near, outer to inner; mirrors compose() in
    // tools/engrave_world.py.
    for(int d = gen::max_depth; d >= 0; --d)
    {
        for(int a = gen::max_lateral; a >= 0; --a)
        {
            for(int side = 0; side < (a ? 2 : 1); ++side)
            {
                int l = side ? a : -a;
                int k = cell_at(l, d);

                if(! k)
                {
                    continue;
                }

                if(l != 0)
                {
                    int inner = l < 0 ? l + 1 : l - 1;

                    if(! cell_at(inner, d))
                    {
                        blit(gen::panels[k - 1][1][l + gen::max_lateral][d]);
                    }
                }

                if(d >= 1 && ! cell_at(l, d - 1))
                {
                    blit(gen::panels[k - 1][0][l + gen::max_lateral][d]);
                }
            }
        }
    }

    _tiles.reload_tiles_ref();
}

}
