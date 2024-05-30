import cv2
import numpy as np
import pyautogui
import time
import keyboard
import threading
from PIL import Image
import sys
import os

# 用來停止腳本的標誌
stop_script = False


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def load_image(image_path):
    absolute_path = resource_path(image_path)
    image = cv2.imread(absolute_path, cv2.IMREAD_COLOR)
    if image is None:
        print(f"錯誤：無法載入圖片 {image_path}")
    else:
        print(f"已載入圖片：{image_path}")
    return image


def template_matching(screenshot, template):
    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    w, h = template_gray.shape[::-1]

    result = cv2.matchTemplate(
        screenshot_gray, template_gray, cv2.TM_CCOEFF_NORMED)
    threshold = 0.8
    loc = np.where(result >= threshold)

    points = []
    for pt in zip(*loc[::-1]):
        points.append((pt[0] + w // 2, pt[1] + h // 2))

    return points


def draw_markers(image, points):
    for point in points:
        cv2.drawMarker(image, point, (0, 0, 255),
                       markerType=cv2.MARKER_CROSS, markerSize=20, thickness=2)
    return image


def capture_screenshot():
    screenshot = pyautogui.screenshot()
    screenshot = np.array(screenshot)
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)
    return screenshot


def template_within_template(screenshot, template1, template2, ultra_rare):
    points1 = template_matching(screenshot, template1)
    points2 = template_matching(screenshot, template2)

    template1_found = False
    template2_found = False

    if points1:
        print("找到專武1")
        for point in points1:
            region = screenshot[point[1]-template1.shape[0]//2:point[1]+template1.shape[0]//2,
                                point[0]-template1.shape[1]//2:point[0]+template1.shape[1]//2]
            ultra_rare_points = template_matching(region, ultra_rare)
            if ultra_rare_points:
                print("在專武1中找到Ultra rare")
                template1_found = True
                break
        if not template1_found:
            print("在專武1中未找到Ultra rare")

    if points2:
        print("找到專武2")
        for point in points2:
            region = screenshot[point[1]-template2.shape[0]//2:point[1]+template2.shape[0]//2,
                                point[0]-template2.shape[1]//2:point[0]+template2.shape[1]//2]
            ultra_rare_points = template_matching(region, ultra_rare)
            if ultra_rare_points:
                print("在專武2中找到Ultra rare")
                template2_found = True
                break
        if not template2_found:
            print("在專武2中未找到Ultra rare")

    return template1_found and template2_found


def process_buttons_and_templates(iteration, retry_template, retry_confirm_template, skip_template, template1, template2, ultra_rare):
    global stop_script

    # 捕捉初始截圖
    screenshot = capture_screenshot()

    # 檢查是否有retry按鈕並且可以點擊
    retry_points = template_matching(screenshot, retry_template)
    print(f"Retry按鈕座標: {retry_points}")

    if retry_points:
        # 點擊retry按鈕
        pyautogui.click(retry_points[0])
        print(f"已點擊retry按鈕，座標 {retry_points[0]}")
        time.sleep(1.5)  # 根據電腦效能修改,建議為 1~2秒

        # 捕捉retry confirm按鈕後的截圖
        screenshot = capture_screenshot()
        retry_confirm_points = template_matching(
            screenshot, retry_confirm_template)
        print(f"Retry confirm按鈕座標: {retry_confirm_points}")
        if retry_confirm_points:
            pyautogui.click(retry_confirm_points[0])
            print(f"已點擊retry confirm按鈕，座標 {retry_confirm_points[0]}")
            time.sleep(1.5)  # 根據電腦效能修改,建議為 1~2秒

            # 捕捉skip按鈕後的截圖
            screenshot = capture_screenshot()
            skip_points = template_matching(screenshot, skip_template)
            print(f"Skip按鈕座標: {skip_points}")
            if skip_points:
                pyautogui.click(skip_points[0])
                print(f"已點擊skip按鈕，座標 {skip_points[0]}")
                time.sleep(1.5)  # 根據電腦效能修改,建議為 1~2秒

                # 捕捉截圖並檢查模板和Ultra rare
                screenshot = capture_screenshot()
                if template_within_template(screenshot, template1, template2, ultra_rare):
                    print("找到專武1和專武2中的Ultra rare。退出...")
                    return True

    return False


def check_stop_script():
    global stop_script
    while True:
        if keyboard.is_pressed('F9'):
            print("按下F9鍵。退出...")
            stop_script = True
            break
        time.sleep(0.1)


def main():
    global stop_script

    try:
        # 啟動線程來檢查F9鍵按下
        threading.Thread(target=check_stop_script, daemon=True).start()

        # 載入按鈕模板
        retry_template = load_image('retry.png')
        retry_confirm_template = load_image('retry_confirm.png')
        skip_template = load_image('skip.png')

        # 載入目標模板
        template1 = load_image('template1.png')
        template2 = load_image('template2.png')
        ultra_rare = load_image('ultra_rare.png')

        iteration = 0
        while not stop_script:
            iteration += 1
            print(f"運行次數 {iteration}")
            found = process_buttons_and_templates(
                iteration, retry_template, retry_confirm_template, skip_template, template1, template2, ultra_rare)
            if found or stop_script:
                break

            time.sleep(0.1)
    except Exception as e:
        print(f"運行過程中出現錯誤: {e}")
    finally:
        input("按下Enter鍵退出終端...")


if __name__ == "__main__":
    main()
