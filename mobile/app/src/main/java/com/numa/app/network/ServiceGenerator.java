package com.numa.app.network;

import okhttp3.OkHttpClient;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;

class ServiceGenerator {

//  private static final String BASE_URL = "http://37.142.37.70:1684/api/";
  private static final String BASE_URL = "http://192.168.10.233/api/";
//  private static final String BASE_URL = "http://numa.gq/api/";

  private static Retrofit.Builder builder =
      new Retrofit.Builder().baseUrl(BASE_URL).addConverterFactory(GsonConverterFactory.create());

  private static Retrofit retrofit = builder.build();

  private static OkHttpClient.Builder httpClient = new OkHttpClient.Builder();

  public static <S> S createService(Class<S> serviceClass) {
    return retrofit.create(serviceClass);
  }
}
