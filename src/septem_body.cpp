#include "septem_body.h"

#include "bn_regular_bg_items_hands.h"
#include "bn_regular_bg_items_arm_0.h"
#include "bn_regular_bg_items_arm_1.h"
#include "bn_regular_bg_items_arm_2.h"
#include "bn_regular_bg_items_arm_3.h"
#include "bn_regular_bg_items_arm_4.h"
#include "bn_regular_bg_items_arm_5.h"
#include "bn_regular_bg_items_arm_6.h"
#include "bn_regular_bg_items_arm_7.h"
#include "bn_regular_bg_items_arm_8.h"
#include "bn_regular_bg_items_arm_9.h"
#include "bn_regular_bg_items_arm_10.h"
#include "bn_regular_bg_items_left_1.h"
#include "bn_regular_bg_items_left_2.h"
#include "bn_regular_bg_items_left_3.h"
#include "bn_regular_bg_items_left_4.h"
#include "bn_regular_bg_items_left_5.h"
#include "bn_regular_bg_items_left_6.h"
#include "bn_regular_bg_items_vignette_1.h"
#include "bn_regular_bg_items_vignette_2.h"
#include "bn_regular_bg_items_vignette_3.h"
#include "bn_regular_bg_items_death.h"
#include "bn_sprite_items_gem.h"
#include "bn_sprite_items_brand.h"

#include "septem_state.h"
#include "gen/septem_layout.h"

namespace septem
{

namespace
{
    constexpr int max_brand = 15;

    // Screen positions measured from the art (gems in each left-hand frame,
    // brand centre).
    constexpr int brand_x = gen::brand_x;
    constexpr int brand_y = gen::brand_y;

    // Hands sway on each step: down, then settle back.
    constexpr int bob_curve[] = { 1, 3, 4, 4, 3, 2, 1, 1, 0 };
    constexpr int bob_frames = sizeof(bob_curve) / sizeof(bob_curve[0]);

    // Right arm: 0 rest, 1-4 the strike, 5-7 block (raising, held, the blow
    // lands), 8-10 perfect parry (the meeting, the clash, turned aside).
    const bn::regular_bg_item* arm_items[] = {
        &bn::regular_bg_items::arm_0, &bn::regular_bg_items::arm_1, &bn::regular_bg_items::arm_2,
        &bn::regular_bg_items::arm_3, &bn::regular_bg_items::arm_4, &bn::regular_bg_items::arm_5,
        &bn::regular_bg_items::arm_6, &bn::regular_bg_items::arm_7, &bn::regular_bg_items::arm_8,
        &bn::regular_bg_items::arm_9, &bn::regular_bg_items::arm_10,
    };

    constexpr int block_raise_pose = 5;
    constexpr int block_hold_pose = 6;
    constexpr int block_raise_frames = 5;

    // Left hand: the gauntlet, then the flask frames.
    const bn::regular_bg_item* left_items[] = {
        &bn::regular_bg_items::hands, &bn::regular_bg_items::left_1, &bn::regular_bg_items::left_2,
        &bn::regular_bg_items::left_3, &bn::regular_bg_items::left_4, &bn::regular_bg_items::left_5,
        &bn::regular_bg_items::left_6,
    };

    // The strike (A): wind-up, the cut, follow-through, recovery.
    constexpr body::anim_frame strike_frames[] = {
        { 1, 6, 0 },
        { 2, 3, 2 },
        { 3, 6, 1 },
        { 4, 5, 0 },
    };

    constexpr int strike_steps = sizeof(strike_frames) / sizeof(strike_frames[0]);
    constexpr int cut_step = 1;

    constexpr body::anim_frame block_impact_frames[] = {
        { 7, 12, 2 },
    };

    constexpr body::anim_frame parry_frames[] = {
        { 8, 3, 0 },
        { 9, 8, 3 },
        { 10, 12, 0 },
    };
}

body::body() :
    _hands(bn::regular_bg_items::hands.create_bg(0, 0)),
    _arm(bn::regular_bg_items::arm_0.create_bg(0, 0)),
    _gems({
        bn::sprite_items::gem.create_sprite(gen::gem_x[0] - 120, gen::gem_y[0] - 80),
        bn::sprite_items::gem.create_sprite(gen::gem_x[1] - 120, gen::gem_y[1] - 80),
        bn::sprite_items::gem.create_sprite(gen::gem_x[2] - 120, gen::gem_y[2] - 80),
    }),
    _brand(bn::sprite_items::brand.create_sprite(brand_x - 120, brand_y - 80)),
    _bob(bob_frames)
{
    _hands.set_priority(1);
    _hands.set_z_order(1);
    _arm.set_priority(1);
    _arm.set_z_order(0);

    for(bn::sprite_ptr& gem : _gems)
    {
        gem.set_bg_priority(1);
    }

    _brand.set_bg_priority(1);
    refresh();
}

bool body::striking() const
{
    return _seq == strike_frames && _seq_step < _seq_count;
}

void body::_play(const anim_frame* frames, int count)
{
    _guard = 0;
    _seq = frames;
    _seq_count = count;
    _seq_step = 0;
    _seq_wait = 0;
}

void body::strike()
{
    if(! striking())
    {
        _play(strike_frames, strike_steps);
    }
}

void body::guard(int frames)
{
    if(_seq_step < _seq_count)
    {
        return;
    }

    if(! _guard)
    {
        _guard_age = 0;
    }

    _guard = frames;
}

void body::block_impact()
{
    _play(block_impact_frames, 1);
}

void body::parry()
{
    _play(parry_frames, 3);
}

void body::show_left(int frame)
{
    left_pose = frame;
    _left = frame;
    _hands.set_item(*left_items[frame]);

    for(int i = 0; i < max_gems; ++i)
    {
        _gems[i].set_x(gen::left_gem_x[frame][i] - 120);
    }
}

void body::show_death()
{
    // The death screen takes the vignette's layer, above everything.
    _vignette.reset();
    _vignette = bn::regular_bg_items::death.create_bg(0, 0);
    _vignette->set_priority(0);
}

void body::refresh()
{
    for(int i = 0; i < max_gems; ++i)
    {
        _gems[i].set_tiles(bn::sprite_items::gem.tiles_item(), i < gems ? 0 : 1);
    }

    int brand = deaths < max_brand ? deaths : max_brand;
    _brand.set_tiles(bn::sprite_items::brand.tiles_item(), brand);

    _vignette.reset();

    switch(wounds)
    {
    case 1:
        _vignette = bn::regular_bg_items::vignette_1.create_bg(0, 0);
        break;
    case 2:
        _vignette = bn::regular_bg_items::vignette_2.create_bg(0, 0);
        break;
    case 3:
        _vignette = bn::regular_bg_items::vignette_3.create_bg(0, 0);
        break;
    default:
        break;
    }

    if(_vignette)
    {
        _vignette->set_priority(0);
    }
}

int body::update()
{
    int shake = 0;

    if(_seq_step < _seq_count)
    {
        const anim_frame& frame = _seq[_seq_step];

        if(_seq_wait == 0)
        {
            _set_arm(frame.pose);
            _cut = striking() && _seq_step == cut_step;
        }

        shake = frame.shake && (_seq_wait & 1) ? frame.shake : -frame.shake;

        if(++_seq_wait >= frame.frames)
        {
            _seq_wait = 0;

            if(++_seq_step == _seq_count)
            {
                _set_arm(0);
            }
        }
    }
    else if(_guard)
    {
        // Raise the blade, then hold it flat and high until the guard drops.
        _set_arm(_guard_age < block_raise_frames ? block_raise_pose : block_hold_pose);
        ++_guard_age;

        if(--_guard == 0)
        {
            _set_arm(0);
        }
    }

    int offset = _bob < bob_frames ? bob_curve[_bob] : 0;

    if(_bob < bob_frames)
    {
        ++_bob;
    }

    _hands.set_y(offset);
    _arm.set_y(offset);

    for(int i = 0; i < max_gems; ++i)
    {
        _gems[i].set_y(gen::left_gem_y[_left][i] - 80 + offset);
    }

    _brand.set_y(brand_y - 80 + offset);
    return shake;
}

void body::_set_arm(int pose)
{
    if(pose == arm_pose)
    {
        return;
    }

    arm_pose = pose;
    _arm.set_item(*arm_items[pose]);
    // The brand is burned on the resting forearm; mid-swing it turns away.
    _brand.set_visible(pose == 0);
}

}
