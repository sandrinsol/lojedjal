#ifndef SEPTEM_BODY_H
#define SEPTEM_BODY_H

#include "bn_array.h"
#include "bn_optional.h"
#include "bn_regular_bg_ptr.h"
#include "bn_sprite_ptr.h"

namespace septem
{
    // The player's body, the only interface: the left gauntlet with its mana
    // gems, the right arm with the sword and the death brand, and the red
    // vignette of wounds. Reads the game state globals (gems, deaths, wounds).
    class body
    {

    public:
        body();

        // Hands sway after a step.
        void step()
        {
            _bob = 0;
        }

        [[nodiscard]] bool striking() const;

        // Starts a sword strike (ignored mid-swing).
        void strike();

        // Raises the blade to block for a few frames (a parry).
        void guard(int frames);

        // True once, on the frame the blade cuts through (the moment of a hit).
        [[nodiscard]] bool take_cut()
        {
            bool cut = _cut;
            _cut = false;
            return cut;
        }

        // Re-reads gems, deaths and wounds.
        void refresh();

        // Advances animations; returns the view shake for this frame.
        int update();

    private:
        void _set_arm(int pose);

        bn::regular_bg_ptr _hands;
        bn::regular_bg_ptr _arm;
        bn::array<bn::sprite_ptr, 3> _gems;
        bn::sprite_ptr _brand;
        bn::optional<bn::regular_bg_ptr> _vignette;
        int _bob;
        int _strike_step;
        int _strike_wait = 0;
        int _guard = 0;
        bool _cut = false;
    };
}

#endif
