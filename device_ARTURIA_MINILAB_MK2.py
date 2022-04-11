# name=Arturia Minilab MKII

#import mido
import playlist 
import channels
import mixer
import patterns
import arrangement 
import ui
import transport
import device
import plugins 
import general
import launchMapPages


def print_midi_info(event):
	print("handled: {}, timestamp: {}, status: {}, data1: {}, data2: {}, port: {}, sysex: {}, midiId: {}, velocity: {}".format(event.handled, event.timestamp, event.status, event.data1, event.data2, event.port, event.sysex, event.midiId,event.velocity))


def OnMidiIn(event):
        print_midi_info(event)
        #MPC Handling pads 
        if(event.data1==60 and event.data2!=0 and event.status>144):
                channels.selectOneChannel(event.status-145)
                if event.status==160:
                        channels.selectOneChannel(event.status-160)
        #STEP SEQUENCER
        if(event.data1==61):
                if(event.status>=144):
                        channels.setGridBit(channels.channelNumber(), event.status-144, 1)
                else:
                        channels.setGridBit(channels.channelNumber(), event.status-128, 0)
        #MMC MODE PADS 5-8
        elif(event.data1==124):
                transport.setLoopMode()
        elif(event.data1==125):
                transport.globalTransport(110,1)
        elif(event.data1==126):
                transport.globalTransport(115,1)
        elif(event.data1==127):
                transport.globalTransport(113,1)
        #MMC MODE PADS 9-16
        elif(event.data1==116):
                transport.globalTransport(64,1)
        elif(event.data1==117):
                transport.globalTransport(66,1)
        elif(event.data1==118):
                transport.globalTransport(65,1)
        elif(event.data1==119):
                transport.globalTransport(67,1)
        elif(event.data1==120):
                transport.globalTransport(68,1)
        elif(event.data1==121):
                transport.globalTransport(69,1)
        elif(event.data1==122):
                transport.globalTransport(106,1)
        elif(event.data1==123):
                transport.globalTransport(20,1)
        #MPC MAIN KNOB - SCROLL EVERYTHING
        elif(event.data1==112 and event.status==176):
                #ui.setFocused(4)
                if(event.data2==63):
                        ui.previous()
                elif(event.data2==65):
                        ui.next()
        elif(event.data1==113 and event.data2==127):
                ui.enter()

        
        #Mixer Volume and Panning
        elif(event.status==176 and event.data1>=1 and event.data1<=14):
                mixer.setTrackVolume(event.data1-1,(event.data2)/127)
        elif(event.data1<=28 and event.data1>=15 and event.status==177 ):
                mixer.setTrackPan(event.data1-15,(((event.data2)*2)-126)/127)
        #Channel Mode
        elif(event.data1==29):
                channels.showCSForm(channels.channelNumber())
                channels.setChannelPan(channels.channelNumber(),(((event.data2)*2)-126)/127)
        elif(event.data1==30):
                channels.showCSForm(channels.channelNumber())
                channels.setChannelVolume(channels.channelNumber(),(event.data2)/127)
        elif(event.data1==31):
                channels.showCSForm(channels.channelNumber())
                channels.setChannelPitch(channels.channelNumber(),(((event.data2)*2)-126)/127)