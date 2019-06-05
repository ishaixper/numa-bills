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
            case R.id.activity_main_button_grade_estimation:
                startActivity(new Intent(this, GradeEstimateActivity.class));
                break;
            case R.id.activity_main_button_want_to_buy:
                startActivity(new Intent(this, WantToBuyActivity.class));
                break;
            case R.id.activity_main_button_want_to_sell:
                startActivity(new Intent(this, WantToSellActivity.class));
                break;
            case R.id.activity_main_button_my_collection:
                startActivity(new Intent(this, MyCollectionActivity.class));
                break;
        }
    }
}
