package com.numa.app;

import android.app.Activity;
import android.app.ProgressDialog;
import android.content.Intent;
import android.graphics.Matrix;
import android.os.Bundle;
import android.util.DisplayMetrics;
import android.util.Rational;
import android.util.Size;
import android.view.Surface;
import android.view.TextureView;
import android.view.View;
import android.widget.FrameLayout;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;
import androidx.camera.core.CameraX;
import androidx.camera.core.ImageCapture;
import androidx.camera.core.ImageCaptureConfig;
import androidx.camera.core.Preview;
import androidx.camera.core.PreviewConfig;
import androidx.core.content.ContextCompat;

import com.numa.app.network.Network;

import java.io.File;

import okhttp3.ResponseBody;
import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class CameraActivity extends AppCompatActivity {

  private int currentPhoto;
  private TextView frontTitle, backTitle;
  private CameraX.LensFacing lensFacing = CameraX.LensFacing.BACK;
  private TextureView texture;
  private View button;
  private ImageCapture imageCapture;
  private File backgroundFile, foregroundFile;
  private View processingHolder, frontBackHolder;

  @Override
  protected void onCreate(Bundle savedInstanceState) {
    super.onCreate(savedInstanceState);
    setContentView(R.layout.activity_camera);
    frontBackHolder = findViewById(R.id.activity_camera_back_front_holder);
    processingHolder = findViewById(R.id.activity_camera_processing_holder);
    frontTitle = findViewById(R.id.activity_camera_front_side_text);
    backTitle = findViewById(R.id.activity_camera_back_side_text);
    texture = findViewById(R.id.activity_camera_texture);
    button = findViewById(R.id.activity_camera_button);
    currentPhoto = 1;

    initComponents();
  }

  private void initComponents() {
    frontBackHolder.setVisibility(View.VISIBLE);
    processingHolder.setVisibility(View.GONE);
    frontTitle.setTextColor(ContextCompat.getColor(this, android.R.color.white));
    backTitle.setTextColor(ContextCompat.getColor(this, android.R.color.darker_gray));

    texture.post(
        new Runnable() {
          @Override
          public void run() {
            startCamera();
          }
        });

    texture.addOnLayoutChangeListener(
        new View.OnLayoutChangeListener() {
          @Override
          public void onLayoutChange(
              View v,
              int left,
              int top,
              int right,
              int bottom,
              int oldLeft,
              int oldTop,
              int oldRight,
              int oldBottom) {
            updateTransform();
          }
        });

    button.setOnClickListener(
        new View.OnClickListener() {
          @Override
          public void onClick(View v) {
            if (imageCapture == null) {
              button.postDelayed(
                  new Runnable() {
                    @Override
                    public void run() {
                      onClick(button);
                    }
                  },
                  300);
            } else {
              File image = new File(getCacheDir() + "/image" + currentPhoto);
              button.setEnabled(false);
              imageCapture.takePicture(
                  image,
                  new ImageCapture.OnImageSavedListener() {
                    @Override
                    public void onImageSaved(@NonNull File file) {
                      if (currentPhoto == 2) {
                        backgroundFile = file;
                        processPhotos();
                      } else {
                        foregroundFile = file;
                        currentPhoto++;
                        frontTitle.setTextColor(ContextCompat.getColor(CameraActivity.this, android.R.color.darker_gray));
                        backTitle.setTextColor(ContextCompat.getColor(CameraActivity.this, android.R.color.white));
                        button.setEnabled(true);
                      }
                    }

                    @Override
                    public void onError(
                        @NonNull ImageCapture.UseCaseError useCaseError,
                        @NonNull String message,
                        @Nullable Throwable cause) {
                      Toast.makeText(
                              CameraActivity.this,
                              getString(R.string.something_went_wrong) + message,
                              Toast.LENGTH_LONG)
                          .show();
                      button.setEnabled(true);
                    }
                  });
            }
          }
        });
  }

  private void processPhotos() {
    frontBackHolder.setVisibility(View.GONE);
    processingHolder.setVisibility(View.VISIBLE);

    Network.postFiles(
        foregroundFile,
        backgroundFile,
        new Callback<ResponseBody>() {
          @Override
          public void onResponse(Call<ResponseBody> call, Response<ResponseBody> response) {
            Intent intent = new Intent(CameraActivity.this, ResultActivity.class);
            String responseString;
            try {
              responseString = response.body().string();
            } catch (Exception e) {
              responseString = getString(R.string.success_upload_no_response);
            }
            intent.putExtra(ResultActivity.DATA, responseString);
            startActivity(intent);
            finish();
          }

          @Override
          public void onFailure(Call<ResponseBody> call, Throwable t) {
            Intent intent = new Intent(CameraActivity.this, ResultActivity.class);
            intent.putExtra(ResultActivity.DATA, t.toString());
            startActivity(intent);
            finish();
          }
        });
  }

  private void startCamera() {
    DisplayMetrics metrics = new DisplayMetrics();
    texture.getDisplay().getRealMetrics(metrics);
    Size screenSize = new Size(metrics.widthPixels, metrics.heightPixels);
    Rational screenAspectRatio = new Rational(metrics.widthPixels, metrics.heightPixels);

    PreviewConfig previewConfig =
        new PreviewConfig.Builder()
            .setLensFacing(lensFacing)
            .setTargetResolution(screenSize)
            .setTargetAspectRatio(screenAspectRatio)
            .setTargetRotation(texture.getDisplay().getRotation())
            .build();

    Preview preview = new Preview(previewConfig);
    preview.setOnPreviewOutputUpdateListener(
        new Preview.OnPreviewOutputUpdateListener() {
          @Override
          public void onUpdated(Preview.PreviewOutput output) {
            texture.setSurfaceTexture(output.getSurfaceTexture());

            float width = output.getTextureSize().getWidth();
            float height = output.getTextureSize().getHeight();

            // Hack fix until CameraX api will fix it
            if (height < width) {
              float temp = width;
              width = height;
              height = temp;
            }
            if ((float) texture.getWidth() / (float) texture.getHeight() != width / height) {
              texture.setLayoutParams(
                  new FrameLayout.LayoutParams(
                      texture.getWidth(), (int) ((float) texture.getWidth() * height / width)));
            }

            updateTransform();
          }
        });

    ImageCaptureConfig imageCaptureConfig =
        new ImageCaptureConfig.Builder()
            .setLensFacing(lensFacing)
            .setTargetAspectRatio(screenAspectRatio)
            .setTargetRotation(texture.getDisplay().getRotation())
            .setCaptureMode(ImageCapture.CaptureMode.MAX_QUALITY)
            .build();

    imageCapture = new ImageCapture(imageCaptureConfig);

    CameraX.bindToLifecycle(this, preview, imageCapture);
  }

  private void updateTransform() {
    Matrix matrix = new Matrix();
    float centerX = texture.getWidth() / 2f;
    float centerY = texture.getHeight() / 2f;

    float rotationDegrees = 0;
    switch (texture.getDisplay().getRotation()) {
      case Surface.ROTATION_0:
        rotationDegrees = 0;
        break;
      case Surface.ROTATION_90:
        rotationDegrees = 90;
        break;
      case Surface.ROTATION_180:
        rotationDegrees = 180;
        break;
      case Surface.ROTATION_270:
        rotationDegrees = 270;
        break;
    }
    matrix.postRotate(-rotationDegrees, centerX, centerY);
    texture.setTransform(matrix);
  }
}
