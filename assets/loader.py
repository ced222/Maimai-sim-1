#assets/loader.py
import os
import math
import sprites
chart = [['note', 0, 0, False, False],['note', 1, 0, False, False],['note', 2, 0 , False, False],['slide', 3, 0, 3, 2, [1,2,3,4,5], False, False],['slide', 3, 0, 3, 3, [1,2,3,4,5], False, False]]
'''
def load(type, chart):
    for i in chart:
        type = i['type']
        if type == 'slide':
            note = [type, i[1], i[2], i[3], i[4], i[5], i[6], i[7]]
        elif type == 'note':
            note = [type, i[1], i[2], i[3]]
        elif type == 'hold':
            note = [type, i[1], i[2], i[3], i[4]]

def save(chart):
    with open('./test.csv', 'w') as f:
        f.write('#Python MAIMAI simulator chart file\n')
        f.write('#Version 0.1 \n\n')
        for i in chart:
            line = ''
            for j in i[:-1]:
                line += f'{j},'
            line += str(i[-1])
            line += '\n'
            f.write(line)
def open(file):
    with open(file, 'r') as f:
        line = f.readline()
        if f.readline().list()[0] == '#':
            pass
        else:
            pass


# [type, bar, bar_fraction, button_start, button_end, duration, [cord], break, double] #slide
# [type, bar, bar_fraction, button, break, double] #note
# [type, bar, bar_fraction, button, duration, break, double] #hold


def phraseHold(speed : float, button : int, beat : int, duration : float, breaknote, doublenote, timesig , bar) -> list:
    # bolierplate code that hopefully works
    # splits the hold into 3 parts
    # head body and tail
    # head is the start of note
    # body is the note every 0.1 of the duration
    # tail is the ending of the note

    head = ['hold-head', bar, beat , 0, button, breaknote, doublenote]
    body = []

    for i in range(1, int(duration*10)):
        # detect if note goes over one bar
        beatoffset = beat + i/10
        if beatoffset > timesig:
            beatoffset -= int(beatoffset/timesig) + beatoffset % timesig
            baroffset = int(beatoffset/timesig)
        else:
            baroffset = 0
        
        body.append(['hold-body', baroffset, beatoffset, 0, button, breaknote, doublenote])
    
    end = ['hold-end', beat + duration, 0, button, breaknote, doublenote]

    
    
    return head+body+end'''

['(119){1}', '{4}3', '3', '4', '4', '{4}5', '5', '6', '', '{4}7', '7', '8', '8', '{4}1', '1', '2', '', '{4}3', '3/4', '3', '3/4', '{4}6', '5/6', '6', '5/6', '{4}4/5', '3/6', '4/5', '3/6', '{4}4/5', '3/6', '2b/7b', '', '{4}5/6', '5/6', '3/4', '3/4', '{4}5/6', '3/4', '5b/6b', '', '{4}3/4', '3/4', '5/6', '5/6', '{4}3/4', '5/6', '3b/4b', '', '{4}6h[4:1]', '5', '6h[4:1]', '5', '{4}3h[4:1]', '4', '3h[4:1]', '4', '{4}6h[4:1]', '5', '6h[4:1]', '5', '{4}3h[4:1]', '4', '4/5', '', '{4}7/8', '7/8', '1/2', '1/2', '{4}7/8', '1/2', '7b/8b', '', '{4}1/2', '1/2', '7/8', '7/8', '{4}1/2', '7/8', '1b/2b', '', '{4}7h[4:1]', '8', '7h[4:1]', '8', '{4}2h[4:1]', '1', '2h[4:1]', '1', '{4}7h[4:1]', '8', '7h[4:1]', '8', '{4}2h[4:1]', '1', '1/8', '', '{4}3h[4:3]', '', '4', '4', '{4}6h[4:3]', '', '5', '5', '{4}7h[4:3]', '', '8', '8', '{4}2h[4:3]', '', '1', '1', '{4}8', '8', '7', '7', '{4}6', '6', '5', '5', '{4}4', '4', '3', '3', '{4}2', '2', '1h[4:1]', '8b', '{4}1', '2', '3', '4', '{4}5', '6', '7', '1/8', '{4}8', '7', '6', '5', '{4}4', '3', '2', '1/8', '{4}8', '1/7', '8', '1/7', '{4}1', '2/8', '1', '2/8', '{4}8', '1/7', '1', '2/8', '{4}1/8', '2/7', '3b/6b', '', '{1}3-8[2:1]/4-7[2:1]', '{4}1', '1', '2h[4:1]', '', '{1}1-6[2:1]/2-5[2:1]', '{4}7', '7', '8h[4:1]', '', '{4}8', '7', '6', '5', '{4}1', '2', '3', '4', '{4}4/5', '3/6', '4/5', '3/6', '{4}2/7', '2/7', '2b/7b', '', '{4}7/8', '1/6', '1/2', '3/8', '{4}7/8', '1/2', '7b/8b', '', '{4}1/2', '3/8', '7/8', '1/6', '{4}1/2', '7/8', '1b/2b', '', '{4}7h[4:1]', '8', '2h[4:1]', '1', '{4}7h[4:1]', '8', '2h[4:1]', '1', '{4}1/8', '1/8', '2/7', '2/7', '{4}1/8', '2/7', '3b/6b', '', '{4}3/4', '2/5', '5/6', '4/7', '{4}3/4', '5/6', '3b/4b', '', '{4}5/6', '4/7', '3/4', '2/5', '{4}5/6', '3/4', '5b/6b', '', '{4}3h[4:1]', '4', '6h[4:1]', '5', '{4}3h[4:1]', '4', '6h[4:1]', '5', '{4}4/5', '4/5', '3/6', '3/6', '{4}4/5', '3/6', '2b/7b', '', '{4}8', '8', '1', '1', '{4}2', '2', '3', '', '{4}4', '4', '5', '5', '{4}6', '6', '7', '', '{4}2', '1/2', '2', '1/2', '{4}7', '7/8', '7', '7/8', '{4}1/8', '2/7', '1/8', '2/7', '{4}1/8', '2/7', '3b/6b', '', '{1}', '{1}', '{1}', 'E'] 


# def phraseBar(bar):
#     print(bar)
#     if '(' in bar and ')' in bar:
#         bpm = bar[1:bar.index(')')]
#     timesig = bar[bar.index('{'):bar.index('}')]

#     notes = bar.split(',')
#     print(notes)
#     bar = {
#         'bpm': bpm, #beats per minute, to get time
#         'timesig':timesig, #number e.g. 4. Fraction is always out of 4 (4)quarter notes so 7 would be 7/4 time signature            
#         'notes':notes, #list type
#         }
#     return bar
    
def phrase_simai(chart, diffcuilty, speed):
    chart = chart.split('\n')
    bpm = 120
    
    phrasedchart = []
    barNumber = 0
    for bar in chart:
        if bar == '':
            continue
        if 'E' in bar:
            continue
        if '(' in bar and ')' in bar:
            bpm = bar[1:bar.index(')')]
            bar = bar[bar.index(')')+1:]

        try:
            timesig = bar[bar.index('{')+1:bar.index('}')]
            bar = bar[:bar.index('{')] + bar[bar.index('}')+1:]
        except ValueError:
            print(bar)
            exit()
        

        barFraction = 0
        
        notes = bar.split(',')
        notes = notes[:-1]
        phrasednotes = []
        for i in notes:
            isbreak = False
            isdouble = False
            if 'b' in i:
                isbreak = True
                while True:
                    try:
                        i = i[:i.index('b')] + i[i.index('b')+1:]
                    except:
                        break
            if '/' in i:
                isdouble = True
                j = i
                i = j.split('/')[1]
                if len(i) == 1:
                    note = TapNote()
                    try:

                        note.buttonNumber = int(i) - 1
                    except:
                        continue
                    note.barNumber = barNumber
                    note.barFraction = barFraction
                    
                    note.sprite[0] = sprites.TapNote(note.buttonNumber)
                    note.breakNote = isbreak
                    note.doubleNote = isdouble
                    if isdouble:
                        note.sprite[0].double()
                    phrasednotes.append(note)
            
                if 'h' in i:
                    note = HoldNote(divider = int(i.split(':')[0][-1]), duration = int(i.split(':')[1][0]), timeSig = int(timesig))

                    try:
                        note.buttonNumber = int(i[0]) - 1
                    except:
                        continue
                    note.barNumber = barNumber
                    note.barFraction = barFraction
                  

                    note.timeSig = timesig
                    note.sprite[0] = sprites.HoldHead(note.buttonNumber)
                    note.sprite[1] = sprites.HoldTail(note.buttonNumber)
                    note.sprite[2]  = sprites.HoldBody(note.buttonNumber, note.holdDuration, speed=speed,bpm=bpm)
                    note.breakNote = isbreak
                    note.doubleNote = isdouble
                    if isdouble:
                        note.sprite[0].double()
                        note.sprite[1].double()
                        note.sprite[2].double()
                    phrasednotes.append(note)
                i = j.split('/')[0]
            if len(i) == 1:
                note = TapNote()
                try:
                    note.buttonNumber = int(i) - 1
                except:
                    continue
                note.barNumber = barNumber
                note.barFraction = barFraction
                note.sprite[0] = sprites.TapNote(note.buttonNumber)
                note.breakNote = isbreak
                note.doubleNote = isdouble
                if isdouble:
                    note.sprite[0].double()
                phrasednotes.append(note)
           
            if 'h' in i:
                note = HoldNote(divider = int(i.split(':')[0][-1]), duration = int(i.split(':')[1][0]), timeSig = int(timesig))
                try:
                    note.buttonNumber = int(i[0]) - 1
                except:
                    continue
                note.barNumber = barNumber
                note.barFraction = barFraction
                note.divider = int(i.split(':')[0][-1])
                note.duration = int(i.split(':')[1][0])
                
                note.timeSig = timesig
                note.sprite[0] = sprites.HoldHead(note.buttonNumber)
                note.sprite[1] = sprites.HoldTail(note.buttonNumber)
                note.sprite[2]  = sprites.HoldBody(note.buttonNumber, note.holdDuration, speed, bpm)
                note.breakNote = isbreak
                note.doubleNote = isdouble
                if isdouble:
                    note.sprite[0].double()
                    note.sprite[1].double()
                    note.sprite[2].double()
                phrasednotes.append(note)
            
            

            barFraction += 1
            # print(barFraction, barNumber, timesig)
        
        bar = {
            'bpm': int(bpm), #beats per minute, to get time
            'timesig': int(timesig), #number e.g. 4. the number is the note divider, e.g. 4 would be a quarter note and 2 is half notes. this means that some parts BPM may be in terms of half notes or quarter notes or whatever other division you have    
            'notes':phrasednotes, #list type
            }
        phrasedchart.append(bar)
        barNumber += 1
    

    
    return phrasedchart

class Note:
    def __init__(self):
        self.buttonNumber = 0 #from 0 to 7
        self.barNumber = 0
        self.barFraction = 0 #depends on time signature, from 0 to (time signature-1). 
        self.breakNote = False #false or true, breaknotes provide extra points
        self.doubleNote = False #if true then graphics is yellow
        self.sprite = [None]

class TapNote(Note):
    name = 'TapNote'
    def __init__(self):
        super().__init__()
    


class HoldNote(Note):
    name = 'HoldNote'
    def __init__(self, divider, duration, timeSig):
        super().__init__()
        self.divider = divider #1 is whole note, 2 is half note, 4 is quarter note, 8 is eigth note etc.
        self.duration = duration #how many "notes" of duration. e.g. 1 divider and 2 duration would be 2 whole notes whilst 2 divider 4 duation would be 4 half notes
        self.timeSig = timeSig
        #time signature for the current bar
        self.headSprite = None #head of hold note

        self.holdDuration = self.timeSig/4 * 4/self.divider * self.duration * 16 #duration is in 1/16th per-comma length (per-comma length is basically a quarter note unit) or whatever the defined unit is
        self.tailSprite = None #tail of hold note
        self.elapsedDuration = 1 #in 1/16th of notes
        self.bodySprite = None
        self.sprite = [self.headSprite, self.tailSprite, self.bodySprite]
        self.issegment = False
    def segment(self):
        # return a new segment sprite
        # issegment used to reduce cpu and memory usage, only return every two checks i.e. every 1/8th beat
        self.bodySprite = False
        
        if self.issegment:
            self.sprite[2] = (self.bodySprite)
            if self.doubleNote:
                self.bodySprite.double()
            self.issegment = False
        else:
            self.issegment = True
        
         #segment of hold note

class SlideNote(HoldNote):
    def __init__(self):
        super().__init__()
        self.pattern = ""
        self.duration = 0 #duration is in 1/16th beat or whatever the defined unit is
        self.destinationButton = 0 #button where the slide ends
        self.starGraphic = None #is the star graphic 
        self.arrowGraphic = None #is the graphic of the arrow from the star arrival button to destination button

class TouchNote():
    def __init__(self):
        pass


chart = '''
(119){1},
{4}3,3,4,4,
{4}5,5,6,,
{4}7,7,8,8,
{4}1,1,2,,
{4}3,3/4,3,3/4,
{4}6,5/6,6,5/6,
{4}4/5,3/6,4/5,3/6,
{4}4/5,3/6,2b/7b,,
{4}5/6,5/6,3/4,3/4,
{4}5/6,3/4,5b/6b,,
{4}3/4,3/4,5/6,5/6,
{4}3/4,5/6,3b/4b,,
{4}6h[4:1],5,6h[4:1],5,
{4}3h[4:1],4,3h[4:1],4,
{4}6h[4:1],5,6h[4:1],5,
{4}3h[4:1],4,4/5,,
{4}7/8,7/8,1/2,1/2,
{4}7/8,1/2,7b/8b,,
{4}1/2,1/2,7/8,7/8,
{4}1/2,7/8,1b/2b,,
{4}7h[4:1],8,7h[4:1],8,
{4}2h[4:1],1,2h[4:1],1,
{4}7h[4:1],8,7h[4:1],8,
{4}2h[4:1],1,1/8,,
{4}3h[4:3],,4,4,
{4}6h[4:3],,5,5,
{4}7h[4:3],,8,8,
{4}2h[4:3],,1,1,
{4}8,8,7,7,
{4}6,6,5,5,
{4}4,4,3,3,
{4}2,2,1h[4:1],8b,
{4}1,2,3,4,
{4}5,6,7,1/8,
{4}8,7,6,5,
{4}4,3,2,1/8,
{4}8,1/7,8,1/7,
{4}1,2/8,1,2/8,
{4}8,1/7,1,2/8,
{4}1/8,2/7,3b/6b,,
{1}3-8[2:1]/4-7[2:1],
{4}1,1,2h[4:1],,
{1}1-6[2:1]/2-5[2:1],
{4}7,7,8h[4:1],,
{4}8,7,6,5,
{4}1,2,3,4,
{4}4/5,3/6,4/5,3/6,
{4}2/7,2/7,2b/7b,,
{4}7/8,1/6,1/2,3/8,
{4}7/8,1/2,7b/8b,,
{4}1/2,3/8,7/8,1/6,
{4}1/2,7/8,1b/2b,,
{4}7h[4:1],8,2h[4:1],1,
{4}7h[4:1],8,2h[4:1],1,
{4}1/8,1/8,2/7,2/7,
{4}1/8,2/7,3b/6b,,
{4}3/4,2/5,5/6,4/7,
{4}3/4,5/6,3b/4b,,
{4}5/6,4/7,3/4,2/5,
{4}5/6,3/4,5b/6b,,
{4}3h[4:1],4,6h[4:1],5,
{4}3h[4:1],4,6h[4:1],5,
{4}4/5,4/5,3/6,3/6,
{4}4/5,3/6,2b/7b,,
{4}8,8,1,1,
{4}2,2,3,,
{4}4,4,5,5,
{4}6,6,7,,
{4}2,1/2,2,1/2,
{4}7,7/8,7,7/8,
{4}1/8,2/7,1/8,2/7,
{4}1/8,2/7,3b/6b,,
{1},
{1},
{1},
E'''

# (phrase_simai(chart))