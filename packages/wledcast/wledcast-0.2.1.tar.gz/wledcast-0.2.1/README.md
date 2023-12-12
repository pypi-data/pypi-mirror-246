A cross platform python application for capturing an area of your screen and streaming it to any WLED device over UDP using the DDP realtime protocol.

Maybe I just wasn't lookig very hard, but I didn't find a simple tool already existing that does this.

This was mostly created with the idea of casting to an LED matrix in mind, but there's no reason you couldn't use it to cast to a strip or an alien covered in strips. 
You'd just need to use your imagination a bit more to work out what mapped where.

There are loads of cool visualisations on youtube etc that look good even at relatively low resolution

Issues and PRs are welcomed. This is still alpha at the moment. I have only really tested on windows but theoretically it should work on linux and MacOS too.

### Features
- Autodiscovers WLED devices on your network. Choose which to cast to.
- Pick a window to cast
- The aspect ratio of the wled configuration is autodiscovered and applied to the casting area
- Filters for saturation, contrast, brightness, sharpness and rgb balance are included. The values can be edited in the console menu on the fly while casting.
  Scale r, g, b down (ie less than 1) if you need sp you as not to have values overflow and clip. The default values work well for the 16x16 matrices from Aliexoress I have, but experiment as there is no doubt variation
- The area being cast is clearly displayed with a red border
- Move and scale the capture area with the keyboard  (Ctrl + arrows to move, Alt+arrows to scale). Alternatively left click on the red border to drag it around, right click and move up/down to scale.
- Decent performance - I get around 60-65fps with all filters enabled with the fps limiter off. This is really a little too fast for WS2812bs if you have a quite a few on a pin, so the fps is limited to 25 by default

### Options (none required)
| Option                    | Desctription                                                                                                      |
|:--------------------------|:------------------------------------------------------------------------------------------------------------------|
| --title TITLE             | Cast the window whost title contains TITLE                                                                        |
| --fps FPS                 | Limit fps to FPS. 500 LEDS per GPIO is stable up to around 40Hz on and ESP32-WROOM for me but YMMV. Default 30    |
| --host HOST               | Skip network discovery and cast to this IP address                                                                |
| --live-preview            | Show the output in a preview pane on the computer                                                                 |
| --search-timeout TIMEOUT  | Timeout for WLED network discovery, defaults to 3s. Increase if your latency is higher and devices are not found. |
| --capture-method [METHOD] | Default mss works well on all platforms. dxcam is faster but only supports windows on primary monitor             |
| --monitor [NUMBER]        | Cast a monitor rather than a window. Optionally pass the monitor number, else you'll be asked                     |
| --debug                   | Endable debug logs                                                                                                |

To implement:
--output-resolution     Skip resolution discovery from WLED and use this (format 64x32)
### Installation
______
Requires Python >=3.10. Create and activate a conda/venv, If you aren't sure how, I recommend [micromamba (install here)](https://mamba.readthedocs.io/en/latest/installation/micromamba-installation.html)  as it's very lightweight and fast:
```shell
micromamba create -n wledcast -c conda-forge python=3.11
micromamba activate wledcast
```

#### With pip (recommended)
```shell
pip install wledcast
wledcast
```
Or if you are on windows and want to use the DirectX capture method:
```shell
pip install wledcast[dxcam]
wledcast
```

#### From source (developers/contributors)
Clone the repo, install the package (editable):
```shell
git clone https://github.com/ppamment/wledcast.git
cd wledcast
pip install -e .
wledcast
```

### Not working?
______
#### ImportError: DLL load failed
You probably need to install the Visual C++ 2015 runtime. You can find it here:

https://www.microsoft.com/en-us/download/details.aspx?id=53840

### Licence
______
GPLv3, See the LICENCE file
