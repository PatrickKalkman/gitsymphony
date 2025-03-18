gource -o ./pytorch.ppm --seconds-per-day 0.01 \
       --auto-skip-seconds 4 \
       --max-files 500 \
       --file-idle-time 60 \
       --title "PyTorch" \
       --font-size 24 \
       --filename-time 2 \
       --viewport 1280x720 \
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