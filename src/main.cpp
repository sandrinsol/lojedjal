// SEPTEM - a first-person Soulslike engraved in black, white and blood red.
//
// The title, then Stage I (the Drowned Abbey) on a grid, with the hands as the
// only interface:
//   left gauntlet  - three mana gems (lit red / spent hollow)
//   right forearm  - deaths branded as a Roman numeral
//   screen edges   - red hatching bleeds in as health drops
//
// Somnolent Monks stand on the map. Stepping in front of one starts a duel,
// taken in turns:
//   your turn   A strike, B drink a vial, L cast WARD (one gem)
//   his turn    he raises the censer, holds it for a slow, uneven time, then
//               brings it down: press R in the last moments before the blow
//               lands to parry. A parry staggers him; your next strike lands
//               twice as hard. Pressing too early is a flinch: the blow lands.
// Dying brands the forearm and restarts the stage: every monk stands again.
//
// The globals below are read by name by the gb-gbc-gba-test harness
// (gbtest.json `watch`), so they are volatile and live at global scope.
#include "bn_core.h"
#include "bn_keypad.h"
#include "bn_bg_palettes.h"
#include "bn_color.h"
#include "bn_random.h"
#include "bn_regular_bg_ptr.h"

#include "bn_regular_bg_items_title.h"

#include "septem_body.h"
#include "septem_level.h"
#include "septem_monk.h"
#include "septem_state.h"
#include "septem_view.h"
#include "gen/septem_map.h"

volatile int player_x = 0, player_y = 0, facing = 0;
volatile int hp = septem::max_hp;
volatile int wounds = 0;
volatile int gems = septem::max_gems;
volatile int vials = septem::max_vials;
volatile int deaths = 0;
volatile int game_state = 0;
volatile int arm_pose = 0;
volatile int duel_state = 0;    // see duel_states below
volatile int enemy_hp = 0;
volatile int ward_turns = 0;    // enemy blows still softened by WARD
volatile int last_defence = 0;  // 0 none, 1 parried, 2 hit, 3 flinched (too early)
volatile int parries = 0;       // successful parries, for tests
volatile unsigned frame_counter = 0;
volatile int cpu_usage = 0;

namespace
{
    enum duel_states
    {
        NO_DUEL,
        PLAYER_TURN,
        PLAYER_ACTING,
        ENEMY_WINDUP,
        ENEMY_STRIKE,       // the blow is falling: the parry window is at its end
        ENEMY_STAGGERED,
        ENEMY_DYING,
        PLAYER_DYING,
    };

    // Holding the D-pad keeps walking at this pace.
    constexpr int step_repeat_frames = 16;

    // The Somnolent Monk.
    constexpr int monk_hp = 4;
    constexpr int monk_damage = 3;          // four blows kill
    constexpr int monk_warded_damage = 1;
    constexpr int monk_windup_min = 30;     // frames he holds the censer up:
    constexpr int monk_windup_max = 90;     // slow and uneven, to bait a flinch
    constexpr int monk_strike_frames = 18;  // the censer falling
    constexpr int parry_window = 10;        // the last frames before impact

    constexpr int vial_heal = 6;
    constexpr int ward_length = 2;

    bn::random rng;

    void update()
    {
        rng.update();
        frame_counter = frame_counter + 1;
        bn::core::update();
        cpu_usage = (bn::core::last_cpu_usage() * 100).right_shift_integer();
    }

    void set_hp(int value)
    {
        hp = value < 0 ? 0 : value > septem::max_hp ? septem::max_hp : value;

        if(hp >= septem::max_hp)
        {
            wounds = 0;
        }
        else
        {
            int w = (septem::max_hp - hp + 2) / 3;
            wounds = w > 3 ? 3 : w;
        }
    }

    // One frame of the body and the view, with an extra jolt of the view.
    void tick(septem::view& view, septem::body& hands, int jolt = 0)
    {
        view.set_shake(0, hands.update() + jolt);
        update();
    }

    void wait(septem::view& view, septem::body& hands, int frames)
    {
        for(int i = 0; i < frames; ++i)
        {
            tick(view, hands);
        }
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

    // A duel with the Somnolent Monk standing one cell ahead. Returns true if
    // the monk falls, false if the player does.
    bool duel(septem::view& view, septem::body& hands, septem::monk_view& monk)
    {
        using pose = septem::monk_view::pose;

        game_state = 2;
        enemy_hp = monk_hp;
        ward_turns = 0;
        last_defence = 0;
        bool riposte = false;

        // Mana returns at the start of every fight.
        gems = septem::max_gems;
        hands.refresh();
        monk.show_far(0);
        monk.show_duel(pose::IDLE);
        wait(view, hands, 24);

        while(true)
        {
            // Your turn: strike, drink or cast.
            duel_state = PLAYER_TURN;
            int action = 0;

            while(! action)
            {
                if(bn::keypad::a_pressed())
                {
                    action = 1;
                }
                else if(bn::keypad::b_pressed() && vials > 0 && hp < septem::max_hp)
                {
                    action = 2;
                }
                else if(bn::keypad::l_pressed() && gems > 0)
                {
                    action = 3;
                }
                else
                {
                    tick(view, hands);
                }
            }

            duel_state = PLAYER_ACTING;

            if(action == 1)
            {
                hands.strike();

                while(hands.striking())
                {
                    tick(view, hands);

                    if(hands.take_cut())
                    {
                        enemy_hp = enemy_hp - (riposte ? 2 : 1);
                        riposte = false;
                        monk.show_duel(pose::STAGGER);
                    }
                }

                if(enemy_hp <= 0)
                {
                    duel_state = ENEMY_DYING;
                    monk.show_duel(pose::DEATH);

                    for(int i = 0; i < 80; ++i)
                    {
                        // He sinks into the flood.
                        monk.set_offset(0, i / 8);
                        tick(view, hands);
                    }

                    monk.hide_duel();
                    duel_state = NO_DUEL;
                    return true;
                }

                monk.show_duel(pose::IDLE);
            }
            else if(action == 2)
            {
                vials = vials - 1;
                set_hp(hp + vial_heal);
                hands.refresh();
                wait(view, hands, 30);
            }
            else
            {
                gems = gems - 1;
                ward_turns = ward_length;
                hands.refresh();
                hands.guard(20);
                wait(view, hands, 24);
            }

            // His turn: the censer rises, hangs, and falls.
            wait(view, hands, 16);
            duel_state = ENEMY_WINDUP;
            monk.show_duel(pose::WINDUP);

            bool flinched = false;
            bool parried = false;
            int hold = rng.get_int(monk_windup_min, monk_windup_max + 1);

            for(int i = 0; i < hold; ++i)
            {
                if(bn::keypad::r_pressed())
                {
                    flinched = true;
                }

                tick(view, hands);
            }

            duel_state = ENEMY_STRIKE;
            monk.show_duel(pose::STRIKE);

            for(int i = 0; i < monk_strike_frames && ! parried; ++i)
            {
                if(bn::keypad::r_pressed() && ! flinched)
                {
                    if(i >= monk_strike_frames - parry_window)
                    {
                        parried = true;
                    }
                    else
                    {
                        flinched = true;
                    }
                }

                monk.set_offset(0, i / 3);
                tick(view, hands);
            }

            monk.set_offset(0, 0);

            if(parried)
            {
                last_defence = 1;
                parries = parries + 1;
                riposte = true;
                duel_state = ENEMY_STAGGERED;
                hands.guard(14);
                monk.show_duel(pose::STAGGER);

                for(int i = 0; i < 30; ++i)
                {
                    tick(view, hands, i < 6 ? ((i & 1) ? 1 : -1) : 0);
                }
            }
            else
            {
                last_defence = flinched ? 3 : 2;
                set_hp(hp - (ward_turns > 0 ? monk_warded_damage : monk_damage));
                hands.refresh();

                for(int i = 0; i < 14; ++i)
                {
                    tick(view, hands, (i & 1) ? 3 - i / 5 : -(3 - i / 5));
                }

                if(hp <= 0)
                {
                    duel_state = PLAYER_DYING;

                    for(int i = 0; i < 90; ++i)
                    {
                        tick(view, hands, i < 20 ? ((i & 1) ? 2 : -2) : 0);
                    }

                    monk.hide_duel();
                    duel_state = NO_DUEL;
                    return false;
                }
            }

            if(ward_turns > 0)
            {
                ward_turns = ward_turns - 1;
            }

            monk.show_duel(pose::IDLE);
        }
    }

    // The nearest living monk straight ahead, with no wall between: its depth
    // (1..4) and index, or depth 0.
    int monk_ahead(const septem::level& lv, int* index)
    {
        for(int d = 1; d <= 4; ++d)
        {
            int x = player_x + septem::dir_x[facing] * d;
            int y = player_y + septem::dir_y[facing] * d;

            if(lv.at(x, y) != septem::OPEN)
            {
                return 0;
            }

            int e = lv.enemy_at(x, y);

            if(e >= 0)
            {
                *index = e;
                return d;
            }
        }

        return 0;
    }

    void restart_stage(septem::level& lv)
    {
        lv.revive_enemies();
        player_x = lv.start_x;
        player_y = lv.start_y;
        facing = lv.start_facing;
        set_hp(septem::max_hp);
        vials = septem::max_vials;
        gems = septem::max_gems;
    }

    void explore(septem::level& lv)
    {
        septem::view view;
        septem::body hands;
        septem::monk_view monk;

        restart_stage(lv);
        hands.refresh();
        bool redraw = true;
        int repeat = 0;

        while(true)
        {
            game_state = 1;

            if(redraw)
            {
                redraw = false;
                view.draw(lv, player_x, player_y, facing);

                int enemy = -1;
                int depth = monk_ahead(lv, &enemy);

                if(depth == 1)
                {
                    // Face to face: the duel.
                    wait(view, hands, 1);

                    if(duel(view, hands, monk))
                    {
                        lv.kill_enemy(enemy);
                    }
                    else
                    {
                        deaths = deaths + 1;
                        restart_stage(lv);
                        hands.refresh();
                    }

                    redraw = true;
                    continue;
                }

                monk.show_far(depth);
            }

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

                // Monks bar the way: they must be fought, not passed.
                if(lv.at(nx, ny) == septem::OPEN && lv.enemy_at(nx, ny) < 0)
                {
                    player_x = nx;
                    player_y = ny;
                    redraw = true;
                    hands.step();
                }
            }

            tick(view, hands);
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
