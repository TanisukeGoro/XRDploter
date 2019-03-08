""" This is the module that change terminal output font color."""
class PlotColor:
    color_index = [
        #check the color push coomand + shift + C
        # 'rgb(212, 212, 212)', # grey
        'rgb(37, 154, 255)', # blue
        'rgb(255, 96, 96)', # red
        'rgb(69, 198, 188)', # blue green
        'rgb(215, 214, 76)', # yellowgreen
        'rgb(27, 157, 26)', # green
        'rgb(250, 10, 16)', # red
        'rgb(212, 23, 255)', # parple
        'rgb(25, 73, 82)', # darkseagreen
        'rgb(194, 126, 185)',
        'rgb()',
        'rgb()',
        'rgb()',
        'rgb()',
        'rgb()',
    ]

class TerminalFontColor:
    BLACK     = '\033[30m'
    RED       = '\033[31m'
    GREEN     = '\033[32m'
    YELLOW    = '\033[33m'
    BLUE      = '\033[34m'
    PURPLE    = '\033[35m'
    CYAN      = '\033[36m'
    WHITE     = '\033[37m'
    END       = '\033[0m'
    BOLD      = '\038[1m'
    UNDERLINE = '\033[4m'
    INVISIBLE = '\033[08m'
    REVERCE   = '\033[07m'
