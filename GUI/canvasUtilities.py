#! /usr/bin/env python
#
"""Utilities for matplotlib graphics

We will have two subpanels: an options panel at the
top and a graphics canvas below it.
"""
import copy

import wx

import numpy
#
#  Matplotlib stuff
#
import matplotlib

from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wxagg import NavigationToolbar2WxAgg
from matplotlib.figure                 import Figure
from matplotlib                        import pyplot
from matplotlib                        import cm

from guiConfig    import WindowParameters as WP
from guiUtilities import makeTitleBar

__all__ = ['matplotlib',
           'FigureCanvas',
           'NavigationToolbar2WxAgg',
           'Figure',
           'pyplot',
           'cmapPanel']
#
# ---------------------------------------------------CLASS:  cmapPanel
#
class cmapPanel(wx.Panel):
    """cmapPanel """
    def __init__(self, parent, id, **kwargs):
	"""Constructor for cmapPanel."""
	#
	wx.Panel.__init__(self, parent, id, **kwargs)
        #
	#  Window Objects.
	#
        self.__makeObjects()
	#
	#  Bindings.
	#
	self.__makeBindings()
	#
	#  Sizing.
	#
	self.__makeSizers()
	#
        #  Data
        #
        self.cmap = copy.deepcopy(getattr(cm, self.cmap_name))
	#
	self.SetAutoLayout(True)
        self.SetSizerAndFit(self.sizer)
	#
	return
    #
    # ============================== Internal Methods
    #
    def __makeObjects(self):
        """Add interactors"""

        self.tbarSizer = makeTitleBar(self, 'Colormap',
                                      color=WP.BG_COLOR_TITLEBAR_PANEL1)
        #
        #  * choose colormap and vmin and vmax
        #
        self.cmap_lab = wx.StaticText(self, wx.NewId(), 
                                        'Colormap:  ', 
                                        style=wx.ALIGN_RIGHT)
        
        self.cmap_nameList = ['autumn', 'bone', 'bone_r', 'cool', 'copper', 
                              'flag', 'gray', 'gray_r', 'hot', 'hot_r',
                              'hsv', 'jet', 'pink', 'prism', 'spring',
                              'summer', 'winter', 'spectral']
        self.cmap_cho = wx.Choice(self, wx.NewId(), 
                                  choices=self.cmap_nameList)
        
        self.cmap_name = 'bone'
        self.cmap_cho.SetStringSelection(self.cmap_name)
        
        self.cmin_val = 0
        self.cmin_lab = wx.StaticText(self, wx.NewId(), 
                                        'Minimum:  ', 
                                        style=wx.ALIGN_RIGHT)
        self.cmin_txt = wx.TextCtrl(self, wx.NewId(), 
                                       value=str(self.cmin_val), 
                                       style=wx.RAISED_BORDER | wx.TE_PROCESS_ENTER)
        self.cmUnder_box = wx.CheckBox(self, wx.NewId(), 'show under')

        self.cmax_val = 2000
        self.cmax_lab = wx.StaticText(self, wx.NewId(), 
                                        'Maximum:  ', 
                                        style=wx.ALIGN_RIGHT)
        self.cmax_txt = wx.TextCtrl(self, wx.NewId(), 
                                       value=str(self.cmax_val), 
                                       style=wx.RAISED_BORDER | wx.TE_PROCESS_ENTER)
        self.cmOver_box = wx.CheckBox(self, wx.NewId(), 'show over')
        

        return

    def __makeBindings(self):
        """Bind interactors"""
        # colormap stuff
        self.Bind(wx.EVT_CHOICE,     self.OnChooseCmap,    self.cmap_cho)
        self.Bind(wx.EVT_TEXT_ENTER, self.OnSetCmin,       self.cmin_txt)
        self.Bind(wx.EVT_TEXT_ENTER, self.OnSetCmax,       self.cmax_txt)

        self.Bind(wx.EVT_CHECKBOX, self.OnSetUnder,      self.cmUnder_box)
        self.Bind(wx.EVT_CHECKBOX, self.OnSetOver,       self.cmOver_box)

        return

    def __makeSizers(self):
	"""Lay out the interactors"""
        #
        #  colormap sizer
        #
        nrow = 1; ncol = 3; padx = 5; pady = 5
	self.cmSizer = wx.FlexGridSizer(nrow, ncol, padx, pady)
        
        self.cmSizer.Add(self.cmap_lab, 0, wx.EXPAND | wx.ALIGN_RIGHT)
        self.cmSizer.Add(self.cmap_cho, 0, wx.EXPAND | wx.ALIGN_RIGHT)
        self.cmSizer.AddSpacer(1)
        
        self.cmSizer.Add(self.cmin_lab, 0, wx.EXPAND | wx.ALIGN_RIGHT)
        self.cmSizer.Add(self.cmin_txt, 0, wx.EXPAND | wx.ALIGN_RIGHT)
        self.cmSizer.Add(self.cmUnder_box, 0, wx.EXPAND | wx.ALIGN_RIGHT)
        
        self.cmSizer.Add(self.cmax_lab, 0, wx.EXPAND | wx.ALIGN_RIGHT)
        self.cmSizer.Add(self.cmax_txt, 0, wx.EXPAND | wx.ALIGN_RIGHT)
        self.cmSizer.Add(self.cmOver_box, 0, wx.EXPAND | wx.ALIGN_RIGHT)
	
	self.sizer = wx.BoxSizer(wx.VERTICAL)
	self.sizer.Add(self.tbarSizer, 0, wx.EXPAND|wx.ALIGN_CENTER)
        self.sizer.Add(self.cmSizer,   0, wx.EXPAND|wx.ALIGN_RIGHT)

	return
    #
    # ============================== API
    #
    #                     ========== *** Access Methods
    #
    def update(self, **kwargs):
        """Call parent to update"""
        self.GetParent().update(**kwargs)
        
        return
    #
    #                     ========== *** Event Callbacks
    #
    def OnChooseCmap(self, e):
        self.cmap_name = self.cmap_cho.GetStringSelection()
        self.cmap = copy.deepcopy(getattr(cm, self.cmap_name))
        self.update(newImage=True)
        return

    def OnSetCmin(self, e):
        self.cmin_val = float(self.cmin_txt.GetValue())
        self.update(newImage=True)
        return

    def OnSetCmax(self, e):
        self.cmax_val = float(self.cmax_txt.GetValue())
        self.update(newImage=True)
        return

    def OnSetUnder(self, e):
        """show values under threshold"""
        self.cmap = copy.deepcopy(getattr(cm, self.cmap_name))
        if e.IsChecked():
            self.cmap.set_under('b')
            pass
        
        self.update(newImage=True)

        return
    
    def OnSetOver(self, e):
        """show values over threshold"""
        self.cmap = copy.deepcopy(getattr(cm, self.cmap_name))

        if e.IsChecked():
            self.cmap.set_over('r')
            pass
        
        self.update(newImage=True)

        return
    
    pass # end class
#
# -----------------------------------------------END CLASS:  cmapPanel