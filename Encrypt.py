import wx
import os
import commands
import ctypes
import hashlib

# Global Variable
MyMD5 = "./MyMD5 "

class EncryptFrame(wx.Frame):
    
    def __init__(self, superion):
        wx.Frame.__init__(self, parent = superion, title = "Encrypt", size = (1000, 200))
        panel = wx.Panel(self)
        
        # String Input TextCtrl
        wx.StaticText(parent = panel, label = 'Input a string:', pos = (10, 10))
        self.inputStr = wx.TextCtrl(parent = panel, pos = (120, 10), size = (300, 20))
        
        # MD5 Output TextCtrl
        wx.StaticText(parent = panel, label = 'MD5:', pos = (10, 50))
        self.outputMD5 = wx.TextCtrl(parent = panel, pos = (120, 50), size = (300, 20))
        # MD5 Generate Button
        self.buttonMD5Gen = wx.Button(parent = panel , label = 'MD5 Generate', pos = (450, 46))
        self.Bind(wx.EVT_BUTTON, self.OnButtonMD5Gen, self.buttonMD5Gen)
        
        # SHA-512 Output TextCtrl
        wx.StaticText(parent = panel, label = 'SHA-512:', pos = (10, 90))
        self.outputSHA512 = wx.TextCtrl(parent = panel, pos = (120, 90), size = (300, 20))
        # SHA-512 Generate Button
        self.buttonSHA512Gen = wx.Button(parent = panel, label = 'SHA-512 Generate', pos = (450, 86))
        self.Bind(wx.EVT_BUTTON, self.OnButtonSHA512Gen, self.buttonSHA512Gen)
        
        # Functional Button
        self.buttonClear = wx.Button(parent = panel, label = 'Clear', pos = (70, 130))
        self.Bind(wx.EVT_BUTTON, self.OnButtonClear, self.buttonClear)
        self.buttonQuit = wx.Button(parent = panel, label = 'Quit', pos = (150, 130))
        self.Bind(wx.EVT_BUTTON, self.OnButtonQuit, self.buttonQuit)
        
    #The old version of MD5 Generation
    '''    
    def OnButtonMD5Gen(self, event):
        self.outputMD5.Clear()
        try:
            LoadStr = str(self.inputStr.GetValue())
        except BaseException, e:
            wx.MessageBox('Please input a string!')
            return
        MyMD5Command = MyMD5 + LoadStr
        ResultStr = commands.getoutput(MyMD5Command)
        self.outputMD5.SetLabel(ResultStr)
    '''
    
    def OnButtonMD5Gen(self, event):
        self.outputMD5.Clear()
        try:
            LoadStr = str(self.inputStr.GetValue())
        except BaseException, e:
            wx.MessageBox('Please input a string!')
            return
        so = ctypes.cdll.LoadLibrary
        lib = so("./MyMD5.so")
        MyMD5 = lib.MD5
        MyMD5.restype = ctypes.c_char_p
        ResultStr = MyMD5(LoadStr)
        self.outputMD5.SetLabel(ResultStr)
        
    def OnButtonSHA512Gen(self, event):
        self.outputSHA512.Clear()
        try:
            LoadStr = str(self.inputStr.GetValue())
        except BaseException, e:
            wx.MessageBox('Please input a string!')
            return
        h = hashlib.new('sha512', LoadStr)
        self.outputSHA512.SetLabel(h.hexdigest())
                    
    def OnButtonClear(self, event):
        self.inputStr.Clear()
        self.outputMD5.Clear()
        self.outputSHA512.Clear()
        
    def OnButtonQuit(self, event):
        dlg = wx.MessageDialog(self, 'Really Quit?', 'Caution', wx.CANCEL|wx.OK|wx.ICON_QUESTION)
        if dlg.ShowModal() == wx.ID_OK:
            self.Destroy()
            
if __name__ == '__main__':
    app = wx.App()
    frame = EncryptFrame(None)
    frame.Show()
    app.MainLoop()
    
                