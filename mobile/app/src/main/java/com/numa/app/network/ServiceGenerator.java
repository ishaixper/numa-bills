package com.numa.app.network;

import java.util.concurrent.TimeUnit;

import okhttp3.OkHttpClient;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;

class ServiceGenerator {

  private static final String BASE_URL = "http://numa.gq/api/";

  private static OkHttpClient httpClient =
      new OkHttpClient.Builder()
          .callTimeout(60, TimeUnit.SECONDS)
          .connectTimeout(60, TimeUnit.SECONDS)
          .readTimeout(60, TimeUnit.SECONDS)
          .writeTimeout(60, TimeUnit.SECONDS)
          .build();

  private static Retrofit.Builder builder =
      new Retrofit.Builder()
          .baseUrl(BASE_URL)
          .client(httpClient)
          .addConverterFactory(GsonConverterFactory.create());

  private static Retrofit retrofit = builder.build();

  public static <S> S createService(Class<S> serviceClass) {
    return retrofit.create(serviceClass);
  }
}
