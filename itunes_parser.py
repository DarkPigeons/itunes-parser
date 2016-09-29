import re, argparse, math
import sys, os
import matplotlib.pyplot as plt
import plistlib
import numpy


'''
sizes = []
sizes.append(round(track_info["Size"] / 80000)) # megabytes
len(sizes) == 0 or
'''

def find_duplicates(file_name):
    '''
    file_name: path to xml file containing itunes library information
    '''
    with open(file_name, "rb") as file: # open file, rb opens binary file in binary
        plist = plistlib.load(file)  # return a dictionary from binary file object

    track_ids = [] # contains track ids
    track_names = [] # contains track names
    track_times = [] # contains track times in seconds
    duplicates = [] # contains tuples of tracks and the number of times they are found in our library
    count = 1 # base count

    for track_id, track_info in plist["Tracks"].items(): #  append ids, names, and times to various lists
        try:
            track_ids.append(track_id) # append each id
            track_names.append(track_info['Name']) # append each name
            track_times.append(track_info['Total Time']/1000) # append times change milliseconds to seconds by 1000 div
        except:
            pass

    for track_id1, track_info1 in plist["Tracks"].items(): # reiterate of tracks to locate duplicates
        # if track is not already in duplicates and it is in our list of names more than once...
        try:
            if (track_id1 not in duplicates) and (track_names.count(track_info1['Name']) > 1):
                duplicates.append((track_info1['Name'], track_names.count(track_info1['Name']))) # append name and count
        except:
            pass


    if len(duplicates) > 0: # if there are more than one duplicates, we will write them to dups.txt
        print("%d duplicates tracks found" % len(duplicates))
        with open("dups.txt", "w") as duplicates_file: # write in duplicates to dups.txt
            for val in duplicates:
                duplicates_file.write("%s [%d]" % (val[0], val[1]))
                duplicates_file.write("\n")
    else:
        print("No duplicates found")

    '''
    with open("dups.txt", "r") as dup:
            content = dup.read()
            print(content)
    '''


def find_common_tracks(file_names):
    '''
    file_names: list of playlist filenames [users/arnav/playlist1, users/arnav/playlist2]
    '''
    track_name_sets = []

    for file_name in file_names:
        track_names = set()
        plist = plistlib.readPlist(file_name)
        tracks = plist["Tracks"]
        for track_id, track_info in tracks.items():
            try:
                track_names.add(track_info["Name"])
            except:
                pass
            track_name_sets.append(track_names)

    common_tracks = set.intersection(*track_name_sets) # find tracks common in multiple playlsts

    if len(common_tracks) >= 1: # if more than one common track
        with open("common.txt", "wb") as common_file: # write common tracks to common.txt
            for val in common_tracks:
                common_file.write(("%s\n" % val).encode("UTF-8"))
        print("%d common tracks found. Written to common.txt" % len(common_tracks))
    else:
        print("No common tracks found between playlists")


def plotDurations(file_name):
    '''
    file_name: path to xml containing file_information
    plotStats: gather info and plot statistics for files
    '''
    plist = plistlib.readPlist(file_name)
    tracks = plist["Tracks"]
    durations = []

    for track_id, track_info in tracks.items():
        try:
            durations.append(track_info["Total Time"]) # seconds
        except:
            pass

    if len(durations) == 0:
        print("No valid album times in %s" % file_name)
        return None

    orgx = numpy.array(durations, numpy.int32)

    y = []
    for i in orgx:
        y.append(round(i / 60000)) # converts to minutes
    y.sort()

    x = [] # durations in minutes
    for i in range(math.trunc(y[0]), math.ceil(y[len((y))-1])):
        x.append(i)
    print(x)
    print(y)

    plt.hist(x, y, histtype = "bar", color = "green", rwidth = 1)
    plt.title("ITunes Track Lengths")
    plt.xlabel("Minutes Long")
    plt.ylabel("Number of Tracks")
    plt.show()

def largestSizeFile(file_name):
    plist = plistlib.readPlist(file_name)
    tracks = plist["Tracks"]
    durations = {}
    print(tracks)
    for track_id, track_info in tracks.items():
        if 1==1:
            print(1)


largestSizeFile("/Users/arnavmahajan/Desktop/pp-master/playlist/test-data/pl1.xml")

#plotDurations("/Users/arnavmahajan/Desktop/pp-master/playlist/test-data/pl1.xml")

# find_common_tracks(["/Users/arnavmahajan/Desktop/pp-master/playlist/test-data/pl1.xml",
#  "/Users/arnavmahajan/Desktop/pp-master/playlist/test-data/pl2.xml"])
# find_common_tracks("/Users/arnavmahajan/Desktop/pp-master/playlist/test-data/mymusic.xml")
# print(find_duplicates("/Users/arnavmahajan/Desktop/pp-master/playlist/test-data/pp1.xml"))
# print(find_duplicates("/Users/arnavmahajan/Desktop/Python/Python Playground/iTunes Music Library.xml"))