#include "septem_monk.h"

#include "bn_sprite_items_monk.h"
#include "bn_sprite_items_monk_far.h"

namespace septem
{

namespace
{
    // Feet on the water line of the cell `depth` ahead: the floor at
    // z = depth is at screen y = 86 + 40 / depth (see tools/engrave_world.py).
    constexpr int far_center_y[5] = { 0, 0, 106 - 32, 99 - 32, 96 - 32 };

    // The 128x128 duel figure stands one cell ahead (feet at y = 126), its
    // top-left at (56, -2); quadrant centres in screen space.
    constexpr int duel_x[4] = { 88, 152, 88, 152 };
    constexpr int duel_y[4] = { 30, 30, 94, 94 };

    bn::sprite_ptr make(const bn::sprite_item& item, int x, int y)
    {
        bn::sprite_ptr sprite = item.create_sprite(x - 120, y - 80);
        sprite.set_bg_priority(2);
        sprite.set_visible(false);
        return sprite;
    }
}

monk_view::monk_view() :
    _far(make(bn::sprite_items::monk_far, 120, far_center_y[2])),
    _duel({
        make(bn::sprite_items::monk, duel_x[0], duel_y[0]),
        make(bn::sprite_items::monk, duel_x[1], duel_y[1]),
        make(bn::sprite_items::monk, duel_x[2], duel_y[2]),
        make(bn::sprite_items::monk, duel_x[3], duel_y[3]),
    })
{
}

void monk_view::show_far(int depth)
{
    if(depth < 2 || depth > 4)
    {
        _far.set_visible(false);
        return;
    }

    _far.set_tiles(bn::sprite_items::monk_far.tiles_item(), depth - 2);
    _far.set_y(far_center_y[depth] - 80);
    _far.set_visible(true);
}

void monk_view::show_duel(pose p)
{
    for(int q = 0; q < 4; ++q)
    {
        _duel[q].set_tiles(bn::sprite_items::monk.tiles_item(), int(p) * 4 + q);
        _duel[q].set_visible(true);
    }
}

void monk_view::hide_duel()
{
    for(bn::sprite_ptr& sprite : _duel)
    {
        sprite.set_visible(false);
    }

    set_offset(0, 0);
}

void monk_view::set_offset(int x, int y)
{
    _offset_x = x;
    _offset_y = y;

    for(int q = 0; q < 4; ++q)
    {
        _duel[q].set_position(duel_x[q] - 120 + x, duel_y[q] - 80 + y);
    }
}

}
