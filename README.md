# Inky Frame<!-- omit in toc -->

## Pico W and Pico 2 W powered ePaper display boards<!-- omit in toc -->

This repository is home to the MicroPython firmware and examples for
Inky Frame (Pico W Aboard and Pico 2 W Aboard).

- [Get Inky Frame](#get-inky-frame)
- [Download Firmware](#download-firmware)
- [Installation](#installation)
- [Useful Links](#useful-links)
- [Other Resources](#other-resources)

![Three sizes of Inky Frame displayed side-to-side.](inky-frame.png)

## Get Inky Frame

- [Inky Frame 7.3"](https://shop.pimoroni.com/products/inky-frame-7-3?variant=40541882056787)
- [Inky Frame 5.7"](https://shop.pimoroni.com/products/inky-frame-5-7?variant=40057850331219)
- [Inky Frame 4.0"](https://shop.pimoroni.com/products/inky-frame-4?variant=40443825127507)

## Download Firmware

You can find the latest release at [https://github.com/pimoroni/inky-frame/releases/latest](https://github.com/pimoroni/inky-frame/releases/latest).

There are two choices, a regular build that just updates the firmware on
your board and a "-with-examples" build which includes a ready-to-go set
of examples (everything in [examples/inkylauncher](examples/inkylauncher))
that you can interact with right on your display.

:warning: If you've changed any of the code on your board then back up before
flashing "-with-examples" - *your files will be erased!*

## Installation

1. Connect Inky Frame to your computer with a micro USB cable.
2. Put your device into bootloader mode by holding down the BOOTSEL button (on the Pico W / Pico 2 W) whilst tapping Reset (on the Inky Frame board).
3. Drag and drop the downloaded .uf2 file to the "RPI-RP2" or "RP2350" drive that appears.
4. Your device should reset, and you should then be able to connect to it using [Thonny](https://thonny.org/).
5. These builds are pre-configured for Inky Frame 7.3". If you have a different size of Inky Frame you'll need to edit `main.py` with Thonny and uncomment the line with the correct display size.

## Useful Links

- [Learn: Getting Started With Inky Frame](https://learn.pimoroni.com/article/getting-started-with-inky-frame)
- [`inky_frame` Function Reference](docs/inky_frame.md)
- [Pico Graphics Function Reference](https://github.com/pimoroni/pimoroni-pico/blob/main/micropython/modules/picographics/README.md)

## Other Resources

Links to community projects and other resources that you might find helpful can be found below. Note that these code examples have not been written/tested by us and we're not able to offer support with them.

- [Stay on schedule with Raspberry Pi Pico W and an e-ink dashboard](https://www.raspberrypi.com/news/stay-on-schedule-with-raspberry-pi-pico-w-and-an-e-ink-dashboard/)
- [Inky Frame displaying a Home Assistant dashboard with a Nextcloud Calendar](https://blog.paco.to/2023/inky-frame-lovelace-dashboard-nextcloud/)