# Stroke
Captures a list of points which typically represents a mouse path which is decoded as a stroke or gesture.

I was working at a company in early 2000, using Mentor Graphics CAD tools which implement middle button mouse gestures as shortcuts to commands. While dabbling in Objective-C, I tried implementing the equivalent functionality in an example sketch program provided by Apple. It worked but the code / algorithm sat unused for many many years. Recently I've been writing some tools in Python and I wanted to share the algorithm since I think it was clever. I translated it to Python and used wxPython libraries to create a graphical demo.

stroke_demo.py will let you practice using strokes / gestures using the left mouse button and drawing in the window. wxPython does not currently work with Python 3.10 so you should use 3.9 for now to run the demo.

stroke.py implements an algorithm which translates the path (points) on a virtual grid into a unique identifier. This can be translated to other languages. I purposely changed it some so that it could be implemented in C with only integers and not use any division provided you remove the debug grid code. You could return an integer instead of a string by using a quadrant number. stroke = stroke * 10 + quadrant. You might want to use 64 bit integers and stop if it overflows. 32 bits will store most gestures.

stroke_decode.py contains a function which will turn the number sequence into some descriptive text. This was added because the numbers are not so descriptive. You can use the 

Below are a couple of screenshots from the demo. The path is displayed as a thick black line. White dots show the points captured by the mouse move event handler and a red grid is overlaid to show the extents of the path to understand the decoded value.

![Screen Shot 2022-01-25 at 2 16 04 AM](https://user-images.githubusercontent.com/28468090/150929129-917a4c99-0d43-4eaa-8ae4-064a6dd67caf.png)
![Screen Shot 2022-01-25 at 2 17 27 AM](https://user-images.githubusercontent.com/28468090/150929351-cb665db1-bb82-480e-b16c-2560703f6c55.png)
![Screen Shot 2022-01-25 at 2 21 23 AM](https://user-images.githubusercontent.com/28468090/150929811-340861aa-9ef5-4151-b1c8-bf495bb3a1c9.png)

I'll be back here to improve the readme and wiki since this is my first github repository.
