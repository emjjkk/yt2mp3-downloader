from flask import Flask, render_template, request, redirect, url_for, send_file
import pafy
import os

app = Flask(__name__)

DOWNLOAD_FOLDER = 'downloads'
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    download_links = {}
    if request.method == 'POST':
        url = request.form.get('url')
        try:
            video = pafy.new(url)
            best_audio = video.getbestaudio()
            best_video = video.getbest()
            
            download_links = {
                'title': video.title,
                'mp3': url_for('download', url=url, format='mp3'),
                'mp4': url_for('download', url=url, format='mp4')
            }
        except Exception as e:
            return f"Error: {e}"
    
    return render_template('index.html', download_links=download_links)

@app.route('/download')
def download():
    url = request.args.get('url')
    format_type = request.args.get('format')

    if not url or not format_type:
        return redirect(url_for('index'))

    try:
        video = pafy.new(url)
        if format_type == 'mp3':
            best_audio = video.getbestaudio()
            filename = os.path.join(DOWNLOAD_FOLDER, f"{video.title}.mp3")
            best_audio.download(filepath=filename)
        elif format_type == 'mp4':
            best_video = video.getbest()
            filename = os.path.join(DOWNLOAD_FOLDER, f"{video.title}.mp4")
            best_video.download(filepath=filename)
        else:
            return "Invalid format"

        return send_file(filename, as_attachment=True)
    except Exception as e:
        return f"Error: {e}"

if __name__ == '__main__':
    app.run(debug=True)
