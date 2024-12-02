export TERM=${TERM:="xterm-256color"}

MICROPYTHON_FLAVOUR="peterharperuk"
MICROPYTHON_VERSION="pico2_w_changes"

PIMORONI_PICO_FLAVOUR="pimoroni"
PIMORONI_PICO_VERSION="feature/inky-pico2_w"

PY_DECL_VERSION="v0.0.3"
DIR2UF2_VERSION="v0.0.9"

SCRIPT_PATH="$(dirname $0)"
CI_PROJECT_ROOT=$(realpath "$SCRIPT_PATH/..")
CI_BUILD_ROOT=$(pwd)


function log_success {
	echo -e "$(tput setaf 2)$1$(tput sgr0)"
}

function log_inform {
	echo -e "$(tput setaf 6)$1$(tput sgr0)"
}

function log_warning {
	echo -e "$(tput setaf 1)$1$(tput sgr0)"
}

function ci_pimoroni_pico_clone {
    log_inform "Using Pimoroni Pico $PIMORONI_PICO_FLAVOUR/$PIMORONI_PICO_VERSION"
    git clone https://github.com/$PIMORONI_PICO_FLAVOUR/pimoroni-pico "$CI_BUILD_ROOT/pimoroni-pico"
    cd "$CI_BUILD_ROOT/pimoroni-pico" || return 1
    git checkout $PIMORONI_PICO_VERSION
    git submodule update --init
    cd "$CI_BUILD_ROOT"
}

function ci_micropython_clone {
    log_inform "Using MicroPython $MICROPYTHON_FLAVOUR/$MICROPYTHON_VERSION"
    git clone https://github.com/$MICROPYTHON_FLAVOUR/micropython "$CI_BUILD_ROOT/micropython"
    cd "$CI_BUILD_ROOT/micropython" || return 1
    git checkout $MICROPYTHON_VERSION
    git submodule update --init lib/pico-sdk
    git submodule update --init lib/cyw43-driver
    git submodule update --init lib/lwip
    git submodule update --init lib/mbedtls
    git submodule update --init lib/micropython-lib
    git submodule update --init lib/tinyusb
    git submodule update --init lib/btstack
    cd "$CI_BUILD_ROOT"
}

function ci_tools_clone {
    mkdir -p "$CI_BUILD_ROOT/tools"
    git clone https://github.com/gadgetoid/py_decl -b "$PY_DECL_VERSION" "$CI_BUILD_ROOT/tools/py_decl"
    git clone https://github.com/gadgetoid/dir2uf2 -b "$DIR2UF2_VERSION" "$CI_BUILD_ROOT/tools/dir2uf2"
}

function ci_micropython_build_mpy_cross {
    cd "$CI_BUILD_ROOT/micropython/mpy-cross" || return 1
    ccache --zero-stats || true
    CROSS_COMPILE="ccache " make
    ccache --show-stats || true
    cd "$CI_BUILD_ROOT"
}

function ci_apt_install_build_deps {
    sudo apt update && sudo apt install ccache
}

function ci_prepare_all {
    ci_tools_clone
    ci_micropython_clone
    ci_pimoroni_pico_clone
    ci_micropython_build_mpy_cross
}

function micropython_version {
    BOARD=$1
    echo "MICROPY_GIT_TAG=$MICROPYTHON_VERSION, $BOARD $TAG_OR_SHA" >> $GITHUB_ENV
    echo "MICROPY_GIT_HASH=$MICROPYTHON_VERSION-$TAG_OR_SHA" >> $GITHUB_ENV
}

function ci_cmake_configure {
    BOARD=$1
    MICROPY_BOARD_DIR=$CI_PROJECT_ROOT/boards/$BOARD
    if [ ! -f "$MICROPY_BOARD_DIR/usermodules.cmake" ]; then
        log_warning "Invalid board: $MICROPY_BOARD_DIR"
        return 1
    fi
    cmake -S $CI_BUILD_ROOT/micropython/ports/rp2 -B build-$BOARD \
    -DPICOTOOL_FORCE_FETCH_FROM_GIT=1 \
    -DPICO_BUILD_DOCS=0 \
    -DPICO_NO_COPRO_DIS=1 \
    -DUSER_C_MODULES="$MICROPY_BOARD_DIR/usermodules.cmake" \
    -DMICROPY_BOARD_DIR="$MICROPY_BOARD_DIR" \
    -DMICROPY_BOARD="$BOARD" \
    -DCMAKE_C_COMPILER_LAUNCHER=ccache \
    -DCMAKE_CXX_COMPILER_LAUNCHER=ccache
}

function ci_cmake_build {
    BOARD=$1
    ccache --zero-stats || true
    cmake --build build-$BOARD -j 2
    ccache --show-stats || true
    if [ -d "tools/py_decl" ]; then
        log_inform "Tools found, verifying .uf2 with py_decl..."
        python3 tools/py_decl/py_decl.py --to-json --verify "build-$BOARD/firmware.uf2"
    fi
    log_inform "Copying .uf2 to $(pwd)/$BOARD.uf2"
    cp build-$BOARD/firmware.uf2 $BOARD.uf2
}

log_inform "Script path: $SCRIPT_PATH"
log_inform "Project root: $CI_PROJECT_ROOT"
log_inform "Build root: $CI_BUILD_ROOT"