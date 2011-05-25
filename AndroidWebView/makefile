SHELL = /bin/sh
export LANG = C
prefix = `pwd`

all: 
	@rm -rf $(prefix)/bin/*
	@convert -verbose -resize 48x48 res/drawable-hdpi/ic_launcher.png res/drawable/ic_launcher.png 
	@convert -verbose -resize 36x36 res/drawable-hdpi/ic_launcher.png res/drawable-ldpi/ic_launcher.png 
	@ant debug
	@cd $(HOME)/workspace/android-sdk-linux_x86/tools/
<<<<<<< HEAD
	@adb -e uninstall com.emainmacha.androidwebview
	@adb -e install $(prefix)/bin/AndroidWebView-debug.apk
=======

emu:
	@echo "Deinstalling application from device."
	@adb -e uninstall com.emainmacha.androidwebview
	@echo "Installing application from device."
	@adb -e install $(prefix)/bin/AndroidWebView-debug.apk

device:
	@echo "Deinstalling application from device."
	@adb -d uninstall com.emainmacha.androidwebview
	@echo "Installing application from device."
	@adb -d install $(prefix)/bin/AndroidWebView-debug.apk
>>>>>>> 68b8c95a7805ae715639229a353ade17ae1eb225


