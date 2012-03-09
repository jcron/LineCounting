import unittest
import os
from LineCounting import LineCounting

WRITE = "w"

class TestLineCounting(unittest.TestCase):

    def setUp(self):
        self.file = "TestFile.cpp"
        self.files = []
        self.f = None

    def tearDown(self):
        for file in self.files:
            os.remove(file)

#Tests
    def testEmptyFile(self):
        self.setUpFile()
        self.writeEmptyFile(self.file)

        self.counter.countLines()

        assert 0 == self.counter.totalLinesOfCode()
        assert 0 == self.counter.totalCommentLines()

    def testFileWithOneLine(self):
        self.setUpFile()
        self.f.write("#include \"stdafx.h\"")
        self.f.close()

        self.counter.countLines()

        assert 1 == self.counter.totalLinesOfCode()
        assert 0 == self.counter.totalCommentLines()

    def testFileWithOneCommentLine(self):
        self.setUpFile()
        self.f.write("//#include \"stdafx.h\"")
        self.f.close()

        self.counter.countLines()

        assert 0 == self.counter.totalLinesOfCode()
        assert 1 == self.counter.totalCommentLines()

    def testFileWithTwoValidLines(self):
        self.setUpFile()
        self.f.write("#include \"stdafx.h\"\n")
        self.f.write("#include \"stdafx.h\"")
        self.f.close()

        self.counter.countLines()

        assert 2 == self.counter.totalLinesOfCode()
        assert 0 == self.counter.totalCommentLines()

    def testFileWithBraces(self):
        self.setUpFile()
        self.f.write("#include \"stdafx.h\"\n")
        self.f.write("{\n")
        self.f.write("}")
        self.f.close()

        self.counter.countLines()

        assert 1 == self.counter.totalLinesOfCode()
        assert 0 == self.counter.totalCommentLines()

    def testFileWithIndentedBraces(self):
        self.setUpFile()
        self.f.write("#include \"stdafx.h\"\n")
        self.f.write("   {\n")
        self.f.write("   }")
        self.f.close()

        self.counter.countLines()

        assert 1 == self.counter.totalLinesOfCode()
        assert 0 == self.counter.totalCommentLines()

    def testFileWithCodeAfterBraceOnSameLine(self):
        self.setUpFile()
        self.f.write("{ int x = 10;  }");
        self.f.close()

        self.counter.countLines()

        assert 1 == self.counter.totalLinesOfCode()
        assert 0 == self.counter.totalCommentLines()

    def testFileWithCommentAfterBraceOnSameLine(self):
        self.setUpFile()
        self.f.write("} // comment");
        self.f.close()

        self.counter.countLines()

        assert 0 == self.counter.totalLinesOfCode()
        assert 1 == self.counter.totalCommentLines()

    def testFileWithMultiLineComments(self):
        self.setUpFile()
        self.f.write("#include \"stdafx.h\"\n")
        self.f.write("   int main()\n")
        self.f.write("   {\n")
        self.f.write("      private variable;\n")
        self.f.write("      /*private variable1;\n")
        self.f.write("      private variable2;*/\n")
        self.f.write("   }")
        self.f.close()

        self.counter.countLines()

        assert 3 == self.counter.totalLinesOfCode()
        assert 2 == self.counter.totalCommentLines()

    def testFileWithCloseOfClassDeclaration(self):
        self.setUpFile()
        self.f.write("class Class\n");
        self.f.write("{\n");
        self.f.write("   // My class\n");
        self.f.write("};");
        self.f.close()

        self.counter.countLines()

        assert 1 == self.counter.totalLinesOfCode()
        assert 1 == self.counter.totalCommentLines()
        assert 1 == self.counter.totalFiles()

    def testCountingSameFileTwiceProducesRightNumberOfLines(self):
        self.setUpFile()
        self.f.write("// PCR# 1047\n");
        self.f.write("{\n");
        self.f.write("   // Redundancy\n");
        self.f.write("   int x = 0;\n");
        self.f.write("   int x = 0;\n");
        self.f.write("};");
        self.f.close()

        self.counter.countLines()
        self.counter.countLines()

        assert 2 == self.counter.totalLinesOfCode()
        assert 2 == self.counter.totalCommentLines()

    def testDirectoryWithEmptyFile(self):
        self.setUpDir()

        self.writeEmptyFile(self.fileAndDir)
        
        self.counter.countLines()

        assert 0 == self.counter.totalLinesOfCode()
        assert 0 == self.counter.totalCommentLines()
        assert 1 == self.counter.totalFiles()

    def testDirectoryWithOneFileAndOneComment(self):
        self.setUpDir()

        self.f = open(self.fileAndDir, WRITE)
        self.f.write("// This is a comment")
        self.f.close()

        self.counter.countLines()

        assert 0 == self.counter.totalLinesOfCode()
        assert 1 == self.counter.totalCommentLines()
        assert 1 == self.counter.totalFiles()
        
    def testDirectoryWithFilter(self):
        self.setUpDir()

        self.f = open(self.fileAndDir, WRITE)
        self.f.write("// This is a comment")
        self.f.close()
        
        self.writeEmptyFile("%s/TestFile.txt" % (self.dir))
        self.files.append("%s/TestFile.txt" % (self.dir))

        self.counter.countLines()

        assert 0 == self.counter.totalLinesOfCode()
        assert 1 == self.counter.totalCommentLines()
        assert 1 == self.counter.totalFiles() 
        
    def testDirectoryWithMultipleFilters(self):
        self.setUpDir()

        self.f = open(self.fileAndDir, WRITE)
        self.f.write("// This is a comment")
        self.f.close()
        
        self.f = open("%s/%s" % (self.dir, "TestFile.h"), WRITE)
        self.f.write("int x = 0;")
        self.f.close()
        self.files.append("%s/TestFile.h" % (self.dir))
        
        self.writeEmptyFile("%s/TestFile.txt" % (self.dir))
        self.files.append("%s/TestFile.txt" % (self.dir))

        self.counter.countLines()

        assert 1 == self.counter.totalLinesOfCode()
        assert 1 == self.counter.totalCommentLines()
        assert 2 == self.counter.totalFiles() 

#private methods
    def writeEmptyFile(self, file):
        if self.f is not None:
            self.f.close()
        self.f = open(file, WRITE)
        self.f.write("")
        self.f.close()

    def setUpFile(self):
        self.files.append(self.file)

        self.counter = LineCounting(self.file)
        self.f = open(self.file, WRITE)

    def setUpDir(self):
        self.file = "Testing.cpp"
        self.dir = "TestDirectory"
        self.fileAndDir = "%s/%s" % (self.dir, self.file)
        self.files.append(self.fileAndDir)

        self.counter = LineCounting(self.dir, [".cpp",".h"])

        
#Main entry for application
if __name__ == "__main__":
    unittest.main()