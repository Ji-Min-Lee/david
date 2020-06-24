package com.jimin.fordavid;

import android.app.Notification;
import android.graphics.drawable.Icon;
import android.os.Bundle;
import android.service.notification.NotificationListenerService;
import android.service.notification.StatusBarNotification;
import android.util.Log;

import com.jimin.fordavid.entities.KakaoMessage;

public class DavidNotificationListener extends NotificationListenerService {
    public final static String TAG = "DavidNotification";

    @Override
    public void onNotificationRemoved(StatusBarNotification sbn) {
        super.onNotificationRemoved(sbn);
        Log.d(TAG, "onNotificationRemoved ~ " +
                " packageName: " + sbn.getPackageName() +
                " id: " + sbn.getId());
    }

    @Override
    public void onNotificationPosted(StatusBarNotification sbn) {
        super.onNotificationPosted(sbn);
        String packageName = sbn.getPackageName();
        if(!packageName.equals("com.kakao.talk")) {
            // other application not kakao
            return;
        }

        Notification notification = sbn.getNotification();
        Bundle extras = sbn.getNotification().extras;
        String userName = extras.getString(Notification.EXTRA_TITLE);
        String text = extras.getString(Notification.EXTRA_TEXT);
        CharSequence csRoom = extras.getCharSequence(Notification.EXTRA_SUB_TEXT);
        if(csRoom == null) {
            return;
        }
        String room = csRoom.toString();

        if(userName==null && text==null && room.contains("개의 안 읽은 메시지")) {
            // trash notification
            return;
        }

        KakaoMessage kakaoMessage = new KakaoMessage(userName, text, room);

        Log.d(TAG, "onNotificationPosted ~ " +
                " packageName: " + sbn.getPackageName() +
                " message: " + kakaoMessage);
    }

}