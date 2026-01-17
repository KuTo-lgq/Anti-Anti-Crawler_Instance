import ddddocr
from selenium.webdriver.edge.options import Options
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 1. 创建链接
# 创建EdgeOptions对象，用于配置Edge浏览器的选项
edge_options = Options()
# 添加启动参数，'--disable-gpu'参数用于禁用GPU加速，适用于部分平台上的兼容性问题
edge_options.add_argument('--disable-gpu')

# 2. 添加请求头伪装浏览器
edge_options.add_argument(
    'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0')

# 3. 创建Edge浏览器实例
driver = webdriver.Edge(options=edge_options)

# 4. 执行 `stealth.min.js` 文件进行隐藏浏览器指纹
with open('stealth.min.js') as f:
    js = f.read()
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": js
})

# 5. 最大化浏览器窗口
driver.maximize_window()

# 6. 发送请求，打开网页
driver.get('https://captcha7.scrape.center/')
time.sleep(1)

# 7. 输入账号密码
username_input = driver.find_element(by=By.XPATH, value="//div[@class='el-tooltip username item el-input']/input")  # 定位账号框
username_input.send_keys("admin")  # 输入账号信息（这里自行替换）

password_input = driver.find_element(by=By.XPATH, value="//div[@class='el-tooltip password item el-input']/input")  # 定位密码框
password_input.send_keys("admin")  # 输入密码信息（这里自行替换）

# 8. 下载验证码
element = driver.find_element(By.ID, 'captcha')  # 定位验证码
element.screenshot('test.png')  # 保存截图

# 9. 识别验证码
# 创建DdddOcr对象
ocr = ddddocr.DdddOcr(show_ad=False)

# 读取图片
with open('test.png', 'rb') as f:
    img = f.read()
# 识别图片内验证码并返回字符串
result = ocr.classification(img)
print("识别结果：",result)

# 10. 输入验证码
yzm = driver.find_element(by=By.XPATH, value="//div[@class='captcha el-input']/input") # 定位账号框
yzm.clear()  # 清空默认文本
yzm.send_keys(result)

# 11. 点击登录按钮元素
login_button = driver.find_element(by=By.XPATH, value="//button[@class='el-button login el-button--primary']")
# 点击登录按钮
login_button.click()

# 等待页面加载完成
WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.TAG_NAME, "body"))
)

# 12. 进行截图
driver.save_screenshot('1.png')

# 13.  获取页面上所有可见元素的文本内容
all_text = []
elements = driver.find_elements(By.XPATH, "//*[not(self::script or self::style)]")
for element in elements:
    text = element.text.strip()
    if text:  # 如果元素包含文本，则添加到列表中
        all_text.append(text)
        print("文本为：", text)
        break

# 14. 爬取网页结构
page_source = driver.page_source
with open('page_source.html', 'w', encoding='utf-8') as file:
    file.write(page_source)
print("网页结构已保存到 'page_source.html' 文件中。")

# 15. 关闭浏览器
driver.quit()
