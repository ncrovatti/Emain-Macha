package com.midgard.malmohus;

import android.app.Activity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.view.View.OnClickListener;
import android.content.Intent;
	
public class MalmohusMainActivity extends Activity implements OnClickListener
{
    /** Called when the activity is first created. */
    @Override
    public void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.main);

		View newGameButton = findViewById(R.id.new_game_button);
        newGameButton.setOnClickListener(this);

        View aboutButton = findViewById(R.id.about_button);
        aboutButton.setOnClickListener(this);
    }

	@Override
    public void onClick(View v) 
    {
    	switch (v.getId()) {
    		case R.id.new_game_button: 
    			Intent gridIntent = new Intent(this, GridActivity.class);
    			startActivity(gridIntent);
    		break;
    		case R.id.about_button:
    			Intent aboutIntent = new Intent(this, AboutActivity.class);
    			startActivity(aboutIntent);
    		break;
    	}
    }
}
