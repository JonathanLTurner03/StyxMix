# <h1 align="center">StyxMix</h1>
<h3 align="center">A Simple Solution To An Annoying Problem</h3>
<p align="center">
<img src="">
</p>

---
## Description

### :cd: What is StyxMix?
StyxMix is a simple solution to a problem that many people face. It is a software that allows for the manipulation of 
the Windows Audio Mixer utilizing an RP Zero 2W. This software is designed to be simple and easy to implement and 
replicate. It utilizes popular python libraries such as [`pycaw`](https://github.com/AndreMiras/pycaw), 
[`pyzmq`](https://github.com/zeromq/pyzmq), and [`zeroconf`](https://github.com/wmcbrine/pyzeroconf) to facilitate an
easy-to-use network pairing, binding, and core audio control system. 

---
### :floppy_disk: Background
Why the name StyxMix? It is not named after the band Styx, which I didn't even know of until I already began this project.
Most of my projects are named after some Mythology being/creature/place. In this case, it is named after the River Styx
from Greek Mythology. Along with the fact that this project is a mixer, it seemed fitting to name it StyxMix.

The idea for this project was due to the fact that different games and applications like to play volume at wildly
different levels. This can be annoying when you are trying to listen to music and play a game at the same time. 

While some headphones and interfaces have the ability to map applications to different channels, most do not. Along with
this, some ways to accomplishing this goal require you to change your default audio device, which can be annoying
and problematic if you are utilizing an Audio Interface.

---
### :level_slider: Why not [deej](https://github.com/omriharel/deej)?
When researching to find a solution that did a potential fix for this issue, I came across deej. deej is a great project
that does exactly what I wanted to do. However, it is designed to be used with an Arduino, or a microcontroller that can
be programmed to act as a HID device. While this is a great solution, there are a few caveats with this project in my
situation. 

Firstly, I wanted to allow wireless and wired connection, along with the ability to switch between devices. Secondly, 
the project hasn't been updated in quite a long time as far as I can tell. This means that it may not work with
newer versions of Windows, or may have bugs that have been fixed in newer versions of Go. Along with that, I wanted 
to develop the project in Python to allow for more platform independent development with the potential ability to support 
Linux in the future.

---
## :construction: Road Maps
This roadmap is a high-level overview of the features and enhancements that are planned for StyxMix. It is subject to 
change and will be updated as new features are added, and others are completed. The way these features are implemented 
may depend on version to version depending on the features of the library.

---
### Functionality
|   Status   |          Feature           |                            Description                             | Implemented in |
|:----------:|:--------------------------:|:------------------------------------------------------------------:|:--------------:|
| :pushpin:  | Windows Audio Manipulation |      Allows for the manipulation of the Windows Audio Mixer.       |      :x:       |
| :calendar: |     Multiple Channels      | Allows for multiple Rotary Encoders to control different channels  |      :x:       |
| :calendar: |  Remote Changes to Config  | Allows for changes to the configuration file from the host device. |      :x:       |
| :calendar: |       Multiple Hosts       |      Allows for multiple hosts to connect to the same device.      |      :x:       |

---
### Features
|       Status       |   Feature    |                           Description                           | Implemented in |
|:------------------:|:------------:|:---------------------------------------------------------------:|:--------------:|
| :white_check_mark: | Auto Pairing |            Allows for dynamic discovery and binding.            |  1.0.0-alpha   |
|     :calendar:     | Auto Update  |             Automatically updates the application.              |      :x:       |
|     :calendar:     |  Auto Start  |              Automatically starts the application.              |      :x:       |
|     :calendar:     |     GUI      | Allows for easy changing of configuration files within windows. |      :x:       |

---
### Compatibility
|   Status   |    Feature    |                       Description                       | Implemented in |
|:----------:|:-------------:|:-------------------------------------------------------:|:--------------:|
| :pushpin:  |  Windows 10   | Allows for the manipulation of the Windows Audio Mixer. |  1.0.0-alpha   |
| :calendar: | Linux Support |          Allows for the manipulation of ALSA.           |      :x:       |
| :calendar: | MacOS Support |        Allows for the manipulation of CoreAudio.        |      :x:       |

---
### :gear: Deployment / Installation
This section will be updated as the project progresses. The deployment and installation process will be detailed here.