# Description: This module is used to control the audio device on Windows.
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


class AudioController:
    audio_devices = None
    interface = None
    volume = None

    # Initializes the audio device, interface, and volume
    def __init__(self):
        self.audio_devices = AudioUtilities.GetSpeakers()
        self.interface = self.audio_devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self.volume = self.interface.QueryInterface(IAudioEndpointVolume)

    # Returns the current volume of the audio device
    def is_mute(self) -> bool:
        return True if self.volume.GetMute() else False

    # Toggles the mute state of the audio device
    def toggle_mute(self) -> None:
        self.volume.SetMute(not self.is_mute(), None)

    # Sets the volume of the audio device
    def set_volume(self, percent) -> None:
        scalar_volume = percent / 100.0  # convert percentage to scalar
        self.volume.SetMasterVolumeLevelScalar(scalar_volume, None)

    # Gets the current volume of the audio device
    def get_volume(self) -> int:
        return self.volume.GetMasterVolumeLevelScalar() * 100

    # Increases the volume of the audio device
    def increase_volume(self, percent) -> None:
        scalar_volume = self.get_volume() + (percent / 100.0)
        self.volume.SetMasterVolumeLevelScalar(scalar_volume, None)

    # Decreases the volume of the audio device
    def decrease_volume(self, percent) -> None:
        scalar_volume = self.get_volume() - (percent / 100.0)
        self.volume.SetMasterVolumeLevelScalar(scalar_volume, None)
