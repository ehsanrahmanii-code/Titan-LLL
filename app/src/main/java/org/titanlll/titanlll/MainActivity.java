package org.titanlll.titanlll;

import android.Manifest;
import android.content.pm.PackageManager;
import android.os.Build;
import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;

import com.chaquo.python.PyObject;
import com.chaquo.python.Python;
import com.chaquo.python.android.AndroidPlatform;

public class MainActivity extends AppCompatActivity {
    private WebView webView;
    private static final int REQ_STORAGE = 1001;
    private final Handler handler = new Handler(Looper.getMainLooper());
    private int loadAttempts = 0;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        webView = findViewById(R.id.webview);
        WebSettings s = webView.getSettings();
        s.setJavaScriptEnabled(true);
        s.setDomStorageEnabled(true);
        s.setLoadWithOverviewMode(true);
        s.setUseWideViewPort(true);
        s.setBuiltInZoomControls(false);
        webView.setWebViewClient(new WebViewClient());

        requestStorageIfNeeded();
        startPythonServer();
        scheduleLoad();
    }

    private void requestStorageIfNeeded() {
        if (Build.VERSION.SDK_INT >= 23) {
            if (ContextCompat.checkSelfPermission(this, Manifest.permission.WRITE_EXTERNAL_STORAGE)
                    != PackageManager.PERMISSION_GRANTED) {
                ActivityCompat.requestPermissions(this,
                        new String[]{
                                Manifest.permission.WRITE_EXTERNAL_STORAGE,
                                Manifest.permission.READ_EXTERNAL_STORAGE
                        }, REQ_STORAGE);
            }
        }
    }

    private void startPythonServer() {
        new Thread(() -> {
            try {
                if (!Python.isStarted()) {
                    Python.start(new AndroidPlatform(getApplicationContext()));
                }
                Python py = Python.getInstance();
                PyObject mod = py.getModule("android_main");
                mod.callAttr("start_server");
            } catch (Exception e) {
                e.printStackTrace();
                handler.post(() ->
                        Toast.makeText(MainActivity.this,
                                "Server error: " + e.getMessage(),
                                Toast.LENGTH_LONG).show());
            }
        }, "titan-python").start();
    }

    private void scheduleLoad() {
        handler.postDelayed(this::tryLoad, 2500);
    }

    private void tryLoad() {
        loadAttempts++;
        webView.loadUrl("http://127.0.0.1:5000/");
        if (loadAttempts < 12) {
            handler.postDelayed(this::tryLoad, 2000);
        }
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
    }

    @Override
    public void onBackPressed() {
        if (webView != null && webView.canGoBack()) {
            webView.goBack();
        } else {
            super.onBackPressed();
        }
    }
}
