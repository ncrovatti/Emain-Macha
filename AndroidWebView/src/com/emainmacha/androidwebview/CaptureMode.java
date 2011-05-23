package com.emainmacha.androidwebview;

import java.io.File;

import android.app.Activity;
import android.os.Bundle;
import android.os.Environment;
import android.net.Uri;
import android.content.Context;
import android.content.Intent;
import android.provider.MediaStore;
import android.widget.Toast;

import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import jp.sourceforge.qrcode.QRCodeDecoder;   
import jp.sourceforge.qrcode.data.QRCodeImage;   
import jp.sourceforge.qrcode.exception.DecodingFailedException;   
import jp.sourceforge.qrcode.exception.InvalidVersionInfoException;


public class CaptureMode extends Activity
{
	public static final int PICTURE_CAPTURED = 1;
	
	Uri outputFileUri;
	
	/** Called when the activity is first created. */
    @Override
    public void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.camera);

		Intent camera = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);
		File file     = new File(Environment.getExternalStorageDirectory(), "scanned-qrcode.jpg");
		outputFileUri = Uri.fromFile(file);

		camera.putExtra(MediaStore.EXTRA_OUTPUT, outputFileUri);
        startActivityForResult(camera, PICTURE_CAPTURED);
    }

	@Override
	protected void onActivityResult(int requestCode, int resultCode, Intent data) {
		if ((requestCode == PICTURE_CAPTURED) && (resultCode == Activity.RESULT_OK)) {
			// Check if the result includes a thumbnail Bitmap
			if (data == null) {
				Toast.makeText(this, "Image Captured, Data is null", Toast.LENGTH_SHORT).show();
				
				Toast.makeText(this, outputFileUri.toString(), Toast.LENGTH_SHORT).show();
				QRCodeDecoder decoder = new QRCodeDecoder();   
				Bitmap image = null;

				image = BitmapFactory.decodeFile(outputFileUri.toString());   

				String decodedData = new String(decoder.decode(new QRCodeImage(image)));  
			} 
			else {
				Toast.makeText(this, "Image Captured, Data is not null", Toast.LENGTH_SHORT).show();
			}
		}
	}
}
