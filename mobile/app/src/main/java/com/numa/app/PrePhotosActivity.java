package com.numa.app;

import android.Manifest;
import android.annotation.SuppressLint;
import android.app.Activity;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.os.Bundle;
import android.view.View;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;

public class PrePhotosActivity extends Activity {

  private static final int MY_PERMISSIONS_REQUEST_CAMERA = 10;
  private TextView mainTextView;

  @Override
  protected void onCreate(Bundle savedInstanceState) {
    super.onCreate(savedInstanceState);

    setContentView(R.layout.activity_pre_photo);

    mainTextView = findViewById(R.id.activity_pre_photo_textbox);
    View button = findViewById(R.id.activity_pre_photo_btn_take_picture);

    if (!CameraUtils.isCameraSupported(this)) {
      mainTextView.setText(R.string.no_camera_found);
      button.setEnabled(false);
      finish();
    }

    button.setOnClickListener(
        new View.OnClickListener() {
          @Override
          public void onClick(View v) {
            capturePhotos();
          }
        });
  }

  private void capturePhotos() {
    if (ContextCompat.checkSelfPermission(this, Manifest.permission.CAMERA)
        != PackageManager.PERMISSION_GRANTED) {
      ActivityCompat.requestPermissions(
          this, new String[] {Manifest.permission.CAMERA}, MY_PERMISSIONS_REQUEST_CAMERA);
    } else {
      startCameraActivity();
    }
  }

  private void startCameraActivity() {
    startActivity(new Intent(this, CameraActivity.class));
  }

  @Override
  public void onRequestPermissionsResult(
      int requestCode, String[] permissions, int[] grantResults) {
    switch (requestCode) {
      case MY_PERMISSIONS_REQUEST_CAMERA:
        if (grantResults.length > 0 && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
          startCameraActivity();
        } else {
          mainTextView.setText(R.string.permission_denied);
        }
        return;
    }
  }
}
