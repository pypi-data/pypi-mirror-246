"""
Status Byte Enum for messages in MIDI.

Developed using https://www.cs.cmu.edu/~music/cmsip/readings/davids-midi-spec.htm

"""
from enum      import IntEnum

#####################
### MESSAGE ENUMS ###
#####################
class ChannelSpecificMessage (IntEnum):
    """First 4 bits of first byte are used, following 4 bits indicate channel."""
    # MESSAGE STATUS NAME = BYTE # [*DataBytes]
    NOTE_OFF          = 0x8 # [pitch, velocity]
    NOTE_ON           = 0x9 # [pitch, velocity]
    KEY_PRESSURE      = 0XA # [key,   pressure]
    CONTROLLER_CHANGE = 0XB # [controller, value]
    PROGRAM_CHANGE    = 0XC # [preset]
    CHANNEL_PRESSURE  = 0XD # [pressure]
    PITCH_BEND        = 0XE # [bend_LSB, bend_MSB]

class ChannelIndependentMessage (IntEnum):
    """All 8 bits are used for status."""
    # MESSAGE STATUS NAME = BYTE # [*DataBytes]
    SYSTEM_EXCLUSIVE      = 0XF0 # [*any]
    SONG_POSITION         = 0XF2 # [position_LSB, position_MSB]
    SONG_SELECT           = 0XF3 # [song_number]
    UNOFFICIAL_BUS_SELECT = 0xF5 # [bus_number]
    TUNE_REQUEST          = 0XF6 # []
    END_OF_SYSEX          = 0xF7 # []
    TIMING_TICK           = 0XF8 # []
    START_SONG            = 0XFA # []
    CONTINUE_SONG         = 0XFB # []
    STOP_SONG             = 0XFC # []
    ACTIVE_SENSING        = 0XFE # []
    SYSTEM_RESET          = 0XFF # []

########################
### CONTROLLER ENUMS ###
########################
class Controller (IntEnum):
    MODULATION_WHEEL  = 0x01
    BREATH_CONTROLLER = 0x02
    FOOT_CONTROLLER   = 0x04
    PORTAMENTO_TIME   = 0x05
    DATA_ENTRY_SLIDER = 0x06
    MAIN_VOLUME       = 0X07
    BALANCE           = 0X08
    PAN               = 0X0A
    EXPRESSION        = 0x0B
    GEN_PURPOSE_1     = 0x10
    GEN_PURPOSE_2     = 0x11
    GEN_PURPOSE_3     = 0x12
    GEN_PURPOSE_4     = 0x13
    # 0x20 - 0x3F Reserved... (LSB for above...)
    DAMPER_PEDAL      = 0x40 # Toggleable
    PORTAMENTO        = 0x41 # Toggleable
    SOSTENUTO         = 0x42 # Toggleable
    SOFT_PEDAL        = 0x43 # Toggleable
    HOLD_2            = 0x45 # Toggleable
    GEN_PURPOSE_5     = 0x50
    GEN_PURPOSE_6     = 0x51
    GEN_PURPOSE_7     = 0x52
    GEN_PURPOSE_8     = 0x53
    TREMOLO_DEPTH     = 0x5C
    CHORUS_DEPTH      = 0X5D
    DETUNE_DEPTH      = 0X5E
    PHASER_DEPTH      = 0X5F
    DATA_INCREMENT    = 0X60
    DATA_DECREMENT    = 0X61
    NON_REG_PARAM_LSB = 0X62
    NON_REG_PARAM_MSB = 0X63
    REG_PARAM_LSB     = 0X64
    REG_PARAM_MSB     = 0x65
    CHANNEL_MODE_1    = 0X7A
    CHANNEL_MODE_2    = 0X7B
    CHANNEL_MODE_3    = 0X7C
    CHANNEL_MODE_4    = 0X7D
    CHANNEL_MODE_5    = 0X7E
    CHANNEL_MODE_6    = 0X7F
