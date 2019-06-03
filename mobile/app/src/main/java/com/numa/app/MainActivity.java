package com.numa.app;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;

import androidx.annotation.Nullable;

public class MainActivity extends Activity {

    @Override
    protected void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
    }

    public void mainButtonClicked(View view) {
        switch (view.getId()) {
            case R.id.activity_main_button_note_identification:
                startActivity(new Intent(this, PrePhotosActivity.class));
                break;
        }
    }
}
