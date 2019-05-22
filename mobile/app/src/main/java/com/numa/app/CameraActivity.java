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
import android.widget.TextView;
import android.widget.Toast;

import com.numa.app.network.Network;

import java.io.File;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;
import androidx.camera.core.CameraX;
import androidx.camera.core.ImageCapture;
import androidx.camera.core.ImageCaptureConfig;
import androidx.camera.core.Preview;
import androidx.camera.core.PreviewConfig;
import okhttp3.ResponseBody;
import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class CameraActivity extends AppCompatActivity {

  public static final String POST_URL = "http://numa.gq/api/detect";

  private int currentPhoto;
  private TextView title;
  private CameraX.LensFacing lensFacing = CameraX.LensFacing.BACK;
  private TextureView texture;
  private View button;
  private ImageCapture imageCapture;
  private File backgroundFile, foregroundFile;

  @Override
  protected void onCreate(Bundle savedInstanceState) {
    super.onCreate(savedInstanceState);
    setContentView(R.layout.activity_camera);
    title = findViewById(R.id.activity_camera_textbox);
    texture = findViewById(R.id.activity_camera_texture);
    button = findViewById(R.id.activity_camera_button);
    currentPhoto = 1;

    initComponents();
  }

  private void initComponents() {
    title.setText(R.string.fetch_bill_foreground);

    texture.post(
        new Runnable() {
          @Override
          public void run() {
            startCamera();
          }
        });

    // Every time the provided texture view changes, recompute layout
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
                        Toast.makeText(
                                CameraActivity.this,
                                R.string.photo_taken_successfully,
                                Toast.LENGTH_LONG)
                            .show();

                        foregroundFile = file;
                        currentPhoto++;
                        title.setText(R.string.fetch_bill_background);
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
    final ProgressDialog pd = new ProgressDialog(this);
    pd.setMessage(getString(R.string.uploading_message));
    pd.show();

    Network.postFiles(
        POST_URL,
        foregroundFile,
        backgroundFile,
        new Callback<ResponseBody>() {
          @Override
          public void onResponse(Call<ResponseBody> call, Response<ResponseBody> response) {
            pd.dismiss();
            Intent intent = new Intent();
            intent.putExtra("data", "BLA");
            setResult(Activity.RESULT_OK, intent);
            finish();
          }

          @Override
          public void onFailure(Call<ResponseBody> call, Throwable t) {
            pd.dismiss();
            setResult(Activity.RESULT_CANCELED);
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
            .setTargetRotation(getWindowManager().getDefaultDisplay().getRotation())
            .setTargetRotation(texture.getDisplay().getRotation())
            .build();

    Preview preview = new Preview(previewConfig);
    preview.setOnPreviewOutputUpdateListener(
        new Preview.OnPreviewOutputUpdateListener() {
          @Override
          public void onUpdated(Preview.PreviewOutput output) {
            texture.setSurfaceTexture(output.getSurfaceTexture());
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
