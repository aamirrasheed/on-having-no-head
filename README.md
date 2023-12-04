# Description
Play the [Waking Up](wakingup.com) Daily meditation using a Raspberry Pi to avoid screen usage in the morning.

Currently in outline stages.

# Construction
3D printed case that contains a Raspberry Pi Zero W, a speaker/sound driver, a power supply, and two buttons. 

* [Raspberry Pi Zero W](https://www.raspberrypi.com/products/raspberry-pi-zero-2-w/)
* 3D printed case (need to learn how to make this)
* Speaker module
* mini-HDMI to audio out, or another way to drive sound
* power supply
* Buttons

# How it works
1. Button 1 triggers a Python script.
2. Python script logs into Waking Up website and plays Daily Meditation.
3. Sound is piped from the script to the speakers.
4. Button 2 allows me to connect my computer to the Raspberry Pi to give it the Wifi password (for portability)


# How the Python Script works
1. Uses `selenium` to navigates to [wakingup.com](wakingup.com)
2. Check if user is logged in. If not, trigger magic link auth and use Gmail API to grab login link
3. Once logged in, clicks Daily Meditation, then hits play in the popup dialog
4. Network packets will contain a direct Cloudfront link to a .m4a file. 
5. Play .m4a file using `pydub`
