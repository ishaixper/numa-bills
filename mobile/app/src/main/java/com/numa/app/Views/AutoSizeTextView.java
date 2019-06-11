package com.numa.app.Views;

import android.content.Context;
import android.util.AttributeSet;
import android.view.ViewGroup;

import androidx.annotation.Nullable;
import androidx.appcompat.widget.AppCompatTextView;

public class AutoSizeTextView extends AppCompatTextView {

  public AutoSizeTextView(Context context) {
    super(context);
  }

  public AutoSizeTextView(Context context, @Nullable AttributeSet attrs) {
    super(context, attrs);
  }

  public AutoSizeTextView(Context context, @Nullable AttributeSet attrs, int defStyleAttr) {
    super(context, attrs, defStyleAttr);
  }

  @Override
  protected void onLayout(boolean changed, int left, int top, int right, int bottom) {
    super.onLayout(changed, left, top, right, bottom);
    ViewGroup parent = (ViewGroup) getParent();
    while (parent != null && !(parent instanceof UniformTextLinearLayout)) {
      parent = (ViewGroup) parent.getParent();
    }

    if (parent != null) {
      ((UniformTextLinearLayout) parent).onAutoSizeTextLayout(this);
    }
  }
}
