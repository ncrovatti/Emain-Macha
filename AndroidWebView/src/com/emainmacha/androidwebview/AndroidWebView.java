package com.emainmacha.androidwebview;

import android.app.Activity;
import android.os.Bundle;
import android.webkit.WebView;
import android.webkit.WebSettings;
import android.webkit.WebViewClient;
import android.webkit.WebChromeClient;
import android.view.KeyEvent;
import android.util.Log;

public class AndroidWebView extends Activity
{

	public class JavaScriptInterface {
 	   Context mContext;

		/** Instantiate the interface and set the context */
		JavaScriptInterface(Context c) {
			mContext = c;
		}

		/** Show a toast from the web page */
		public void showToast(String toast) {
			Toast.makeText(mContext, toast, Toast.LENGTH_SHORT).show();
		}
	}
	private static WebView myWebView;

    private class AndroidWebViewClient extends WebViewClient {
    	@Override
    	public boolean shouldOverrideUrlLoading (WebView view, String url) {
    		view.loadUrl(url);
    		return true; 
    	}
    }

    /** Called when the activity is first created. */
    @Override
    public void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.main);

        myWebView = (WebView) findViewById(R.id.webview);
        myWebView.setWebViewClient(new AndroidWebViewClient());
		myWebView.setVerticalScrollBarEnabled(false);
		myWebView.setHorizontalScrollBarEnabled(false);
		myWebView.addJavascriptInterface(new JavaScriptInterface(this), "Android");
		myWebView.setWebChromeClient(new WebChromeClient() {
			public void onConsoleMessage(String message, int lineNumber, String sourceID) {
				Log.d("MyApplication", message + " -- From line " + lineNumber + " of " + sourceID);
			}
		});
        myWebView.getSettings().setJavaScriptEnabled(true);
        myWebView.getSettings().setPluginsEnabled(true);
       	myWebView.loadUrl("http://ncrovatti.cardinet.kewego.int:1234/droid.html");
//        myWebView.loadUrl("http://linuxfr.org/");
    }

    @Override
    public boolean onKeyDown(int keyCode, KeyEvent event) {
    	if ((keyCode == KeyEvent.KEYCODE_BACK) && myWebView.canGoBack()) {
    		myWebView.goBack();
    		return true;
    	}

    	return super.onKeyDown(keyCode, event);
	} 
}
