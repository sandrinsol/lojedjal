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
        // One step of an arm animation: the arm pose, how long it shows, and
        // how hard it jolts the view.
        struct anim_frame
        {
            int pose;
            int frames;
            int shake;
        };

        body();

        // Hands sway after a step.
        void step()
        {
            _bob = 0;
        }

        [[nodiscard]] bool striking() const;

        // Starts a sword strike (ignored mid-swing).
        void strike();

        // Raises the guard (or keeps it raised) for `frames` more frames: the
        // blade swings up, then is held flat and high.
        void guard(int frames);

        // A blocked blow lands on the raised guard.
        void block_impact();

        // The perfect parry: the blade snaps up, the clash, the blow turned aside.
        void parry();

        // Shows a left-hand frame: 0 the gauntlet, 1..4 the flask held with
        // 0..3 draughts left, 5 drinking, 6 the last draught gone.
        void show_left(int frame);

        // True once, on the frame the blade cuts through (the moment of a hit).
        [[nodiscard]] bool take_cut()
        {
            bool cut = _cut;
            _cut = false;
            return cut;
        }

        // Shows the death screen over everything (until the next refresh).
        void show_death();

        // Re-reads gems, deaths and wounds.
        void refresh();

        // Advances animations; returns the view shake for this frame.
        int update();

    private:
        void _play(const anim_frame* frames, int count);
        void _set_arm(int pose);

        bn::regular_bg_ptr _hands;
        bn::regular_bg_ptr _arm;
        bn::array<bn::sprite_ptr, 3> _gems;
        bn::sprite_ptr _brand;
        bn::optional<bn::regular_bg_ptr> _vignette;
        int _bob;
        const anim_frame* _seq = nullptr;
        int _seq_count = 0;
        int _seq_step = 0;
        int _seq_wait = 0;
        int _guard = 0;
        int _guard_age = 0;
        int _left = 0;
        bool _cut = false;
    };
}

#endif
