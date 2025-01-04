

#find ./ -type f -name "*.py" 
#find ./ -type f -name "*.py" | xargs sed -i -e "s/PyQt6/PySide6/g"
find ./ -type f -name "*.py" | xargs sed -i -e "s/pyqtSignal/Signal/g"



