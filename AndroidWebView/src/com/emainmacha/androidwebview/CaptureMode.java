package com.emainmacha.androidwebview;

import java.io.File;

import android.app.Activity;
import android.os.Bundle;
import android.os.Environment;
import android.net.Uri;
import android.content.Context;
import android.content.Intent;
import android.widget.Toast;

import com.google.zxing.integration.android.IntentIntegrator;
import com.google.zxing.integration.android.IntentResult;

public class CaptureMode extends Activity
{
	
	/** Called when the activity is first created. */
    @Override
    public void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.camera);
		IntentIntegrator.initiateScan(this); 
    }

	@Override 
	protected void onActivityResult(int requestCode, int resultCode, Intent intent) 
	{
		Toast.makeText(this, "Result: " + IntentIntegrator.REQUEST_CODE, Toast.LENGTH_SHORT).show();

		if ((requestCode == IntentIntegrator.REQUEST_CODE) && (intent != null)) 
		{
			IntentResult scanResult = IntentIntegrator.parseActivityResult(requestCode, resultCode, intent);

			if (scanResult != null) 
			{
				String format  = scanResult.getFormatName();
	            String barcode = scanResult.getContents();
            }

			Toast.makeText(this, "Image capture successfull", Toast.LENGTH_SHORT).show();
		} 
		else if (resultCode == RESULT_CANCELED) 
		{
			Toast.makeText(this, "Image capture canceled", Toast.LENGTH_SHORT).show();
		}
	}
}
