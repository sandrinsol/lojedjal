# SEPTEM - Butano (C++) project. `make` builds septem.gba plus septem.elf, whose
# symbols the gb-gbc-gba-test harness reads (player_x, wounds, gems, ...).
#
# Needs devkitARM (DEVKITPRO / DEVKITARM set) and Butano: set BUTANO to the
# Butano checkout (the folder with butano/ and common/ inside).
# Map: `make map` turns maps/drowned_abbey.txt into include/gen/septem_map.h.
# Art: `make art` regenerates (artwork in assets/raw replaces the engraved
# placeholders, see tools/import_art.py) assets/ and graphics/ (Python 3 + numpy, scipy,
# Pillow; Node 20 + the gb-gbc-gba-test-mcp harness, see tools/convert_art.mjs).
BUTANO       ?= /opt/butano
# Butano resolves these folders from the project, so use a relative path.
BN           := $(shell python3 -c "import os, sys; print(os.path.relpath(sys.argv[1]))" "$(BUTANO)")

TARGET       := septem
BUILD        := build
LIBBUTANO    := $(BUTANO)/butano
PYTHON       := python3
SOURCES      := src
INCLUDES     := include
DATA         :=
GRAPHICS     := graphics
AUDIO        :=
AUDIOBACKEND := maxmod
AUDIOTOOL    :=
DMGAUDIO     :=
DMGAUDIOBACKEND := default
ROMTITLE     := SEPTEM
ROMCODE      := SPTM
USERFLAGS    :=
USERCXXFLAGS :=
USERASFLAGS  :=
USERLDFLAGS  :=
USERLIBDIRS  :=
USERLIBS     :=
DEFAULTLIBS  :=
STACKTRACE   :=
USERBUILD    :=
EXTTOOL      :=

ifndef LIBBUTANOABS
	export LIBBUTANOABS := $(realpath $(LIBBUTANO))
endif
ifeq ($(LIBBUTANOABS),)
$(error Butano not found at $(BUTANO): set BUTANO=/path/to/butano)
endif

include $(LIBBUTANOABS)/butano.mak

.PHONY: art map
map:
	$(PYTHON) tools/build_map.py

art: map
	$(PYTHON) tools/engrave_world.py
	$(PYTHON) tools/engrave_sprites.py
	$(PYTHON) tools/engrave_monk.py
	$(PYTHON) tools/import_art.py
	node tools/convert_art.mjs
