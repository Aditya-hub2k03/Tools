<p>To package it to a windows .exe file</p>
<ul>Steps to be followed are
<li>Install the pip package "pyinstaller"</li>
<li>Add this at the top of the app.py <br>
  import os<br>
  os.environ["QTWEBENGINE_DISABLE_SANDBOX"] = "1"</li>
<li>Run this in terminal from the project directory<br>
pyinstaller --noconfirm --onedir --windowed ^<br>
--hidden-import PyQt5.QtWebEngineWidgets ^<br>
--collect-all PyQt5 ^<br>
app.py<br>
</li>
<li>The application will be in the folder ./dist/app</li>

</ul>
