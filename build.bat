@echo off
echo "Building one-folder bundle"
pyinstaller main.py --clean -D -n Rental_Kendaraan
echo "Building one-file bundle"
pyinstaller main.py --clean -F -n Rental_Kendaraan
PAUSE