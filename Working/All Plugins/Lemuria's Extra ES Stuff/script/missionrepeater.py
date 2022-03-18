import input.missionrepeaterinput as inpt

def main():
    numtimes_repeat = int(input('How many times to repeat? '))
    mission_repeater(numtimes_repeat)

def mission_repeater(numtimes_repeat):
    for i in range(1,numtimes_repeat+1):
        inpt.printMission(i)

if __name__ == '__main__':
    main()