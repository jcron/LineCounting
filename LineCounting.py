import sys
import os


READ_ONLY = "r"
OPEN_BRACE = "{"
CLOSE_BRACE = "}"
CLASS_DECLARATION_END = "};"
MULTILINE_COMMENT_OPEN = "/*"
MULTILINE_COMMENT_CLOSE = "*/"
SINGLELINE_COMMENT = "//"

class LineCounting:
        
    def __init__(self, file):
        self.__file = file
        self.__fileCount = 0
        self.__codeLines = 0
        self.__commentLines = 0
        
    def inputIsFile(self):
        return os.path.isfile(self.__file)
        
    def inputIsDir(self):
        return os.path.isdir(self.__file)
        
    def totalLinesOfCode(self):
        return self.__codeLines
        
    def totalCommentLines(self):
        return self.__commentLines
        
    def totalFiles(self):
        return self.__fileCount
        
    def countLines(self):
        self.__codeLines = 0
        self.__commentLines = 0
        
        if self.inputIsDir():
            for directory, dirnames, filenames in os.walk(self.__file):
                for name in filenames:
                    self.__countLinesInFile(name)
                    self.__fileCount += 1
        elif self.inputIsFile():
            self.__countLinesInFile(self.__file)
            self.__fileCount += 1
            
#private methods
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
        