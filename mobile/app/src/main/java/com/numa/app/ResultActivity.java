package com.numa.app;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.TextView;

import androidx.annotation.Nullable;

public class ResultActivity extends Activity {

  public static final String DATA = "data";

    @Override
    protected void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_result);

        Intent intent = getIntent();
        if (intent != null) {
            String result = intent.getStringExtra(DATA);
            if (result != null) {
                ((TextView)findViewById(R.id.activity_result_result_textbox)).setText(result);
            }
        }

        findViewById(R.id.activity_result_btn_take_picture).setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                startActivity(new Intent(ResultActivity.this, CameraActivity.class));
            }
        });

//        findViewById(R.id.activity_result_btn_back).setOnClickListener(new View.OnClickListener() {
//            @Override
//            public void onClick(View v) {
//                onBackPressed();
//            }
//        });

        findViewById(R.id.activity_result_btn_get_grade).setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                startActivity(new Intent(ResultActivity.this, GradeEstimateActivity.class));
            }
        });

        findViewById(R.id.activity_result_btn_my_collection).setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                startActivity(new Intent(ResultActivity.this, MyCollectionActivity.class));
            }
        });


        findViewById(R.id.activity_result_btn_wants_to_buy).setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                startActivity(new Intent(ResultActivity.this, WantToBuyActivity.class));
            }
        });

        findViewById(R.id.activity_result_btn_wants_to_sell).setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                startActivity(new Intent(ResultActivity.this, WantToSellActivity.class));
            }
        });

    }

    @Override
    public void onBackPressed() {
        startActivity(new Intent(this, MainActivity.class));
        finish();
    }
}
