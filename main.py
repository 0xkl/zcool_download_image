import logging
import concurrent.futures
from function.download_main import xhs_main,zcool_main,behance_main
from flask import Flask, render_template, request, redirect, url_for
# 终端日志系统
log_file = './download.log'
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', encoding='utf-8')

# 创建线程池
executor = concurrent.futures.ThreadPoolExecutor(max_workers=3)

# 网页请求头
headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 Edg/87.0.664.75'
    }

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        selected_site = request.form.get('site')
        if selected_site == 'xhs':
            return redirect(url_for('xhs_form'))
        elif selected_site == 'zcool':
            return redirect(url_for('zcool_form'))
        elif selected_site =='behance':
            return redirect(url_for('behance_form'))
        
    return render_template('index.html')

@app.route('/zcool', methods=['GET', 'POST'])
def zcool_form():
    if request.method == 'POST':
        zcool_url = request.form.get('zcool_url')
        download_name = request.form.get('zcool_name')     # 控制谁在用的变量，并且创建他的名字

        # title 用来返回标题
        # folder_path 用来返回目录地址
        # title, folder_path = zcool_main(zcool_url,download_name,headers)
        # 创建任务，等待任务执行完毕，提取title，folder_path
        future = executor.submit(zcool_main, zcool_url, download_name, headers)
        concurrent.futures.wait([future])
        title, folder_path = future.result()

        return redirect(url_for('result', title=title, folder_path=folder_path, site='zcool'))
    return render_template('zcool_form.html')

@app.route('/xhs', methods=['GET', 'POST'])
def xhs_form():
    if request.method == 'POST':
        xhs_url = request.form.get('xhs_url')
        download_name = request.form.get('xhs_name')
        ''' 自用
        user_id = request.form.get('xhs_name')    # 控制谁在用的变量，并且创建他的名字
        xhs_user_id = request.form.get('xhs_user_id')
        download_name = f'{user_id}/小红书/{xhs_user_id}/'
        '''
        # title 用来返回标题
        # folder_path 用来返回目录地址
        # title,folder_path = xhs_main(xhs_url,download_name)
        # 多线程
        future = executor.submit(xhs_main, xhs_url, download_name)
        concurrent.futures.wait([future])
        title,folder_path = future.result()

        return redirect(url_for('result', title=title, folder_path=folder_path, site='xhs'))
    return render_template('xhs_form.html')


# 待测试 behance download
@app.route('/behance',methods=['GET', 'POST'])
def behance_form():
    if request.method == 'POST':
        behance_url = request.form.get('behance_url')
        download_name = request.form.get('behance_name')

        #behance_main(behance_url, download_name, "Project-title-Q6Q")
        # 多线程 # 搜查  <span class="Project-title-Q6Q"></span> 类标签内容作为标题
        executor.submit(behance_main,behance_url, download_name, "Project-title-Q6Q")
        
        return redirect(url_for('result',site='behance'))
    return render_template('behance_form.html')


@app.route('/result', methods=['GET'])
def result():
    title = request.args.get('title')   # 返回标题
    folder_path = request.args.get('folder_path')   # 返回地址
    download_log = request.args.get('download_log') # 返回日志
    site = request.args.get('site')
    return render_template('result.html', title=title, folder_path=folder_path, site=site)

if __name__ == '__main__':
    app.run(host='192.168.0.33', port='8080',debug=True)