# Build APK using Google Colab

Since you are on Windows, the easiest way to build the APK is using Google Colab.

1.  **Create a new Notebook** in Google Colab.
2.  **Upload Files**:
    -   Upload the entire `mobile_app` folder content to the Colab environment.
    -   Ensure `main.py`, `screens.py`, `database.py`, and `buildozer.spec` are in the root or same directory.
3.  **Run the following commands** in a cell:

```python
!pip install buildozer cython==0.29.33

!sudo apt-get update
!sudo apt-get install -y \
    python3-pip \
    build-essential \
    git \
    python3 \
    python3-dev \
    ffmpeg \
    libsdl2-dev \
    libsdl2-image-dev \
    libsdl2-mixer-dev \
    libsdl2-ttf-dev \
    libportmidi-dev \
    libswscale-dev \
    libavformat-dev \
    libavcodec-dev \
    zlib1g-dev

!sudo apt-get install -y libgstreamer1.0 \
    gstreamer1.0-plugins-base \
    gstreamer1.0-plugins-good

!sudo apt-get install build-essential libsqlite3-dev sqlite3 bzip2 libbz2-dev zlib1g-dev libssl-dev openssl libgdbm-dev libgdbm-compat-dev liblzma-dev libreadline-dev libncursesw5-dev libffi-dev uuid-dev libopenjp2-7-dev

!buildozer init
# (If you already have buildozer.spec, skip init and just upload it)

!buildozer -v android debug
```

4.  **Download APK**:
    -   Once the build finishes (it takes 15-20 mins), the APK will be in the `bin/` folder.
