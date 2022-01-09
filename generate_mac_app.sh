#/bin/bash
rm -rf __pycache__ build dist
pyinstaller sea_snake_game_cnl.py -n SeaSnakeCNL --windowed --noconfirm --onefile --add-data 'bg01.jpg:.' --add-data 'bg02.jpg:.' --add-data 'bg03.png:.' --add-data 'bite.wav:.' --add-data 'bomb_exploding.wav:.' --add-data 'eating_chips.wav:.'
cp *.wav *.jpg *.png dist/SeaSnakeCNL.app/Contents/MacOS/
cp *.wav *.jpg *.png dist/SeaSnakeCNL.app/Contents/Resources/
