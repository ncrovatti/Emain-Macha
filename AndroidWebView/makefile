SHELL = /bin/sh
export LANG = C
prefix = `pwd`

all: 
	@rm -rf $(prefix)/bin/*
	@convert -verbose -resize 48x48 res/drawable-hdpi/ic_launcher.png res/drawable/ic_launcher.png 
	@convert -verbose -resize 36x36 res/drawable-hdpi/ic_launcher.png res/drawable-ldpi/ic_launcher.png 
	@ant debug
	@cd $(HOME)/workspace/android-sdk-linux_x86/tools/
	@adb -e uninstall com.emainmacha.androidwebview
	@adb -e install $(prefix)/bin/AndroidWebView-debug.apk


