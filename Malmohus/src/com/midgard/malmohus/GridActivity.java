package com.midgard.malmohus;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;

import android.view.Menu;
import android.view.MenuInflater;
import android.view.MenuItem;

import android.util.Log;

public class GridActivity extends Activity {

	@Override
	public void onCreate(Bundle savedInstanceState) 
	{
		super.onCreate(savedInstanceState);
		setContentView(R.layout.grid);
	}

	@Override
	public boolean onCreateOptionsMenu(Menu menu) 
	{
		super.onCreateOptionsMenu(menu);
		MenuInflater inflater = getMenuInflater();
		inflater.inflate(R.menu.menu, menu);
		return true;
	}
	
	public boolean onOptionsItemSelected(MenuItem item) 
	{
		Log.v("INFO", "" + item.getItemId());
		Log.v("INFO", "" + R.id.settings);
		if (item.getItemId() == R.id.settings) 
		{
			startActivity(new Intent(getBaseContext(), PreferencesActivity.class));
			return true;
		}
		return false;
	}

}
