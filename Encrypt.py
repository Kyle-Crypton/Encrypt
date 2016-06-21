import wx
import os
import base64
import commands
import ctypes
import hashlib

from Crypto.Cipher import AES
from binascii import b2a_base64, a2b_base64

# Global Variable
MyMD5 = "./MyMD5 "
# -----------------
# AES Variable
# The block size for the cipher object; must be 16, 24, or 32 for AES
BLOCK_SIZE = 16

# The character used for padding--with a block cipher such as AES, the value
# you encrypt must be a multiple of BLOCK_SIZE in length. This character is
# used to ensure that your value is always a multiple of BLOCK_SIZE
PADDING = '{'

# One-linear to sufficiently pad the text to be encrypted
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING

# One-liners to encrypt/encode and decrypt/decode a string/message
# Encrypt with AES, encode with base64
EncodeAES = lambda c, s: base64.b64encode(c.encrypt(pad(s)))
DecodeAES = lambda c, e: c.decrypt(base64.b64decode(e)).rstrip(PADDING)

# Generate a random secret key and iv
AESKEY = os.urandom(BLOCK_SIZE)
AESIV = os.urandom(BLOCK_SIZE)

# Create cipher and dcipher using the random secret
AESCipher = AES.new(AESKEY, AES.MODE_CBC, AESIV)
AESDcipher = AES.new(AESKEY, AES.MODE_CBC, AESIV)

class EncryptFrame(wx.Frame):
    
    def __init__(self, superion):
        wx.Frame.__init__(self, parent = superion, title = "Encrypt", size = (1000, 500))
        panel = wx.Panel(self)
        
        # String Input TextCtrl
        wx.StaticText(parent = panel, label = 'Input message:', pos = (10, 10))
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
        
        # AES Input TextCtrl
        wx.StaticText(parent = panel, label = 'AES:', pos = (10, 130))
        wx.StaticText(parent = panel, label = 'Key:', pos = (120, 130))
        self.aesKEY = wx.TextCtrl(parent = panel, pos = (180, 130), size = (200, 20))
        wx.StaticText(parent = panel, label = 'IV:', pos = (440, 130))
        self.aesIV = wx.TextCtrl(parent = panel, pos = (500, 130), size = (200, 20))
        # AES Generate Button
        self.buttonAESGen = wx.Button(parent = panel, label = 'AES Generate', pos = (730, 126))
        self.Bind(wx.EVT_BUTTON, self.OnButtonAESGen, self.buttonAESGen)
        # AES Encrypt TextCtrl
        wx.StaticText(parent = panel, label = 'Encrypt:', pos = (120, 170))
        self.aesEncrypted = wx.TextCtrl(parent = panel, pos = (180, 170), size = (200, 20))
        # AES Encrypt Button
        self.buttonAESEnc = wx.Button(parent = panel, label = 'Encrypt', pos = (410, 166))
        self.Bind(wx.EVT_BUTTON, self.OnButtonAESEnc, self.buttonAESEnc)
        # AES Decrypt TextCtrl
        wx.StaticText(parent = panel, label = 'Decrypt:', pos = (120, 210))
        self.aesDecrypted = wx.TextCtrl(parent = panel, pos = (180, 210), size = (200, 20))
        # AES Decrypt Button
        self.buttonAESDec = wx.Button(parent = panel, label = 'Decrypt', pos = (410, 206))
        self.Bind(wx.EVT_BUTTON, self.OnButtonAESDec, self.buttonAESDec)
        
        # Functional Button
        self.buttonClear = wx.Button(parent = panel, label = 'Clear', pos = (70, 250))
        self.Bind(wx.EVT_BUTTON, self.OnButtonClear, self.buttonClear)
        self.buttonQuit = wx.Button(parent = panel, label = 'Quit', pos = (160, 250))
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
        self.outputMD5.SetValue(ResultStr)
    '''
    
    def OnButtonMD5Gen(self, event):
        self.outputMD5.Clear()
        try:
            LoadStr = str(self.inputStr.GetValue())
        except BaseException, e:
            wx.MessageBox('Please input a string!')
            return
        so = ctypes.cdll.LoadLibrary
        lib = so("./KKMD5.so")
        KKMD5 = lib.MD5
        KKMD5.restype = ctypes.c_char_p
        ResultStr = KKMD5(LoadStr)
        self.outputMD5.SetValue(ResultStr)
        
    def OnButtonSHA512Gen(self, event):
        self.outputSHA512.Clear()
        try:
            LoadStr = str(self.inputStr.GetValue())
        except BaseException, e:
            wx.MessageBox('Please input a string!')
            return
        h = hashlib.new('sha512', LoadStr)
        self.outputSHA512.SetValue(h.hexdigest())
        
    def OnButtonAESGen(self, event):
        global AESKEY
        global AESIV
        global AESCipher
        global AESDcipher
        
        self.aesKEY.Clear()
        self.aesIV.Clear()
        self.aesEncrypted.Clear()
        self.aesDecrypted.Clear()
        try:
            LoadStr = str(self.inputStr.GetValue())     
        except BaseException, e:
            wx.MessageBox('Please input a string!')
            return
        AESKEY = os.urandom(BLOCK_SIZE)
        AESIV = os.urandom(BLOCK_SIZE)
        AESCipher = AES.new(AESKEY, AES.MODE_CBC, AESIV)
        AESDcipher = AES.new(AESKEY, AES.MODE_CBC, AESIV)
        self.aesKEY.SetValue(b2a_base64(AESKEY))
        self.aesIV.SetValue(b2a_base64(AESIV))
        
    def OnButtonAESEnc(self, event):
        try:
            LoadStr = str(self.inputStr.GetValue())     
        except BaseException, e:
            wx.MessageBox('Please input a string!')
            return
        encoded = EncodeAES(AESCipher, LoadStr)
        self.aesEncrypted.SetValue(encoded)
        
    def OnButtonAESDec(self, event):
        try:
            encoded = str(self.aesEncrypted.GetValue())
        except BaseException, e:
            wx.MessageBox('Wrong encrypted string!')
            return
        decoded = DecodeAES(AESDcipher, encoded)
        self.aesDecrypted.SetValue(decoded)
                                
    def OnButtonClear(self, event):
        self.inputStr.Clear()
        self.outputMD5.Clear()
        self.outputSHA512.Clear()
        self.aesKEY.Clear()
        self.aesIV.Clear()
        self.aesEncrypted.Clear()
        self.aesDecrypted.Clear()
        
    def OnButtonQuit(self, event):
        dlg = wx.MessageDialog(self, 'Really Quit?', 'Caution', wx.CANCEL|wx.OK|wx.ICON_QUESTION)
        if dlg.ShowModal() == wx.ID_OK:
            self.Destroy()
            
if __name__ == '__main__':
    app = wx.App()
    frame = EncryptFrame(None)
    frame.Show()
    app.MainLoop()
    
                