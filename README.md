# Youtube_Video_Transcriber

* testing video link : https://www.youtube.com/watch?v=ZU0f8_C5Pm0

### download below packages:
  * Flask: pip install Flask
  *	ffmpeg-python: pip install ffmpeg-python
  * yt-dlp: pip install yt-dlp
  *	ibm-watson: pip install ibm-watson
  *	selenium: pip install selenium
  *	webdriver-manager: pip install webdriver-manager

### This project is build for Transcribing the Youtube Videos. Also the summarization of transcribed text is done and both are displayed on the webpage 
### We did not use any NLP frameworks for summarizing the text, intead we use a free website that helps in summarizing the text and for that automation is done using 'Selenium' framework.
### Here we used the IBM cloud service of 'Audio-to-Text' and for that you will require the 
  * apikey = 'api-key-of-your-cloud-service(audio-to-text)'
  * url = 'url-of-cloud-service'

### IBM provides audio-to-text service for free(500 minutes for a month)
### You can convert audio of total 500 minutes in a month 
