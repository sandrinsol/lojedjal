#ifndef SEPTEM_STATE_H
#define SEPTEM_STATE_H

// Game state shared across the game, defined in main.cpp. They are volatile
// globals so the gb-gbc-gba-test harness can read them by name (gbtest.json).

extern volatile int player_x, player_y, facing;
extern volatile int hp;           // 0..max_hp; 0 is death
extern volatile int wounds;       // 0 unhurt .. 3 one blow from death (the red vignette)
extern volatile int gems;         // lit mana gems
extern volatile int vials;        // health vials left
extern volatile int deaths;       // branded on the right forearm
extern volatile int game_state;   // 0 title, 1 exploring, 2 duel
extern volatile int arm_pose;     // 0 rest, 1-4 strike, 5-7 block, 8-10 perfect parry
extern volatile int left_pose;    // 0 gauntlet, 1-4 flask held (0..3 left), 5-6 drinking

namespace septem
{
    constexpr int max_hp = 12;
    constexpr int max_gems = 3;
    constexpr int max_vials = 3;
}

#endif
