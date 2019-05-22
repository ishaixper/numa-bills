package com.numa.app;

import android.content.Context;
import android.content.pm.PackageManager;

public class CameraUtils {

  /** Check if this device has a camera */
  static boolean isCameraSupported(Context context) {
    return context.getPackageManager().hasSystemFeature(PackageManager.FEATURE_CAMERA);
  }
}
