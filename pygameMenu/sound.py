# coding=utf-8
"""
pygame-menu
https://github.com/ppizarror/pygame-menu

SOUND
Sound class.

License:
-------------------------------------------------------------------------------
The MIT License (MIT)
Copyright 2017-2020 Pablo Pizarro R. @ppizarror

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the Software
is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
-------------------------------------------------------------------------------
"""

from sys import stderr as _stderr
import os.path as _path
import time as _time

from pygame import error as _pygame_error
from pygame import mixer as _mixer
from pygame import vernum as _pygame_version

try:  # pygame<2.0.0 compatibility
    from pygame import AUDIO_ALLOW_CHANNELS_CHANGE as _AUDIO_ALLOW_CHANNELS_CHANGE
    from pygame import AUDIO_ALLOW_FREQUENCY_CHANGE as _AUDIO_ALLOW_FREQUENCY_CHANGE
except ImportError:
    _AUDIO_ALLOW_CHANNELS_CHANGE = False
    _AUDIO_ALLOW_FREQUENCY_CHANGE = False

__actualpath = str(_path.abspath(_path.dirname(__file__))).replace('\\', '/')
__sounddir = '{0}/resources/sounds/{1}.ogg'

# Sound types
SOUND_TYPE_CLICK_MOUSE = '__pygameMenu_sound_click_mouse__'
SOUND_TYPE_CLOSE_MENU = '__pygameMenu_sound_close_menu__'
SOUND_TYPE_ERROR = '__pygameMenu_sound_error__'
SOUND_TYPE_EVENT = '__pygameMenu_sound_event__'
SOUND_TYPE_EVENT_ERROR = '__pygameMenu_sound_event_error__'
SOUND_TYPE_KEY_ADDITION = '__pygameMenu_sound_key_addition__'
SOUND_TYPE_KEY_DELETION = '__pygameMenu_sound_key_deletion__'
SOUND_TYPE_OPEN_MENU = '__pygameMenu_sound_open_menu__'

# Sound examples
_SOUND_EXAMPLE_CLICK_MOUSE = __sounddir.format(__actualpath, 'click_mouse')
_SOUND_EXAMPLE_CLOSE_MENU = __sounddir.format(__actualpath, 'close_menu')
_SOUND_EXAMPLE_ERROR = __sounddir.format(__actualpath, 'error')
_SOUND_EXAMPLE_EVENT = __sounddir.format(__actualpath, 'event')
_SOUND_EXAMPLE_EVENT_ERROR = __sounddir.format(__actualpath, 'event_error')
_SOUND_EXAMPLE_KEY_ADDITION = __sounddir.format(__actualpath, 'key_add')
_SOUND_EXAMPLE_KEY_DELETION = __sounddir.format(__actualpath, 'key_delete')
_SOUND_EXAMPLE_OPEN_MENU = __sounddir.format(__actualpath, 'open_menu')

# Stores global reference that marks sounds as initialized
SOUND_INITIALIZED = [False]


class Sound(object):
    """
    Sound engine class.
    
    :param uniquechannel: Force the channel to be unique, this is set at the moment of creation of the object
    :type uniquechannel: bool
    :param frequency: Frequency of sounds
    :type frequency: int
    :param size: Size of sample
    :type size: int
    :param channels: Number of channels by default
    :type channels: int
    :param buffer: Buffer size
    :type buffer: int
    :param devicename: Device name
    :type devicename: basestring
    :param allowedchanges: Convert the samples at runtime, only in pygame>=2.0.0
    :type allowedchanges: bool
    :param force_init: Force mixer init with new parameters
    :type force_init: bool
    """

    # noinspection PyShadowingBuiltins
    def __init__(self,
                 uniquechannel=True,
                 frequency=22050,
                 size=-16,
                 channels=2,
                 buffer=4096,
                 devicename='',
                 allowedchanges=_AUDIO_ALLOW_CHANNELS_CHANGE | _AUDIO_ALLOW_FREQUENCY_CHANGE,
                 force_init=False):
        assert isinstance(uniquechannel, bool)
        assert isinstance(frequency, int)
        assert isinstance(size, int)
        assert isinstance(channels, int)
        assert isinstance(buffer, int)
        assert isinstance(devicename, str)
        assert isinstance(allowedchanges, int)
        assert isinstance(force_init, bool)
        assert frequency > 0, 'frequency must be greater than zero'
        assert channels > 0, 'channels must be greater than zero'
        assert buffer > 0, 'buffer size must be greater than zero'

        # Initialize sounds if not initialized
        if (_mixer.get_init() is None and SOUND_INITIALIZED[0] is False) or force_init:

            # Set sound as initialized globally
            SOUND_INITIALIZED[0] = True

            # Check pygame version
            version_major, _, version_minor = _pygame_version

            # noinspection PyBroadException
            try:
                # <= 1.9.4
                if version_major == 1 and version_minor <= 4:
                    _mixer.init(frequency=frequency,
                                size=size,
                                channels=channels,
                                buffer=buffer)

                # <2.0.0 & >= 1.9.5
                elif version_major == 1 and version_minor > 4:  # lgtm [py/redundant-comparison]
                    _mixer.init(frequency=frequency,
                                size=size,
                                channels=channels,
                                buffer=buffer,
                                devicename=devicename)

                # >= 2.0.0
                elif version_major > 1:
                    _mixer.init(frequency=frequency,
                                size=size,
                                channels=channels,
                                buffer=buffer,
                                devicename=devicename,
                                allowedchanges=allowedchanges)

            except Exception as e:
                print('sound error: ' + str(e))
            except _pygame_error as e:
                print('sound engine could not be initialized, pygame error: ' + str(e))

        # Channel where a sound is played
        self._channel = None  # type: (_mixer.ChannelType,None)
        self._uniquechannel = uniquechannel

        # Sound dict
        self._type_sounds = [
            SOUND_TYPE_CLICK_MOUSE,
            SOUND_TYPE_CLOSE_MENU,
            SOUND_TYPE_ERROR,
            SOUND_TYPE_EVENT,
            SOUND_TYPE_EVENT_ERROR,
            SOUND_TYPE_KEY_ADDITION,
            SOUND_TYPE_KEY_DELETION,
            SOUND_TYPE_OPEN_MENU
        ]
        self._sound = {}
        for sound in self._type_sounds:
            self._sound[sound] = {}

        # Last played song
        self._last_play = 0
        self._last_time = 0

        # Other (dev)
        self._verbose = True

    def get_channel(self):
        """
        Return the channel of the sound engine.

        :return: Channel
        :rtype: :py:class:`pygame.mixer.Channel`
        """
        channel = _mixer.find_channel()
        if self._uniquechannel:  # If the channel is unique
            if self._channel is None:  # If the channel has not been set
                self._channel = channel
        else:
            self._channel = channel  # Store the available channel
        return self._channel

    def set_sound(self, sound_type, sound_file, volume=0.5, loops=0, maxtime=0, fade_ms=0):
        """
        Link a sound file to a sound type.

        :param sound_type: Sound type
        :type sound_type: basestring
        :param sound_file: Sound file
        :type sound_file: basestring, NoneType
        :param volume: Volume of the sound, from 0.0 to 1.0
        :type volume: float
        :param loops: Loops of the sound
        :type loops: int
        :param maxtime: Max playing time of the sound
        :type maxtime: int, float
        :param fade_ms: Fading ms
        :type fade_ms: int, float
        :return: The status of the sound load, True if the sound was loaded
        :rtype: bool
        """
        assert isinstance(sound_type, str)
        assert isinstance(sound_file, (str, type(None)))
        assert isinstance(loops, int)
        assert isinstance(maxtime, (int, float))
        assert isinstance(fade_ms, (int, float))
        assert loops >= 0, 'loops count must be equal or greater than zero'
        assert maxtime >= 0, 'maxtime must be equal or greater than zero'
        assert fade_ms >= 0, 'fade_ms must be equal or greater than zero'
        assert 1 >= volume >= 0, 'volume must be between 0 and 1'

        # Check sound type is correct
        if sound_type not in self._type_sounds:
            raise ValueError('sound type not valid, check the manual')

        # If file is none disable the sound
        if sound_file is None:
            self._sound[sound_type] = {}
            return False

        # Check the file exists
        if not _path.isfile(sound_file):
            raise IOError('sound file "{0}" does not exist'.format(sound_file))

        # Load the sound
        try:
            sound_data = _mixer.Sound(file=sound_file)
        except _pygame_error:
            if self._verbose:
                _stderr.write('The sound format is not valid, the sound has been disabled\n')
            self._sound[sound_type] = {}
            return False

        # Configure the sound
        sound_data.set_volume(volume)

        # Store the sound
        self._sound[sound_type] = {
            'file': sound_data,
            'path': sound_file,
            'type': sound_type,
            'length': sound_data.get_length(),
            'volume': volume,
            'loops': loops,
            'maxtime': maxtime,
            'fade_ms': fade_ms,
        }
        return True

    def load_example_sounds(self, volume=0.5):
        """
        Load the example sounds provided by the package.

        :param volume: Volume of the sound, (0-1)
        :type volume: float
        :return: None
        """
        # Must be in the same order of types
        examples = [
            _SOUND_EXAMPLE_CLICK_MOUSE,
            _SOUND_EXAMPLE_CLOSE_MENU,
            _SOUND_EXAMPLE_ERROR,
            _SOUND_EXAMPLE_EVENT,
            _SOUND_EXAMPLE_EVENT_ERROR,
            _SOUND_EXAMPLE_KEY_ADDITION,
            _SOUND_EXAMPLE_KEY_DELETION,
            _SOUND_EXAMPLE_OPEN_MENU
        ]
        for sound in range(len(self._type_sounds)):
            self.set_sound(self._type_sounds[sound], examples[sound], volume=volume)

    def _play_sound(self, sound):
        """
        Play a sound.

        :param sound: Sound to be played
        :type sound: pygame.mixer.SoundType, NoneType
        :return: True if the sound was played
        :rtype: bool
        """
        if not sound:
            return False

        # Find an available channel
        channel = self.get_channel()  # This will set the channel if it's None
        if channel is None:  # The sound can't be played because all channels are busy
            return False

        # Play the sound
        time = _time.time()

        # If the previous sound is the same and has not ended (max 20% overlap)
        if sound['type'] != self._last_play or time - self._last_time >= 0.2 * sound['length'] or self._uniquechannel:
            try:
                if self._uniquechannel:  # Stop the current channel if it's unique
                    channel.stop()
                channel.play(sound['file'],
                             loops=sound['loops'],
                             maxtime=sound['maxtime'],
                             fade_ms=sound['fade_ms']
                             )
            except _pygame_error:  # Ignore errors
                pass

        # Store last execution
        self._last_play = sound['type']
        self._last_time = time
        return True

    def play_click_mouse(self):
        """
        Play click mouse sound.

        :return: None
        """
        self._play_sound(self._sound[SOUND_TYPE_CLICK_MOUSE])

    def play_error(self):
        """
        Play error sound.

        :return: None
        """
        self._play_sound(self._sound[SOUND_TYPE_ERROR])

    def play_event(self):
        """
        Play event sound.

        :return: None
        """
        self._play_sound(self._sound[SOUND_TYPE_EVENT])

    def play_event_error(self):
        """
        Play event error sound.

        :return: None
        """
        self._play_sound(self._sound[SOUND_TYPE_EVENT_ERROR])

    def play_key_add(self):
        """
        Play key addition sound.

        :return: None
        """
        self._play_sound(self._sound[SOUND_TYPE_KEY_ADDITION])

    def play_key_del(self):
        """
        Play key deletion sound.

        :return: None
        """
        self._play_sound(self._sound[SOUND_TYPE_KEY_DELETION])

    def play_open_menu(self):
        """
        Play open menu sound.

        :return: None
        """
        self._play_sound(self._sound[SOUND_TYPE_OPEN_MENU])

    def play_close_menu(self):
        """
        Play close menu sound.

        :return: None
        """
        self._play_sound(self._sound[SOUND_TYPE_CLOSE_MENU])

    def stop(self):
        """
        Stop the current the channel.

        :return: None
        """
        channel = self.get_channel()  # type: _mixer.ChannelType
        if channel is None:  # The sound can't be played because all channels are busy
            return
        try:
            channel.stop()
        except _pygame_error:
            pass

    def pause(self):
        """
        Pause the current channel.

        :return: None
        """
        channel = self.get_channel()  # type: _mixer.ChannelType
        if channel is None:  # The sound can't be played because all channels are busy
            return
        try:
            channel.pause()
        except _pygame_error:
            pass

    def unpause(self):
        """
        Unpause channel.

        :return: None
        """
        channel = self.get_channel()  # type: _mixer.ChannelType
        if channel is None:  # The sound can't be played because all channels are busy
            return
        try:
            channel.unpause()
        except _pygame_error:
            pass

    def get_channel_info(self):
        """
        Return the current channel information of the sound engine.

        :return: An info dict e.g.: {'busy': 0, 'endevent': 0, 'queue': None, 'sound': None, 'volume': 1.0}
        :rtype: dict
        """
        channel = self.get_channel()  # type: _mixer.ChannelType
        data = {}
        if channel is None:  # The sound can't be played because all channels are busy
            return data
        data['busy'] = channel.get_busy()
        data['endevent'] = channel.get_endevent()
        data['queue'] = channel.get_queue()
        data['sound'] = channel.get_sound()
        data['volume'] = channel.get_volume()
        return data
