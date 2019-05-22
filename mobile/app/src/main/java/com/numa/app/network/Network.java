package com.numa.app.network;

import android.util.Log;

import java.io.File;

import androidx.annotation.NonNull;
import okhttp3.MediaType;
import okhttp3.MultipartBody;
import okhttp3.RequestBody;
import okhttp3.ResponseBody;
import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;
import retrofit2.http.Multipart;
import retrofit2.http.POST;
import retrofit2.http.Part;

public class Network {

  public static void postFiles(
      String url, File file1, File file2, final Callback<ResponseBody> callback) {
    FileUploadService service = ServiceGenerator.createService(FileUploadService.class);

    // create part for file (photo, video, ...)
    MultipartBody.Part body1 = prepareFilePart("front", file1);
    MultipartBody.Part body2 = prepareFilePart("back", file2);

    Call<ResponseBody> call = service.uploadMultipleFiles(body1, body2);
    call.enqueue(
        new Callback<ResponseBody>() {
          @Override
          public void onResponse(Call<ResponseBody> call, Response<ResponseBody> response) {
            Log.d("aaa", "success4 " + response.message());
            callback.onResponse(call, response);
          }

          @Override
          public void onFailure(Call<ResponseBody> call, Throwable t) {
            Log.d("aaa", "error : " + t.getMessage());
            callback.onFailure(call, t);
          }
        });
  }

  @NonNull
  private static MultipartBody.Part prepareFilePart(String partName, File file) {
    RequestBody requestFile = RequestBody.create(MediaType.parse("image/*"), file);

    return MultipartBody.Part.createFormData(partName, file.getName(), requestFile);
  }

  public interface FileUploadService {
    @Multipart
    @POST("detection")
    Call<ResponseBody> uploadMultipleFiles(
        @Part MultipartBody.Part file1, @Part MultipartBody.Part file2);
  }
}
