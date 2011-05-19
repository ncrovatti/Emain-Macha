package com.emainmacha.androidwebview;

import android.app.Activity;
import android.os.Bundle;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.view.KeyEvent;

public class AndroidWebView extends Activity
{
	WebView mWebView;

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

        mWebView = (WebView) findViewById(R.id.webview);
        mWebView.setWebViewClient(new AndroidWebViewClient());
        mWebView.getSettings().setJavaScriptEnabled(true);
        mWebView.loadUrl("http://developers.kit-digital.com");
    }

    @Override
    public boolean onKeyDown(int keyCode, KeyEvent event) {
    	if ((keyCode == KeyEvent.KEYCODE_BACK) && mWebView.canGoBack()) {
    		mWebView.goBack();
    		return true;
    	}

    	return super.onKeyDown(keyCode, event);
	} 
}
