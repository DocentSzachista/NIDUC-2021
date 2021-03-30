from Terminals import Terminal

terminal1 = Terminal("Terminal1")
terminal2 = Terminal("Terminal2")

terminal1.bind(terminal2)
terminal2.bind(terminal1)

terminal1.send_message("Hi form terminal 1")
terminal2.send_message("Hi from terminal 2")