"""
Encoding messages for MIDI.

NOTE: The docstrings and stuff are not very readable, I just wanted to test features of Python I had not used before...

Developed using https://www.cs.cmu.edu/~music/cmsip/readings/davids-midi-spec.htm

Messages with first bit as 0 are data bytes (ie. 0x0_ -> 0x7_)

Note Pitches:
60 == Middle C

All values assume little-endianness (as all data is encoded in MIDI).
"""
#######################
### GENERAL IMPORTS ###
#######################
from inspect         import signature, Parameter
from functools       import wraps
from typing          import NewType
from collections.abc import Iterable



#######################
### "LOCAL" IMPORTS ###
#######################
import sys, os
sys.path.append(os.path.dirname(__file__))

from midi_enums import ChannelIndependentMessage, ChannelSpecificMessage

_ = sys.path.pop()



####################
### CUSTOM TYPES ###
####################
_char   = NewType("char [0, 127]", int)
_int16  = NewType("int16 [0, 16383]", int)
_int_n  = NewType("tuple[_size_int_n, _int_n]", tuple[int, int])



############################
### AUXILLIARY "PACKING" ###
############################
def _encode_msg_status(value: int) -> bytes:
    """This value is unbound."""
    return bytes([value % 0xFF])



def _encode_char(value: int) -> bytes:
    """Encodes a byte of the data fields of the messages."""
    return bytes([value % 0x80])



def _encode_int(value: int) -> bytes:
    """Values use 7-bit "encodings", but stored in 8 bits. MSb is used to store 0 if data type."""
    return _encode_char((value // 0x80)) + _encode_char(value % 0x80)



def _encode_byte_n(byte_i: int, value: int) -> bytes:
    """Encode byte_i of an n_bytes encoding of value."""
    return _encode_char((value// (7**byte_i)) % 0x80)



def _encode_n_len(n_bytes: int, value: int) -> bytes:
    """Encode value using n_bytes."""
    return b''.join([_encode_byte_n(i, value) for i in reversed(range(n_bytes))])



def _check_range(val: int, lwr_bnd: int, uppr_bnd: int, err_msg: str = None):
    """Raises ValueError if val is not in [lwr_bnd, uppr_bnd]."""
    if val > uppr_bnd or val < lwr_bnd:
        raise ValueError(err_msg)



def _enc_2_chars(byte_0: int, char_1: int, char_2: int) -> bytes:
    """Encode message with 2 followup bytes from integer type inputs."""
    return _encode_msg_status(byte_0) + _encode_char(char_1) + _encode_char(char_2)



def _enc_1_chars(byte_0: int, char_1: int) -> bytes:
    """Encode message with 1 followup bytes from integer type inputs."""
    return _encode_msg_status(byte_0) + _encode_char(char_1)



def _enc_1_ints(byte_0: int, int_1: int) -> bytes:
    """Encode message with 1 followup int as bytes from integer type inputs."""
    return _encode_msg_status(byte_0) + _encode_int(int_1)



#########################
### DYNAMIC DOCSTRING ###
#########################
def _get_docstring(param: Parameter, param_desc: str) -> str:
    """Formats docstring for a given attribute."""
    if param.annotation == _char:
        type_  = '<int>'
        range_ = '[0, 127]'

    elif param.annotation == _int16:
        type_  = '<int>'
        range_ = '[0, 16383]'

    else:
        raise ValueError(f"Could not assign DocString for input parameter!\n{param}")


    if param.empty == param.default:
        name_ = f'{param.name} {type_}'

    else:
        name_ = f'[{param.name}] {type_} (default = {param.default})'


    return f"""\n\t|- {name_}:\n\t|\t{param_desc} In range of {range_}"""



########################
### MESSAGE WRAPPERS ###
########################
def _channel_specific_encoding(msg_status_byte):
    """Requires all parameters to be either position-only or keyword-only."""
    def function_wrapper(func):
        ## Store name and max value of position only params
        p_only, p_max = [], []

        ## Keep first line of docstring. Interpret each following line as docstring for a positional param.
        og_docstring      = func.__doc__.split('\n')
        new_docstring     = f"{og_docstring[0]}\n\n\tPARAMS:\n"

        ## Add docstring for channel at the very end.
        channel_docstring = """\n\t|- [channel] <int> (default = 1; KEYWORD-ONLY):\n\t|\tChannel, in range of [1, 16]."""

        ## Iterate over params
        for param in signature(func).parameters.values():
            ## Handle POSITIONAL params based on annotation in function definition
            if param.kind == param.POSITIONAL_ONLY:
                p_only.append(param.name)

                ## If 2 bytes for param, max is 2^14-1
                if param.annotation == _int16:
                    p_max.append(16383)

                ## If 1 byte for param, max is 2^7
                elif param.annotation == _char:
                    p_max.append(127)

                ## No other param types should be accepted
                else:
                    raise TypeError("Ensure all parameters have a supported annotation!")

                ## Add line(s) to new docstring for this param
                new_docstring += _get_docstring(param, og_docstring[len(p_only)])

            ## If not POSITIONAL, and not KEYWORD_ONLY, raise TypeError, as other types of params should not be accepted
            elif param.kind != param.KEYWORD_ONLY:
                raise TypeError("Ensure all parameters are KEYWORD_ONLY or POSITIONAL_ONLY!")

        ## Add channel param docstring
        new_docstring += channel_docstring

        ## Make these immutable (cause why not...)
        p_only, p_max = tuple(p_only), tuple(p_max)

        ## Add value/param checking to function, for all positional values, and channel (only KEYWORD_ONLY param).
        @wraps(func)
        def new_func(*args, channel: int = 1):
            for arg_name, arg_value, arg_max in zip(p_only, args, p_max):
                _check_range(arg_value, 0, arg_max, f"[{func.__name__}] Ensure {arg_name} is in the range [0, 127]!")

            _check_range(channel, 1, 16, f"[{func.__name__}] Ensure the channel i in the range [1, 16]!")

            ## Update channel from "numeric" to encoded format, for use as first byte...
            channel -= 1
            channel += msg_status_byte << 4
            return func(*args, channel = channel)

        ## Apply the new docstring
        new_func.__doc__ = new_docstring

        ## Return wrapped function
        return new_func
    return function_wrapper



def _channel_independent_encoding(msg_status_byte):
    def function_wrapper(func):
        p_only, p_max = [], []

        ## Keep first line of docstring. Interpret each following line as docstring for a positional param.
        og_docstring      = func.__doc__.split('\n')
        new_docstring     = f"{og_docstring[0]}\n\n\tPARAMS:\n"

        ## Docstring for VAR_POSITIONAL stuff...
        _int_n_docstring  = "\n\t|- [*args] <tuple[int, int]>:\n"\
        + "\t|\tAdditional values to send, in format of tuples.\n\t|\tFirst value is number of bytes to"\
        + " represent the value when sending it.\n\t|\tSecond value is the value to encode."\
        + "\n\t|\tThe second value must be in range [0, 2^(number_bytes)]."

        for param in signature(func).parameters.values():
            if param.kind == param.POSITIONAL_ONLY:
                p_only.append(param.name)

                ## If 2 bytes for param, max is 2^14-1
                if param.annotation == _int16:
                    p_max.append(16383)

                ## If 1 byte for param, max is 2^7
                elif param.annotation == _char:
                    p_max.append(127)

                ## No other param types should be accepted
                else:
                    raise TypeError("Ensure all parameters have a supported annotation!")

                ## Add line(s) to new docstring for this param
                new_docstring += _get_docstring(param, og_docstring[len(p_only)])

            elif param.kind == param.VAR_POSITIONAL:
                new_docstring += _int_n_docstring

            else:
                raise TypeError("Ensure values are POSITIONAL_ONLY in the channel-independent functions!")

        @wraps(func)
        def new_func(*args):
            for arg_name, arg_value, arg_max in zip(p_only, args, p_max):
                _check_range(arg_value, 0, arg_max, f"[{func.__name__}] Ensure {arg_name} is in the range [0, 127]!")

            if len(args) > len(p_only):
                for arg in args[len(p_only):]:
                    try:
                        arg_bytes, arg_value = arg

                    except TypeError:
                        raise TypeError(f"[{func.__name__}] All non-named values must be in format of [n_bytes, val]")

                    max_val = 2**(7*arg_bytes)-1
                    _check_range(arg_value, 0, max_val,
                                 f"[{func.__name__}] Ensure additional params to be encoded using ({arg_bytes}) bytes are in the range [0, {max_val}]!")

            return _encode_msg_status(msg_status_byte) + func(*args)

        new_func.__doc__ = new_docstring

        return new_func
    return function_wrapper



#######################################
### CHANNEL-SPECIFIC MESSAGE ENCODE ###
#######################################
@_channel_specific_encoding(ChannelSpecificMessage.NOTE_ON)
def note_on(pitch: _char, velocity: _char = 64, /, *, channel: int = 1) -> bytes:
    """Encode a NOTE_ON message.
Velocity of note.
Channel.
"""
    return _enc_2_chars(channel, pitch, velocity)



@_channel_specific_encoding(ChannelSpecificMessage.NOTE_OFF)
def note_off(pitch: _char, velocity: _char = 64, /, *, channel: int = 1) -> bytes:
    """Encode a NOTE_OFF message.
Pitch of note. Middle C corresponds with 60. Increase of 1 corresponds to a half-step up.
Velocity of note.
"""
    return _enc_2_chars(channel, pitch, velocity)



@_channel_specific_encoding(ChannelSpecificMessage.KEY_PRESSURE)
def key_pressure(key: _char, pressure: _char, /, *, channel: int = 1) -> bytes:
    """Encode a KEY_PRESSURE message.
Key of note. Middle C corresponds with 60. Increase of 1 corresponds to a half-step up.
Pressure of note.
"""
    return _enc_2_chars(channel, key, pressure)



@_channel_specific_encoding(ChannelSpecificMessage.CONTROLLER_CHANGE)
def controller_change(controller: _char, value: _char, /, *, channel: int = 1) -> bytes:
    """Encode a CONTROLLER_CHANGE message.
Controller sending message. Note: Values [122, 127] are reserved for special messages!
New value of controller...
"""
    return _enc_2_chars(channel, controller, value)



@_channel_specific_encoding(ChannelSpecificMessage.PROGRAM_CHANGE)
def program_change(preset: _char, /, *, channel: int = 1) -> bytes:
    """Encode a PROGRAM_CHANGE message.
Preset to swap to.
"""
    return _enc_1_chars(channel, preset)



@_channel_specific_encoding(ChannelSpecificMessage.CHANNEL_PRESSURE)
def channel_pressure(controller: _char, value: _char, /, *, channel: int = 1) -> bytes:
    """Encodes a CHANNEL_PRESSURE message.
Controller that the pressure resading is from.
Value is the pressure value measured.
"""
    return _enc_2_chars(channel, controller, value)



@_channel_specific_encoding(ChannelSpecificMessage.PITCH_BEND)
def pitch_bend(bend_amount: _int16, /, *, channel: int = 1) -> bytes:
    """Encodes a PITCH_BEND message.
The amount of bend to apply (accross notes).
"""
    return _enc_1_ints(channel, bend_amount)



##########################################
### CHANNEL-INDEPENDENT MESSAGE ENCODE ###
##########################################
@_channel_independent_encoding(ChannelIndependentMessage.SYSTEM_EXCLUSIVE)
def system_exclusive(*args: Iterable[_int_n]) -> bytes:
    """Encode a SYSTEM_EXCLUSIVE message."""
    return b''.join([_encode_n_len(n_bytes, val) for n_bytes, val in args])



@_channel_independent_encoding(ChannelIndependentMessage.SONG_POSITION)
def song_position(position: _int16, /) -> bytes:
    """Encode a SONG_POSITION message.
Position along song to go to. In song 'ticks'.
"""
    return _encode_int(position)



@_channel_independent_encoding(ChannelIndependentMessage.SONG_SELECT)
def song_select(song_number: _char, /) -> bytes:
    """Encode a SONG_SELECT message.
Song index to select.
"""
    return _encode_char(song_number)




@_channel_independent_encoding(ChannelIndependentMessage.TUNE_REQUEST)
def tune_request() -> bytes:
    """Encode a TUNE_REQUEST message."""
    return b''




@_channel_independent_encoding(ChannelIndependentMessage.END_OF_SYSEX)
def end_of_sysex() -> bytes:
    """Encodes a END_OF_SYSEX message."""
    return b''




@_channel_independent_encoding(ChannelIndependentMessage.TIMING_TICK)
def timing_tick() -> bytes:
    """Encodes a message TIMING_TICK to advance all targets to progress a tick."""
    return b''



@_channel_independent_encoding(ChannelIndependentMessage.START_SONG)
def start_song() -> bytes:
    """Encodes a message START_SONG."""
    return b''



@_channel_independent_encoding(ChannelIndependentMessage.CONTINUE_SONG)
def continue_song():
    """Encodes a message to CONTINUE_SONG."""
    return b''



@_channel_independent_encoding(ChannelIndependentMessage.STOP_SONG)
def stop_song():
    """Encodes a message to STOP_SONG."""
    return b''



@_channel_independent_encoding(ChannelIndependentMessage.ACTIVE_SENSING)
def active_sensing():
    """Encodes a message to go int ACTIVE_SENSING mode."""
    return b''



@_channel_independent_encoding(ChannelIndependentMessage.SYSTEM_RESET)
def system_reset():
    """Encodes a message for device to go into SYSTEM_RESET."""
    return b''




###########
### DEV ###
###########
# if __name__ == '__main__':
#     print(tune_request())
#     print(_encode_msg_status(ChannelIndependentMessage.SONG_SELECT))
