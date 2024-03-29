from flask import Flask, render_template, request, redirect, url_for, session
import os
import ffmpeg
import yt_dlp
import subprocess
from ibm_watson import SpeechToTextV1
#from ibm_watson.websocket import RecognizeCallback, AudioSource
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains


app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/summarize',methods=['GET','POST'])
def summarization():

    if 'transcript_session' in session:
        transcript_text = session['transcript_session']
        print("\n\n",transcript_text,"\n\n")
    else:
        return redirect(url_for('transcription'))

    #if request.method=="POST":
    #webscraping summerized text

    options = Options()
    #options.add_experimental_option("detach", True)
    options.add_argument('--headless') 
    driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))
    driver.get("https://www.semrush.com/goodcontent/summary-generator/")

    wait = WebDriverWait(driver, 7, 2, ignored_exceptions=[ElementClickInterceptedException])
    obj = ActionChains(driver)

    wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/section/div/div[1]/div[2]/button[1]"))).click()
    bullet_pt = driver.find_element(by="xpath", value="//span[normalize-space()='Bullet Points']")
    obj.move_to_element(bullet_pt).click().perform()

    def send_text(text):
        input_text_area = driver.find_element(by="xpath", value="//textarea[@id='input']")
        input_text_area.send_keys(text)
    send_text(transcript_text)

    summerize_btn = driver.find_element(by="xpath", value="//button[@aria-label='Summarize text']//span[@class='___SInner_1ab13_gg_']")
    obj.move_to_element(summerize_btn).click().perform()
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "gch-1k34ke5")))
    summ = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@aria-label='Summary']")))
    summerized_text = summ.text
    final_summerized_text = summerized_text.split("\n")

    print("\n\n",final_summerized_text,"\n\n")


    return render_template('index.html',text=final_summerized_text)


@app.route('/transcribe',methods=['GET','POST'])
def transcription():
    apikey = 'LFkzx_UQCpr2QvgszR-0oz9L3ToszpMke0R7D7PDcWs4'
    url = 'https://api.au-syd.speech-to-text.watson.cloud.ibm.com/instances/31b9f2a5-d2fe-4254-a051-accc44f5b454'

    file_name="Video"
    output_dir="downloads"
    transcript=None

    if request.method == 'POST':

        #Downlaod video 
        yt_url=request.form.get('url_input','None')
        print(yt_url)

        os.makedirs('D:\\Nikhil\\VScode\\LTI\\Transcriber\\downloads', exist_ok=True) 
        output_path = os.path.join(output_dir, f"{file_name}.%(ext)s")

        ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': output_path,
        'keepvideo': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([yt_url])

        #extract audio from video
        input_Video="D:\\Nikhil\\VScode\\LTI\\Transcriber\\downloads\\Video.mp4"
        output_Audio = "D:\\Nikhil\\VScode\\LTI\\Transcriber\\downloads\\Audio.mp3"
        subprocess.run(["ffmpeg", "-i", input_Video, output_Audio])

        #Convert Audio to text using IBM service
            # setup service
        authenticator = IAMAuthenticator(apikey)
        stt = SpeechToTextV1(authenticator=authenticator)
        stt.set_service_url(url)

        with open(output_Audio,"rb") as f:
            res = stt.recognize(audio=f, content_type="audio/mp3", model="en-AU_NarrowbandModel").get_result()
        print("\n\n",res,"\n\n")

        text = [result['alternatives'][0]['transcript'].strip() + '. ' for result in res['results']]
        #text = [para[0].title() + para[1: ] for para in text]
        transcript = ''.join(text)
        print(transcript)

        def delete_files():
            video_file_path = 'D:\\Nikhil\\VScode\\LTI\\Transcriber\\downloads\\Video.mp4'
            download_folder_path = 'D:\\Nikhil\\VScode\\LTI\\Transcriber\\downloads'

            if os.path.exists(video_file_path):
                for filename in os.listdir(download_folder_path):
                    file = os.path.join(download_folder_path, filename)
                    #Check if the path is a file (not a directory)
                    if os.path.isfile(file):
                        # Remove the file
                        os.remove(file)
                print("all files deleted")

            else:
                print(f"The file '{video_file_path}' does not exist.")
        delete_files()
        
        session['transcript_session'] = transcript
        session.modified=True

    return render_template('index.html',transcript=transcript)


    

if __name__ == "__main__":
    app.run(debug=True)