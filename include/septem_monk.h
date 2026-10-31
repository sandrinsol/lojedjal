#ifndef SEPTEM_MONK_H
#define SEPTEM_MONK_H

#include "bn_array.h"
#include "bn_sprite_ptr.h"

namespace septem
{
    // The Somnolent Monk on screen: a small figure down the corridor while
    // exploring, and four 64x64 sprites (a 128x128 figure) filling the view in
    // a duel. Sprites sit behind the hands (BG priority 2).
    class monk_view
    {

    public:
        enum pose
        {
            IDLE,
            WINDUP,
            STRIKE,
            STAGGER,
            DEATH,
        };

        monk_view();

        // Shows the monk `depth` cells ahead (2..4), or hides it (0).
        void show_far(int depth);

        // Shows the duel figure in a pose, or hides it.
        void show_duel(pose p);
        void hide_duel();

        // Flashes the duel figure towards white (0 = none, 100 = all white).
        void set_flash(int percent);

        // Nudges the duel figure (lurching blows, sinking in death).
        void set_offset(int x, int y);

    private:
        bn::sprite_ptr _far;
        bn::array<bn::sprite_ptr, 4> _duel;
        int _offset_x = 0;
        int _offset_y = 0;
    };
}

#endif
