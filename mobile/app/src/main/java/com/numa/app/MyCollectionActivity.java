package com.numa.app;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import androidx.annotation.Nullable;

public class MyCollectionActivity extends Activity {

    @Override
    protected void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_my_collection);


        findViewById(R.id.activity_my_collection_frame).setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
            Intent intent = new Intent(MyCollectionActivity.this, CollectionCategoryActivity.class);
            startActivity(intent);
            finish();
            }
        });
    }
}
