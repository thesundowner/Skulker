# Skulker Readme



Skulker is a application that let's you hide information in jpeg photos with encryption. the photos will be untouched. The only difference is in the file size (obviously). 

The algorithm behind this is.. appending the data directly. 
In more technical terms, every jpeg file has the hex `0xffd9` at the end and `0xffd8` at the beginning. A program that opens a jpeg photo only care about what's inside those 2 offsets. It doesn't care what's written outside those 2 markers. Skulker exploits this and writes the data after `0xffd9`. A typical photo viewer doesn't care about what's outside the file - So theoretically, It's hidden. Along with AES encryption, Your tax records are safe from the IRC. 
