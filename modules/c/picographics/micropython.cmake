add_library(usermod_picographics INTERFACE)

get_filename_component(REPO_ROOT "${CMAKE_CURRENT_LIST_DIR}/../../.." ABSOLUTE)

target_sources(usermod_picographics INTERFACE
    ${PIMORONI_PICO_PATH}/micropython/modules/picographics/picographics.c
    ${PIMORONI_PICO_PATH}/micropython/modules/picographics/picographics.cpp
    ${PIMORONI_PICO_PATH}/drivers/st7789/st7789.cpp
    ${PIMORONI_PICO_PATH}/drivers/st7735/st7735.cpp
    ${PIMORONI_PICO_PATH}/drivers/sh1107/sh1107.cpp
    ${PIMORONI_PICO_PATH}/drivers/uc8151/uc8151.cpp
    ${PIMORONI_PICO_PATH}/drivers/st7567/st7567.cpp
    ${REPO_ROOT}/drivers/uc8159/uc8159.cpp
    ${REPO_ROOT}/drivers/inky73/inky73.cpp
    ${REPO_ROOT}/drivers/shiftregister/shiftregister.cpp
    ${REPO_ROOT}/drivers/psram_display/psram_display.cpp
    ${PIMORONI_PICO_PATH}/libraries/pico_graphics/pico_graphics.cpp
    ${PIMORONI_PICO_PATH}/libraries/pico_graphics/pico_graphics_pen_1bit.cpp
    ${PIMORONI_PICO_PATH}/libraries/pico_graphics/pico_graphics_pen_1bitY.cpp
    ${PIMORONI_PICO_PATH}/libraries/pico_graphics/pico_graphics_pen_3bit.cpp
    ${PIMORONI_PICO_PATH}/libraries/pico_graphics/pico_graphics_pen_p4.cpp
    ${PIMORONI_PICO_PATH}/libraries/pico_graphics/pico_graphics_pen_p8.cpp
    ${PIMORONI_PICO_PATH}/libraries/pico_graphics/pico_graphics_pen_rgb332.cpp
    ${PIMORONI_PICO_PATH}/libraries/pico_graphics/pico_graphics_pen_rgb565.cpp
    ${PIMORONI_PICO_PATH}/libraries/pico_graphics/pico_graphics_pen_rgb888.cpp
    ${PIMORONI_PICO_PATH}/libraries/pico_graphics/pico_graphics_pen_inky7.cpp
    ${PIMORONI_PICO_PATH}/libraries/pico_graphics/types.cpp
)

pico_generate_pio_header(usermod_picographics ${PIMORONI_PICO_PATH}/drivers/st7789/st7789_parallel.pio)

# usermod-common.cmake puts REPO_ROOT ahead of PIMORONI_PICO_PATH, so picographics.cpp
# resolves "drivers/<name>/<name>.hpp" to our copies
target_include_directories(usermod_picographics INTERFACE
    ${CMAKE_CURRENT_LIST_DIR}
)

target_compile_definitions(usermod_picographics INTERFACE
    -DMODULE_PICOGRAPHICS_ENABLED=1
)

target_link_libraries(usermod INTERFACE usermod_picographics)

set_source_files_properties(
    ${PIMORONI_PICO_PATH}/micropython/modules/picographics/picographics.c
    PROPERTIES COMPILE_FLAGS
    "-Wno-discarded-qualifiers"
)
