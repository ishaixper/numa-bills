package com.numa.app.Views;

import android.content.Context;
import android.content.res.TypedArray;
import android.util.AttributeSet;
import android.widget.FrameLayout;
import android.widget.ImageView;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;

import com.numa.app.R;

public class MainButton extends FrameLayout {

    public MainButton(@NonNull Context context, @Nullable AttributeSet attrs) {
        super(context, attrs);
        init(context, attrs);
    }

    public MainButton(@NonNull Context context, @Nullable AttributeSet attrs, int defStyleAttr) {
        super(context, attrs, defStyleAttr);
        init(context, attrs);
    }

    public MainButton(@NonNull Context context, @Nullable AttributeSet attrs, int defStyleAttr, int defStyleRes) {
        super(context, attrs, defStyleAttr, defStyleRes);
        init(context, attrs);
    }

    private void init(Context context, AttributeSet attrs) {
        inflate(context, R.layout.main_button, this);

        TypedArray a = context.getTheme().obtainStyledAttributes(attrs, R.styleable.MainButton, 0, 0);
        String text = null;
        int resId = 0;
        try {
            text = a.getString(R.styleable.MainButton_text);
            resId = a.getResourceId(R.styleable.MainButton_icon, 0);
        } finally {
            a.recycle();
        }

        if (resId != 0) {
            ((ImageView) findViewById(R.id.main_button_icon)).setImageResource(resId);
        }

        if (text != null) {
            ((TextView) findViewById(R.id.main_button_text)).setText(text);
        }
    }
}
