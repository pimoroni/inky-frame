// Board and hardware specific configuration
#define MICROPY_HW_BOARD_NAME                   "Raspberry Pi Pico W"

// Leave 848k for user filesystem
#define MICROPY_HW_FLASH_STORAGE_BYTES          (PICO_FLASH_SIZE_BYTES - (1200 * 1024))

// Enable networking.
#define MICROPY_PY_NETWORK_PPP_LWIP             (1)
#define MICROPY_PY_NETWORK_HOSTNAME_DEFAULT     "InkyW"
#include "../enable_cyw43.h"

// For debugging mbedtls - also set
// Debug level (0-4) 1=warning, 2=info, 3=debug, 4=verbose
// #define MODUSSL_MBEDTLS_DEBUG_LEVEL 1
