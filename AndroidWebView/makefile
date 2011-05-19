SHELL = /bin/sh
export LANG = C
prefix = `pwd`

all: 
	@ant debug
	@cd $(HOME)/workspace/android-sdk-linux_x86/tools/
	@adb uninstall com.emainmacha.androidwebview
	@adb install $(prefix)/bin/AndroidWebView-debug.apk


