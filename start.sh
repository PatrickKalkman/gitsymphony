gource -o ./pytorch.ppm --seconds-per-day 0.01 \
       --max-files 5000 \
       --title "PyTorch" \
       --time-scale 1 \
       --font-size 25 \
       --hide filenames \
       --disable-auto-skip \
       --multi-sampling \
       --1280x720 \
       --output-framerate 25 \
       --filename-time 2 \
       --fullscreen \
       . 

gource --seconds-per-day 0.01 \
       --auto-skip-seconds 4 \
       --max-files 500 \
       --file-idle-time 60 \
       --title "PyTorch" \
       --font-size 24 \
       --filename-time 2 \
       --viewport 1280x720 \
       --output-custom-log ./pytorch.log \
       . 

gource -1280x720 -o - | ffmpeg -y -r 60 -f image2pipe -vcodec ppm -i - -vcodec libx264 -preset ultrafast -pix_fmt yuv420p -crf 1 -threads 0 -bf 0 gource.mp4

-output-custom-log gource.log

seconds per day = 0.01
datetime.datetime(2012, 1, 25, 13, 55, 20)
datetime.datetime(2025, 3, 17, 19, 34)
