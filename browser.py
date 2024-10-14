import wx
import wx.html2
import urllib.request

class Browser(wx.Frame):
    def __init__(self, *args, **kwargs):
        wx.Frame.__init__(self, *args, **kwargs)

        self.panel = wx.Panel(self)
        
        # Create controls
        self.back_button = wx.Button(self.panel, label="Back")
        self.forward_button = wx.Button(self.panel, label="Forward")
        self.refresh_button = wx.Button(self.panel, label="Refresh")
        self.address_bar = wx.TextCtrl(self.panel, style=wx.TE_PROCESS_ENTER)
        self.go_button = wx.Button(self.panel, label="Go")
        
        self.web_view = wx.html2.WebView.New(self.panel)

        # Set up the layout
        nav_sizer = wx.BoxSizer(wx.HORIZONTAL)
        nav_sizer.Add(self.back_button, 0, wx.ALL, 5)
        nav_sizer.Add(self.forward_button, 0, wx.ALL, 5)
        nav_sizer.Add(self.refresh_button, 0, wx.ALL, 5)
        nav_sizer.Add(self.address_bar, 1, wx.EXPAND|wx.ALL, 5)
        nav_sizer.Add(self.go_button, 0, wx.ALL, 5)

        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(nav_sizer, 0, wx.EXPAND)
        main_sizer.Add(self.web_view, 1, wx.EXPAND)

        self.panel.SetSizer(main_sizer)

        # Bind events
        self.Bind(wx.EVT_BUTTON, self.on_back, self.back_button)
        self.Bind(wx.EVT_BUTTON, self.on_forward, self.forward_button)
        self.Bind(wx.EVT_BUTTON, self.on_refresh, self.refresh_button)
        self.Bind(wx.EVT_BUTTON, self.on_go, self.go_button)
        self.Bind(wx.EVT_TEXT_ENTER, self.on_go, self.address_bar)
        self.web_view.Bind(wx.html2.EVT_WEBVIEW_NAVIGATING, self.on_navigating)

        # Load initial page
        self.load_url("https://www.example.com")

    def on_back(self, event):
        if self.web_view.CanGoBack():
            self.web_view.GoBack()

    def on_forward(self, event):
        if self.web_view.CanGoForward():
            self.web_view.GoForward()

    def on_refresh(self, event):
        self.web_view.Reload()

    def on_go(self, event):
        url = self.address_bar.GetValue()
        self.load_url(url)

    def on_navigating(self, event):
        url = event.GetURL()
        print(f"Navigating to: {url}")
        try:
            with urllib.request.urlopen(url) as response:
                html = response.read().decode('utf-8')
                print("HTML content:")
                print(html)
                print("\n" + "="*50 + "\n")
        except Exception as e:
            print(f"Error fetching HTML: {e}")

    def load_url(self, url):
        self.web_view.LoadURL(url)
        self.address_bar.SetValue(url)

def main():
    app = wx.App()
    frame = Browser(None, title="Simple Web Browser")
    frame.Show()
    app.MainLoop()

if __name__ == '__main__':
    main()
