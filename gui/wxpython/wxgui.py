"""
@package wxgui

@brief Main Python application for GRASS wxPython GUI

Classes:
 - wxgui::GMApp
 - wxgui::GSplashScreen

(C) 2006-2015 by the GRASS Development Team

This program is free software under the GNU General Public License
(>=v2). Read the file COPYING that comes with GRASS for details.

@author Michael Barton (Arizona State University)
@author Jachym Cepicky (Mendel University of Agriculture)
@author Martin Landa <landa.martin gmail.com>
@author Vaclav Petras <wenzeslaus gmail.com> (menu customization)
"""

import os
import sys
import getopt

from core import globalvar
from core.utils import _

from grass.exceptions import Usage
from grass.script.core import set_raise_on_error

import wx
try:
    import wx.lib.agw.advancedsplash as SC
except ImportError:
    SC = None

from lmgr.frame import GMFrame


class GMApp(wx.App):
    def __init__(self, workspace = None):
        """ Main GUI class.

        :param workspace: path to the workspace file
        """
        self.workspaceFile = workspace

        # call parent class initializer
        wx.App.__init__(self, False)

        self.locale = wx.Locale(language = wx.LANGUAGE_DEFAULT)

    def OnInit(self):
        """ Initialize all available image handlers

        :return: True
        """
        if not globalvar.CheckWxVersion([2, 9]):
            wx.InitAllImageHandlers()

        splash = GSplashScreen(app=self, workspace=self.workspaceFile)
        splash.Show()
        
        return True

class GSplashScreen(wx.SplashScreen):
    """Create a splash screen widget
    """
    def __init__(self, parent=None, app=None, workspace=None):
        self.workspaceFile = workspace
        self.parent = parent
        self.app = app
        
        bitmap = wx.Image(name=os.path.join(globalvar.IMGDIR, "splash_screen.png")).ConvertToBitmap()
        wx.SplashScreen.__init__(self, bitmap,
                                 wx.SPLASH_CENTRE_ON_SCREEN | wx.SPLASH_TIMEOUT,
                                 2000, parent)
        self.Bind(wx.EVT_CLOSE, self.OnExit)

        wx.Yield()

    def OnExit(self, event):
        self.Hide()
        
        # create and show main frame
        frame = GMFrame(parent = None, id = wx.ID_ANY,
                        workspace = self.workspaceFile)
        self.app.SetTopWindow(frame)
        frame.Show()
        
        event.Skip()  # make sure the default handler runs too

def printHelp():
    """ Print program help"""
    print >> sys.stderr, "Usage:"
    print >> sys.stderr, " python wxgui.py [options]"
    print >> sys.stderr, "%sOptions:" % os.linesep
    print >> sys.stderr, " -w\t--workspace file\tWorkspace file to load"
    sys.exit(1)


def process_opt(opts, args):
    """ Process command-line arguments"""
    workspaceFile = None
    for o, a in opts:
        if o in ("-h", "--help"):
            printHelp()

        if o in ("-w", "--workspace"):
            if a != '':
                workspaceFile = str(a)
            else:
                workspaceFile = args.pop(0)

    return (workspaceFile,)


def main(argv = None):
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "hw:",
                                       ["help", "workspace"])
        except getopt.error as msg:
            raise Usage(msg)

    except Usage as err:
        print >> sys.stderr, err.msg
        print >> sys.stderr, "for help use --help"
        printHelp()

    workspaceFile = process_opt(opts, args)[0]

    app = GMApp(workspaceFile)
    # suppress wxPython logs
    q = wx.LogNull()
    set_raise_on_error(True)

    app.MainLoop()

if __name__ == "__main__":
    sys.exit(main())
