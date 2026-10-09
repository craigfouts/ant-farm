'''
Author(s): Craig fouts
Correspondence: c.fouts25@imperial.ac.uk
License: Apache 2.0 license
'''

from IPython.display import HTML, display

def set_background(color='transparent'):
    display(HTML('''
        <style>
            .cell-output-ipywidget-background {
                background-color: %s !important;
            }
        </style>
    ''' % color))
