package com.numa.app.Views;

import android.content.Context;
import android.util.AttributeSet;
import android.util.TypedValue;
import android.widget.LinearLayout;
import android.widget.TextView;

import androidx.annotation.Nullable;
import androidx.core.widget.TextViewCompat;

import java.util.ArrayList;

public class UniformTextLinearLayout extends LinearLayout {

  private int maxTextSize = Integer.MAX_VALUE;
  private ArrayList<TextView> childrens = new ArrayList<>();

  public UniformTextLinearLayout(Context context) {
    super(context);
  }

  public UniformTextLinearLayout(Context context, @Nullable AttributeSet attrs) {
    super(context, attrs);
  }

  public UniformTextLinearLayout(Context context, @Nullable AttributeSet attrs, int defStyleAttr) {
    super(context, attrs, defStyleAttr);
  }

  public UniformTextLinearLayout(
      Context context, AttributeSet attrs, int defStyleAttr, int defStyleRes) {
    super(context, attrs, defStyleAttr, defStyleRes);
  }

  public void onAutoSizeTextLayout(AutoSizeTextView textView) {
    if (maxTextSize > textView.getTextSize()) {
      maxTextSize = (int) textView.getTextSize();
    }

    if (!childrens.contains(textView)) {
      childrens.add(textView);
    }

    for (TextView child : childrens) {
      TextViewCompat.setAutoSizeTextTypeUniformWithConfiguration(
          child, 10, maxTextSize, 1, TypedValue.COMPLEX_UNIT_PX);
    }
  }
}
