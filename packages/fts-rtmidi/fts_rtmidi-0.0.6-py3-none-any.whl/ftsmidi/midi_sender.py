"""A wrapper of the python-rtmidi library's MidiOut class.

Developed from following MIDI documentation:
https://www.cs.cmu.edu/~music/cmsip/readings/davids-midi-spec.htm

## MidiOut() class methods:
- delete() # Do not use...
- get_current_api() # Do not use...
- send_message(msg)

## MidiBase() class methods:
- cancel_error_callback()
- close_port()
- get_port_count()
- get_port_name(port, [encoding])
- get_ports([encoding])
- is_port_open()
- open_port(port <int>, [name])
- open_virtual_port([name]) # Only on POSIX machines...
- set_client_name(name)
- set_error_callback(function, [data])

"""
from rtmidi       import MidiOut
from .midi_format import *
from .midi_format import _int16, _int_n, _char

#############
### CLASS ###
#############
class MidiSender:
    """MidiSender is a class for sending Midi messages.

    INIT PARAMS:
    |- midi_port <str | int | rtmidi.MidiOut>:
    |   Defines what port to connect to.
    |   If str, will try to connect to port with matching name. Raises ValueError.
    |   If int, will try to connect to port with that index. Raises IndexError.
    |   If MidiOut, port must be opened. Raises ValueError.
    |   Else, raises TypeError.
    |- channel <int>:
    |   Channel to use for any channel-specific messages.
    """

    def __init__(self, midi_port: MidiOut | str | int, channel: int = 1):
        ## If an opened MidiOut, use that, assuming it has been opened
        if isinstance(midi_port, MidiOut):
            if not midi_port.is_port_open():
                raise ValueError("If giving a MidiOut instance, make sure it is connected to the appropriate port!")
            self.midi_port = midi_port

        ## If midi_port is name of port to connect to,
        ## search for it and try to connect.
        elif isinstance(midi_port, str):
            self.midi_port  = MidiOut()
            available_ports = self.midi_port.get_ports()

            ## Try to retrieve midi_port (given as name) from available_ports list
            try:
                port_index = available_ports.index( midi_port )

            except IndexError:
                available_ports = '\n- '.join(available_ports)
                raise ValueError(f"Make sure the midi_port name given is valid! Available ports include:\n{available_ports}")

            ## Open, and assert that port successfully opened
            self.midi_port.open_port(port_index)
            assert(self.midi_port.is_port_open())

        ## If midi_port is an index, open port at index midi_port
        elif isinstance(midi_port, int):
            self.midi_port = MidiOut()
            available_ports = self.midi_port.get_port_count()

            ## If mdidi_port is "out of bounds", raise IndexError
            if midi_port >= available_ports:
                raise IndexError(f"There are only {available_ports} available ports!\n{midi_port} is not valid.")

            ## Open port and assert that the port is open
            self.midi_port.open_port(midi_port)
            assert(self.midi_port.is_port_open())

        else:
            raise TypeError("midi_port is of an unsupported type!")

        self.channel = channel

    # def close_port(self) -> None:
    #     """Close port. Must not continue sending messages after this."""
    #     return self.midi_port.close_port()

    def send_message(self, msg: bytes) -> None:
        """Raw send_message method."""
        assert(self.midi_port.is_port_open())
        self.midi_port.send_message(msg)

    ################################
    ### CHANNEL-SPECIFIC METHODS ###
    ################################
    def note_on(self, pitch: _char, velocity: _char = 64) -> None:
        """Sends a NOTE_ON message."""
        return self.send_message(note_on(pitch, velocity, channel=self.channel))

    def note_off(self, pitch: _char, velocity: _char = 64) -> None:
        """Sends a NOTE_OFF message."""
        return self.send_message(note_off(pitch, velocity, channel=self.channel))

    def key_pressure(self, key: _char, pressure: _char) -> None:
        """Sends a KEY_PRESSURE message."""
        return self.send_message(key_pressure(key, pressure, channel=self.channel))

    def controller_change(self, controller: _char, value: _char) -> None:
        """Sends a CONTROLLER_CHANGE message."""
        return self.send_message(controller_change(controller, value, channel=self.channel))

    def program_change(self, preset: _char) -> None:
        """Sends a PROGRAM_CHANGE message."""
        return self.send_message(program_change(preset, channel=self.channel))

    def channel_pressures(self, controller: _char, value: _char) -> None:
        """Sends a CHANNEL_PRESSURE message."""
        return self.send_message(channel_pressure(controller, value, channel=self.channel))

    def pitch_bend(self, bend_amount: _int16) -> None:
        """Sends a PITCH_BEND message."""
        return self.send_message(pitch_bend(bend_amount, channel=self.channel))

    ###################################
    ### CHANNEL-INDEPENDENT METHODS ###
    ###################################
    def system_exclusive(self, *args: _int_n) -> None:
        return self.send_message(system_exclusive(*args))

    def song_position(self, position: _int16) -> None:
        return self.send_message(song_position(position))

    def song_select(self, song_number: _char) -> None:
        return self.send_message(song_select(song_number))

    def tune_request(self) -> None:
        return self.send_message(tune_request())

    def end_of_sysex(self) -> None:
        return self.send_message(end_of_sysex())

    def timing_tick(self) -> None:
        return self.send_message(timing_tick())

    def start_song(self) -> None:
        return self.send_message(start_song())

    def continue_song(self) -> None:
        return self.send_message(continue_song())

    def stop_song(self) -> None:
        return self.send_message(stop_song())

    def active_sensing(self) -> None:
        return self.send_message(active_sensing())

    def system_reset(self) -> None:
        return self.send_message(system_reset())

    def __del__(self):
        """Destructor... Must call midi_port.close_port() if port is open!"""
        if self.midi_port.is_port_open():
            self.midi_port.close_port()

#################
### DEBUGGING ###
#################
if __name__ == '__main__':
    from time import sleep

    print(MidiOut().get_ports())

    midi = MidiSender('ferdi-test 1')

    midi.note_on(60, 120)

    sleep(0.5)

    midi.pitch_bend(0)

    sleep(1)

    midi.note_off(60)
