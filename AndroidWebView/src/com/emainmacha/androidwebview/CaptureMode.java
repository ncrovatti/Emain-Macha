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

<<<<<<< HEAD
	@Override
	protected void onActivityResult(int requestCode, int resultCode, Intent data) {
		if ((requestCode == PICTURE_CAPTURED) && (resultCode == Activity.RESULT_OK)) {
			// Check if the result includes a thumbnail Bitmap
			if (data == null) {
				Toast.makeText(this, outputFileUri.toString(), Toast.LENGTH_SHORT).show();
				QRCodeDecoder decoder = new QRCodeDecoder();   
				Bitmap image = null;

				image = BitmapFactory.decodeFile(outputFileUri.toString());   
				
				String decodedData = new String(decoder.decode(new J2SEImage(image)));  
			} 
			else {
				Toast.makeText(this, "Image Captured, Data is not null", Toast.LENGTH_SHORT).show();
			}
=======
	@Override 
	protected void onActivityResult(int requestCode, int resultCode, Intent intent) 
	{
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
>>>>>>> 68b8c95a7805ae715639229a353ade17ae1eb225
		}
	}
}
