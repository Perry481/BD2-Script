# Auto-Clicker and Template Matching Script

這是一個用於自動點擊並匹配螢幕截圖中模板的腳本。該腳本會不斷捕捉螢幕截圖，尋找指定的按鈕並點擊它們，然後檢查截圖中是否存在指定的模板。

## 功能

- 自動點擊指定按鈕（retry、retry confirm、skip）。
- 檢查螢幕截圖中是否存在指定模板。
- 檢查模板中是否存在Ultra rare模板。
- 持續運行直到找到所需模板或按下F9鍵退出。

## 先決條件

在運行此腳本之前，請確保您的系統中安裝了以下Python庫：

- `opencv-python`
- `numpy`
- `pyautogui`
- `keyboard`
- `pillow`

您可以使用以下命令來安裝這些庫：

```sh
pip install opencv-python numpy pyautogui keyboard pillow

