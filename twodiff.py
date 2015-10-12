#!/usr/bin/env python
# encoding: utf-8
import sys
import os
import fcntl, termios, struct
import re
import textwrap

GREEN = "\033[1;32m"
RED = "\033[1;31m"
CLEAR = "\033[0m"

def terminal_size():
    h, w, hp, wp = struct.unpack('HHHH',
        fcntl.ioctl(2, termios.TIOCGWINSZ,
        struct.pack('HHHH', 0, 0, 0, 0)))
    return w, h
cols, rows = terminal_size()

def doOutput(top, subtractedLines, addedLines):
    print ""
    for line in top:
        print line.rjust(cols / 2 + len(line) / 2, " ")
    for i in range(max(len(subtractedLines), len(addedLines))):
        subLine = ""
        addLine = ""
        if i < len(subtractedLines):
            subLine = subtractedLines[i]
        if i < len(addedLines):
            addLine = addedLines[i]

        addColor = GREEN if re.match("^\+", addLine) else CLEAR
        subColor = RED if re.match("^-", subLine) else CLEAR
        subLines = textwrap.wrap(subLine, cols / 2 )
        addLines = textwrap.wrap(addLine, cols / 2)
        for i in range(max(len(subLines), len(addLines))):
            sub = subLines[i] if i < len(subLines) else ""
            add = addLines[i] if i < len(addLines) else ""
            print subColor + sub.ljust(cols / 2, " ") + CLEAR + '│' + addColor + add + CLEAR 

addedLines = {}
addedLineNo = 0
subtractedLines = {}
subtractedLineNo = 0
top = []
lineNo = 0
for line in sys.stdin:
  line = line.replace("\n", "")
  if re.match("[^+-@\s]", line):
      continue
  if re.match("^---", line):
      doOutput(top, subtractedLines, addedLines)
      top = []
      top += [line]
      addedLines = {}
      addedLineNo = 0
      subtractedLines = {}
      subtractedLineNo = 0
      lineNo = 0
  elif re.match("\+\+\+", line):
      top += [line]
  elif re.match("@@", line):
      doOutput(top, subtractedLines, addedLines)
      top = []
      top += [line]
      addedLines = {}
      addedLineNo = 0
      subtractedLines = {}
      subtractedLineNo = 0
      lineNo = 0
  else:
      if not top:
          continue
      elif re.match("^\+", line):
          addedLines[addedLineNo] = line
          addedLineNo += 1
      elif re.match("^-", line):
          subtractedLines[subtractedLineNo] = line
          subtractedLineNo += 1
      else:
          lineNo = max(addedLineNo, subtractedLineNo)
          for i in range(subtractedLineNo, lineNo):
              subtractedLines[i] = ""
          for i in range(addedLineNo, lineNo):
              addedLines[i] = ""
          addedLines[lineNo] = line
          subtractedLines[lineNo] = line
          addedLineNo = lineNo + 1
          subtractedLineNo = lineNo + 1
doOutput(top, subtractedLines, addedLines)