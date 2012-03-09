import sys
import os

READ_ONLY = "r"
OPEN_BRACE = "{"
CLOSE_BRACE = "}"
CLASS_DECLARATION_END = "};"
MULTILINE_COMMENT_OPEN = "/*"
MULTILINE_COMMENT_CLOSE = "*/"
SINGLELINE_COMMENT = "//"
DEFAULT_FILTER = "*"

class LineCounting:

    def __init__(self, input, filters=[DEFAULT_FILTER]):
        self.__input = input
        self.__filters = filters

        self.__fileCount = 0
        self.__codeLines = 0
        self.__commentLines = 0

    def totalLinesOfCode(self):
        return self.__codeLines

    def totalCommentLines(self):
        return self.__commentLines

    def totalFiles(self):
        return self.__fileCount

    def countLines(self):
        self.__codeLines = 0
        self.__commentLines = 0

        if self.__inputIsDir():
            self.__processDirectory(self.__input)
        elif self.__inputIsFile():
            self.__processFile(self.__input)

#private methods

    def __inputIsFile(self):
        return os.path.isfile(self.__input)

    def __inputIsDir(self):
        return os.path.isdir(self.__input)

    def __processDirectory(self, directoryToProcess):
        for directory, dirnames, filenames in os.walk(directoryToProcess):
            for name in filenames:
                if filter != DEFAULT_FILTER and self.__filePassesFilter(name):
                    self.__processFile("%s/%s" % (directory, name))
                    
    def __processFile(self, fileToProcess):
        self.__countLinesInFile(fileToProcess)
        self.__fileCount += 1

    def __filePassesFilter(self, fileName):
        for filter in self.__filters:
            if fileName.endswith(filter):
                return True
        return False

    def __countLinesInFile(self, fileToCount):
        file = "%s/%s" % (os.curdir, fileToCount)
        f = open(file, READ_ONLY)
        line = f.readline()

        while self.__lineIsNotEmpty(line):
            if self.__isStartOfMultiLineComment(line):
                self.__advanceUntilEndOfComment(line, f)
            elif self.__linesToCount(line):
                self.__codeLines += 1
            line = f.readline()
        f.close()

    def __lineIsNotEmpty(self, line):
        return line != ""

    def __isStartOfMultiLineComment(self, line):
        return line.find(MULTILINE_COMMENT_OPEN) >= 0

    def __advanceUntilEndOfComment(self, line, f):
        self.__commentLines += 1
        while line.find(MULTILINE_COMMENT_CLOSE) == -1:
            self.__commentLines += 1
            line = f.readline()

    def __linesToCount(self, line):
        line = self.__removeSingleLineCommentsFromLine(line)
        line = line.strip()
        return self.__shouldCountAsLineOfCode(line)
        
    def __shouldCountAsLineOfCode(self, line):
        return self.__lineIsNotEmpty(line) and line != OPEN_BRACE and line != CLOSE_BRACE and not line == CLASS_DECLARATION_END

    def __removeSingleLineCommentsFromLine(self, line):
        index = line.find(SINGLELINE_COMMENT)
        if index > -1:
            line = line[0:index]
            self.__commentLines += 1
        return line

def main():
    counter = LineCounting(sys.argv[1])
    counter.countLines()
    
    print("   Files: %d"  % (counter.totalFiles()))
    print("     LOC: %d"  % (counter.totalLinesOfCode()))
    print("Comments: %d" % (counter.totalCommentLines()))

if __name__ == "__main__":
    main()
