# PyVFW
What is PyVFW?
PyVFW stands for Python Volume For Windows. Written in Python, you can use it to change, increase, mute, or unmute volume in Windows.

# Get the latest version
~~~
pip install pyvfw
~~~

# How to properly import
~~~
import pyvfw
~~~

# What modules does PyVFW use?
In the code, PyVFW uses the following modules:

`ctypes` - For accessing the `cast` and `POINTER` functions.

`comtypes` - For accessing the `CLSCTX_ALL` value.

`pycaw` - For accessing the `AudioUtilities`, `ISimpleAudioVolume`, and `IAudioEndpointVolume` values.

# Install the modules used seperately

~~~
pip install comtypes pycaw
~~~

Or, you can install it from the requirements.txt file:

~~~
pip install -r requirements.txt
~~~

# Examples
Calling `setVolume(...)`:
`vol`: The exact volume to set.

`max`: The maximum that the current volume must be in order for the new volume to be set.

`force`: determines if **all** apps' volumes should be the same as the master volume.

Actual parameters passed:

`setVolume(44)` - sets the master volume to 44.

`setVolume(44, max=40) or setVolume(44, 40)` - sets the master volume to 44, **if** the current volume is less than or equal to the max parameter.

`setVolume(44, force=True)` - sets the master volume to 44, *and* makes all applications the same volume as the master volume.

You can also use the `alignSounds` method to make all volumes the same as the master volume, without having to call `setVolume` or `incVolume`.

For example, if obs64, chrome, and msedge were all open and had these volumes:

Master Volume: 68%

obs64: 36%

Google Chrome: 64%

Microsoft Edge: 52%

And you wanted to make them all to the master volume, you could just call alignSounds, and the applications will have this now:

Speakers (Master): 68%

obs64: 68%

Google Chrome: 68%

Microsoft Edge: 68%