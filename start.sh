gource -o ./pytorch.ppm --seconds-per-day 0.01 \
       --max-files 7000 \
       --title "PyTorch" \
       --time-scale 1 \
       --font-size 25 \
       --hide filenames,users,dirnames \
       --disable-auto-skip \
       --multi-sampling \
       --1280x720 \
       --output-framerate 25 \
       --bloom-intensity 0.3 \
       --filename-time 2 \
       --background 000000 \
       --font-colour 555555 \
       . 

gource -o ./tensorflow.ppm --seconds-per-day 0.01 \
       --max-files 7000 \
       --title "Tensorflow" \
       --time-scale 1 \
       --font-size 25 \
       --output-custom-log ./tensorflow.log \
       --hide filenames,users,dirnames \
       --disable-auto-skip \
       --multi-sampling \
       --1280x720 \
       --output-framerate 25 \
       --bloom-intensity 0.3 \
       --filename-time 2 \
       --background 000000 \
       --font-colour 555555 \
       --fullscreen \
       . 

gource -o ./langchain.ppm --seconds-per-day 0.05 \
       --max-files 7000 \
       --title "Langchain" \
       --time-scale 1 \
       --font-size 25 \
       --hide filenames,users,dirnames \
       --output-custom-log ./langchain.log \
       --disable-auto-skip \
       --multi-sampling \
       --1280x720 \
       --output-framerate 25 \
       --bloom-intensity 0.3 \
       --filename-time 2 \
       --background 000000 \
       --font-colour 555555 \
       --fullscreen \
       . 

gource -o ./transformers.ppm --seconds-per-day 0.01 \
       --max-files 10000 \
       --title "" \
       --time-scale 1 \
       --font-size 25 \
       --hide filenames,users,dirnames,date \
       --disable-auto-skip \
       --multi-sampling \
       --1920x1080 \
       --output-framerate 25 \
       --bloom-intensity 0.4 \
       --filename-time 2 \
       --background 000000 \
       --font-colour 555555 \
       --fullscreen \
       .        

gource -o ./scikit-learn.ppm --seconds-per-day 0.01 \
       --max-files 7000 \
       --title "Scikit-learn" \
       --time-scale 1 \
       --font-size 25 \
       --hide filenames,users,dirnames \
       --output-custom-log ./scikit-learn.log \
       --disable-auto-skip \
       --multi-sampling \
       --1280x720 \
       --output-framerate 25 \
       --bloom-intensity 0.3 \
       --filename-time 2 \
       --background 000000 \
       --font-colour 555555 \
       --fullscreen \
       .      

       --output-custom-log ./tensorflow.log \


--output-custom-log ./tensorflow.log \

--user-font-size 12 --font-colour 555555 --bloom-intensity 0.1


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
