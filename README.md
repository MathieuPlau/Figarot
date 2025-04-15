# Figarot – The Mischievous Maestro of Your Raspberry Pi 🎶

A tiny Flask-powered daemon with a big personality. Figarot plays sounds, talks back, and brings your Pi to life with flair—whether it’s a jingle, a dramatic entrance, a groovy sample, or just a sarcastic comment in French. Built for fun, designed for flexibility, and unafraid to make noise, Figarot is your perfect buddy to add joy (and a little chaos) to your openspace.

---

## 🧠 How It Works

Figarot is a lightweight Python project that lets you trigger sound samples straight from your web browser.

- Organize your sound samples in folders.
- Set the sample path in `config.py` using `SAMPLE_PATH`.
- Sample files are available here: [MathieuPlau/samples](https://github.com/MathieuPlau/samples) as a submodule—but feel free to use your own!
- Run `run.py` to launch the daemon.
- Flask will start a web server—you’ll get the address in your terminal.

That’s it. Open the browser. Push the buttons. Make noise. Enjoy.

---

## 📦 Dependencies

- [`Flask`](https://palletsprojects.com/p/flask/) – the web framework  
- [`simpleaudio`](https://simpleaudio.readthedocs.io/) – plays WAV files reliably  
- [`pygame`](https://www.pygame.org/) – for MP3 playback  
- [`gTTS`](https://pypi.org/project/gTTS/) – text-to-speech, with sass

---

Feel free to contribute, fork, or just sit back and let Figarot serenade your office.
