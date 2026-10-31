#include "septem_body.h"

#include "bn_regular_bg_items_hands.h"
#include "bn_regular_bg_items_arm_0.h"
#include "bn_regular_bg_items_arm_1.h"
#include "bn_regular_bg_items_arm_2.h"
#include "bn_regular_bg_items_arm_3.h"
#include "bn_regular_bg_items_arm_4.h"
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

    // Screen positions measured from the art (gem centres, brand centre).
    constexpr const int* gem_x = gen::gem_x;
    constexpr const int* gem_y = gen::gem_y;
    constexpr int brand_x = gen::brand_x;
    constexpr int brand_y = gen::brand_y;

    // Hands sway on each step: down, then settle back.
    constexpr int bob_curve[] = { 1, 3, 4, 4, 3, 2, 1, 1, 0 };
    constexpr int bob_frames = sizeof(bob_curve) / sizeof(bob_curve[0]);

    // The strike (A): wind-up, the cut, follow-through, recovery.
    const bn::regular_bg_item* arm_items[] = {
        &bn::regular_bg_items::arm_0, &bn::regular_bg_items::arm_1, &bn::regular_bg_items::arm_2,
        &bn::regular_bg_items::arm_3, &bn::regular_bg_items::arm_4,
    };

    struct strike_frame
    {
        int pose;
        int frames;
        int shake;
    };

    constexpr strike_frame strike_frames[] = {
        { 1, 6, 0 },
        { 2, 3, 2 },
        { 3, 6, 1 },
        { 4, 5, 0 },
    };

    constexpr int strike_steps = sizeof(strike_frames) / sizeof(strike_frames[0]);
    constexpr int cut_step = 1;
}

body::body() :
    _hands(bn::regular_bg_items::hands.create_bg(0, 0)),
    _arm(bn::regular_bg_items::arm_0.create_bg(0, 0)),
    _gems({
        bn::sprite_items::gem.create_sprite(gem_x[0] - 120, gem_y[0] - 80),
        bn::sprite_items::gem.create_sprite(gem_x[1] - 120, gem_y[1] - 80),
        bn::sprite_items::gem.create_sprite(gem_x[2] - 120, gem_y[2] - 80),
    }),
    _brand(bn::sprite_items::brand.create_sprite(brand_x - 120, brand_y - 80)),
    _bob(bob_frames),
    _strike_step(strike_steps)
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
    return _strike_step < strike_steps;
}

void body::strike()
{
    if(! striking())
    {
        _guard = 0;
        _strike_step = 0;
        _strike_wait = 0;
    }
}

void body::guard(int frames)
{
    if(! striking())
    {
        _guard = frames;
        _set_arm(1);
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

    if(striking())
    {
        const strike_frame& frame = strike_frames[_strike_step];

        if(_strike_wait == 0)
        {
            _set_arm(frame.pose);
            _cut = _strike_step == cut_step;
        }

        shake = frame.shake && (_strike_wait & 1) ? frame.shake : -frame.shake;

        if(++_strike_wait >= frame.frames)
        {
            _strike_wait = 0;

            if(++_strike_step == strike_steps)
            {
                _set_arm(0);
            }
        }
    }
    else if(_guard && --_guard == 0)
    {
        _set_arm(0);
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
        _gems[i].set_y(gem_y[i] - 80 + offset);
    }

    _brand.set_y(brand_y - 80 + offset);
    return shake;
}

void body::_set_arm(int pose)
{
    arm_pose = pose;
    _arm.set_item(*arm_items[pose]);
    // The brand is burned on the resting forearm; mid-swing it turns away.
    _brand.set_visible(pose == 0);
}

}
