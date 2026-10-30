// SEPTEM - a first-person Soulslike engraved in black, white and blood red.
//
// This first playable build: the title, then free exploration of Stage I (the
// Drowned Abbey) on a grid, with the hands as the only interface:
//   left gauntlet  - three mana gems (lit red / spent hollow)
//   right forearm  - deaths branded as a Roman numeral
//   screen edges   - red hatching bleeds in as health drops
//
// A swings the sword (wind-up, cut, follow-through, recovery).
//
// The globals below are read by name by the gb-gbc-gba-test harness
// (gbtest.json `watch`), so they are volatile and live at global scope.
#include "bn_core.h"
#include "bn_keypad.h"
#include "bn_bg_palettes.h"
#include "bn_color.h"
#include "bn_regular_bg_ptr.h"
#include "bn_sprite_ptr.h"
#include "bn_optional.h"
#include "bn_array.h"

#include "bn_regular_bg_items_hands.h"
#include "bn_regular_bg_items_arm_0.h"
#include "bn_regular_bg_items_arm_1.h"
#include "bn_regular_bg_items_arm_2.h"
#include "bn_regular_bg_items_arm_3.h"
#include "bn_regular_bg_items_arm_4.h"
#include "bn_regular_bg_items_title.h"
#include "bn_regular_bg_items_vignette_1.h"
#include "bn_regular_bg_items_vignette_2.h"
#include "bn_regular_bg_items_vignette_3.h"
#include "bn_sprite_items_gem.h"
#include "bn_sprite_items_brand.h"

#include "septem_level.h"
#include "septem_view.h"
#include "gen/septem_map.h"

volatile int player_x = 0, player_y = 0, facing = 0;
volatile int wounds = 0;      // 0 unhurt .. 3 one blow from death
volatile int gems = 3;        // lit mana gems
volatile int deaths = 0;      // branded on the right forearm
volatile int game_state = 0;  // 0 title, 1 exploring
volatile int arm_pose = 0;    // 0 at rest, 1-4 the frames of a strike
volatile unsigned frame_counter = 0;
volatile int cpu_usage = 0;

namespace
{
    constexpr int max_wounds = 3;
    constexpr int max_gems = 3;
    constexpr int max_brand = 15;

    // Screen positions from tools/engrave_sprites.py (gem centres, brand top-left).
    constexpr int gem_x[3] = { 20, 33, 46 };
    constexpr int gem_y[3] = { 113, 108, 106 };
    constexpr int brand_x = 173 + 16;
    constexpr int brand_y = 113 + 8;

    // Hands sway on each step: down, then settle back.
    constexpr int bob_curve[] = { 1, 3, 4, 4, 3, 2, 1, 1, 0 };
    constexpr int bob_frames = sizeof(bob_curve) / sizeof(bob_curve[0]);

    // Holding the D-pad keeps walking at this pace.
    constexpr int step_repeat_frames = 16;

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

    void update()
    {
        frame_counter = frame_counter + 1;
        bn::core::update();
        cpu_usage = (bn::core::last_cpu_usage() * 100).right_shift_integer();
    }

    void title_screen()
    {
        game_state = 0;
        bn::regular_bg_ptr title = bn::regular_bg_items::title.create_bg(0, 0);

        while(! bn::keypad::start_pressed() && ! bn::keypad::a_pressed())
        {
            update();
        }
    }

    class body
    {

    public:
        body() :
            _hands(bn::regular_bg_items::hands.create_bg(0, 0)),
            _arm(bn::regular_bg_items::arm_0.create_bg(0, 0)),
            _gems({
                bn::sprite_items::gem.create_sprite(gem_x[0] - 120, gem_y[0] - 80),
                bn::sprite_items::gem.create_sprite(gem_x[1] - 120, gem_y[1] - 80),
                bn::sprite_items::gem.create_sprite(gem_x[2] - 120, gem_y[2] - 80),
            }),
            _brand(bn::sprite_items::brand.create_sprite(brand_x - 120, brand_y - 80))
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

        void step()
        {
            _bob = 0;
        }

        [[nodiscard]] bool striking() const
        {
            return _strike_step < strike_steps;
        }

        void strike()
        {
            if(! striking())
            {
                _strike_step = 0;
                _strike_wait = 0;
            }
        }

        // Advances the strike; returns the view shake for this frame.
        int update_strike()
        {
            if(! striking())
            {
                return 0;
            }

            const strike_frame& frame = strike_frames[_strike_step];

            if(_strike_wait == 0)
            {
                _set_arm(frame.pose);
            }

            int shake = frame.shake && (_strike_wait & 1) ? frame.shake : -frame.shake;

            if(++_strike_wait >= frame.frames)
            {
                _strike_wait = 0;

                if(++_strike_step == strike_steps)
                {
                    _set_arm(0);
                }
            }

            return shake;
        }

        void refresh()
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

        void update()
        {
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
        }

    private:
        void _set_arm(int pose)
        {
            arm_pose = pose;
            _arm.set_item(*arm_items[pose]);
            // The brand is burned on the resting forearm; mid-swing it turns away.
            _brand.set_visible(pose == 0);
        }

        bn::regular_bg_ptr _hands;
        bn::regular_bg_ptr _arm;
        bn::array<bn::sprite_ptr, 3> _gems;
        bn::sprite_ptr _brand;
        bn::optional<bn::regular_bg_ptr> _vignette;
        int _bob = bob_frames;
        int _strike_step = strike_steps;
        int _strike_wait = 0;
    };

    void explore(const septem::level& lv)
    {
        game_state = 1;
        player_x = lv.start_x;
        player_y = lv.start_y;
        facing = lv.start_facing;

        septem::view view;
        body hands;
        view.draw(lv, player_x, player_y, facing);

        int repeat = 0;

        while(true)
        {
            bool redraw = false;
            int move = 0;

            if(bn::keypad::a_pressed())
            {
                hands.strike();
            }

            if(hands.striking())
            {
                // Committed to the blow: no turning or stepping mid-swing.
            }
            else if(bn::keypad::left_pressed())
            {
                facing = (facing + 3) & 3;
                redraw = true;
            }
            else if(bn::keypad::right_pressed())
            {
                facing = (facing + 1) & 3;
                redraw = true;
            }
            else if(bn::keypad::up_pressed() || bn::keypad::down_pressed())
            {
                move = bn::keypad::up_held() ? 1 : -1;
                repeat = step_repeat_frames;
            }
            else if(bn::keypad::up_held() || bn::keypad::down_held())
            {
                if(--repeat <= 0)
                {
                    move = bn::keypad::up_held() ? 1 : -1;
                    repeat = step_repeat_frames;
                }
            }

            if(move)
            {
                int nx = player_x + septem::dir_x[facing] * move;
                int ny = player_y + septem::dir_y[facing] * move;

                if(lv.at(nx, ny) == septem::OPEN)
                {
                    player_x = nx;
                    player_y = ny;
                    redraw = true;
                    hands.step();
                }
            }

            // Preview controls until duels exist: SELECT wounds (the fourth
            // wound kills and brands the forearm), L spends a gem, R restores.
            if(bn::keypad::select_pressed())
            {
                if(wounds < max_wounds)
                {
                    wounds = wounds + 1;
                }
                else
                {
                    wounds = 0;
                    deaths = deaths + 1;
                    gems = max_gems;
                }

                hands.refresh();
            }

            if(bn::keypad::l_pressed() && gems > 0)
            {
                gems = gems - 1;
                hands.refresh();
            }

            if(bn::keypad::r_pressed())
            {
                gems = max_gems;
                hands.refresh();
            }

            if(redraw)
            {
                view.draw(lv, player_x, player_y, facing);
            }

            view.set_shake(0, hands.update_strike());
            hands.update();
            update();
        }
    }
}

int main()
{
    bn::core::init();
    bn::bg_palettes::set_transparent_color(bn::color(0, 0, 0));

    title_screen();
    static septem::level stage;
    stage.load(septem::gen::stage_map);
    explore(stage);
}
