# neopolitan
A library for displaying "text" on LED boards

## Description

This is a revamp of [stockticker](https://github.com/alyoshenka/stockticker), which queries real-time stock price data, calculates daily fluctuations, and displays it on an LED board. While the end result of that project was cool, this project aims to clarify much of the data display code and make it usable to display any inputted message. See this [sub-readme](https://github.com/alyoshenka/neopolitan/tree/main/src/writing#readme) for an introduction to how data can be used to make the board display "human-readable" text.

Given that access to hardware boards can be constrictive and testing can be difficult, this project aims to support data display on a graphical interface so that anyone can access it. `pygame` is used to display the graphical display, while the `neopixel` (hence the project name) library is used to interface with the hardware board. The switch between these two displays is OS-dependent.

## Installation
`[python3 -m] pip install neopolitan`

## Usage
*Make sure to exit the program by pressing the window close "X", instead of `ctrl+c`*
- To run the program
  ```py
  from neopolitan.neop import main as main_function
  main_function()
  ```
- To demo live-update functionality
  ```py
  import neopolitan.testboardrunner
  ```
- To run the program with arguments
  ```py
  from queue import Queue

  q = Queue() # Initialize the input events queue
  q.put('say This is a demo statement') # Set the message: 'say {message (spaces okay)}'
  q.put('speed fast') # Set the scroll speed: 'speed {slow/medium/fast}'
  q.put('wrap True') # Set whether message wraps when done displaying: 'wrap {True/False};

  from neopolitan.neop import main
  main(events=q) # Run main with the specified events
  ```
  - See [Supported Characters](https://github.com/alyoshenka/neopolitan/blob/main/neopolitan/writing/ReadMe.md#defined-characters) for a list of supported characters

https://github.com/alyoshenka/neopolitan/assets/38815390/1e98261b-8dfb-48e3-943b-34b49878c55f

- To run some demos
  ```py
  from neopolitan.demos import *

  display('This displays a message that cannot be updated')
  # Execution will return here when the display is closed
  display_all() # display all defined symbols
  ```

https://github.com/alyoshenka/neopolitan/assets/38815390/e9cae65b-2c18-4844-886f-61a2a319c42a


- See [this code](https://github.com/alyoshenka/neo/blob/main/neo/neopolitan_handler.py) for an example of how to send live updates in the package

## Command Line Arguments

[*Deprecated*]
**Note: This code only works from source, NOT the package install**

From the top-level `neopolitan/` directory: `python[3] neopolitan/neop.py {args}`
- `--message/-m {message_to_display}`
  - Displays the given message on the board (enclose in quotes if multiple words)
- `--scroll-speed/-s {slow/medium/fast}`
  - Controls how quickly the display scrolls across the screen
- `--wrap/-w {True/False}`
  - Determines whether the display should "wrap around" when it gets to the end, or just show a blank screen
