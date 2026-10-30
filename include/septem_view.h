#ifndef SEPTEM_VIEW_H
#define SEPTEM_VIEW_H

#include "bn_regular_bg_ptr.h"
#include "bn_regular_bg_map_ptr.h"
#include "bn_regular_bg_tiles_ptr.h"

#include "septem_level.h"

namespace septem
{
    // The first-person view: a full-screen BG whose 600 tiles are composed in
    // EWRAM from the pre-engraved panels, far to near, then copied to VRAM.
    class view
    {

    public:
        view();

        void draw(const level& lv, int x, int y, int facing);

        void set_visible(bool visible)
        {
            _bg.set_visible(visible);
        }

    private:
        bn::regular_bg_tiles_ptr _tiles;
        bn::regular_bg_map_ptr _map;
        bn::regular_bg_ptr _bg;
    };
}

#endif
