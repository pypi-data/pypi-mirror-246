#type: ignore <-- This ignores some reportGeneralTypeIssues on VS Code.
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume, IAudioEndpointVolume

def setVolume(vol=-1, max=100, force=False):
    """
    Sets the absolute volume for all apps.\n
    If the current volume is greater than `max`, current volume will be returned.\n
    `force` parameter, if True, forces all programs to be on the same volume as the master volume.
    `curvol` or `vol` always returns the master volume.
    Returns: `curvol` if `curvol > max`, else `vol` parameter, or nothing if vol or max < 0
    """
    try:
        devices = AudioUtilities.GetSpeakers() # Get the primary speaker
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None) # Do some activation
        volume = cast(interface, POINTER(IAudioEndpointVolume)) # Init the volume setters and getters
        curvol = float(round(volume.GetMasterVolumeLevelScalar() * 100)) # Get current volume in a range from 0-100, rounded.
        max = float(round(max))
        if vol < 0 or max <= 0: toggleMute(); return # Invalid cases
        if curvol > max: return curvol # Return curvol if it is greater than max
        volume.SetMasterVolumeLevelScalar(vol/100, None) # Set the master volume, in a range from 0-1
        if force: alignSounds()
        return vol
    except Exception as e: print(f"An error occured trying to setVolume: {e}")

def incVolume(inc=1, max=100, force=False):
    """
    Increments the speaker volume by `inc`.\n
    If the current volume is greater than the maximum volume, then the current volume will be returned, and nothing will be done.
    `force` parameter, if True, forces all programs to be on the same volume as the master volume.
    `curvol` always returns the master volume.
    Returns: `curvol` if `curvol > max`, else `curvol + inc`, or nothing if inc or max < 0
    """
    try:
        devices = AudioUtilities.GetSpeakers() # Get the primary speaker
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None) # Do some activation
        volume = cast(interface, POINTER(IAudioEndpointVolume)) # Init the volume setters and getters
        curvol = float(round(volume.GetMasterVolumeLevelScalar() * 100)) # Get current volume in a range from 0-100, rounded.
        max = float(round(max))
        if inc < 0 or max <= 0: return # Invalid cases
        if curvol > max: return curvol # Return curvol if it is greater than max
        volume.SetMasterVolumeLevelScalar((curvol + inc)/100, None) # Set the master volume, in a range from 0-1
        if force: alignSounds()
        return curvol + inc
    except Exception as e: print(f"An error occured trying to setVolume: {e}")

def alignSounds():
    """
    Makes all apps' sound levels to that of the master volume.\n
    Returns True or False if operations succeded.
    """
    try:
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions: # Loop through every application
            if session.Process: # To avoid NoneType Error
                volume = session._ctl.QueryInterface(ISimpleAudioVolume) # Init the volume object (this is different from the one taken from the cast() method)
                volume.SetMasterVolume(1, None) # Set the relative volume to 100% to make it equal to the master volume
        return True
    except: return False

def toggleMute(mute=True):
    """
    Mutes and unmutes the speaker.\n
    Returns True or False based on if operation succeeded.
    """
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    volume.SetMute(int(mute), None)